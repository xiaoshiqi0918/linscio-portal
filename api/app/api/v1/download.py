from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.deps import get_current_user_by_session, get_license_by_access_token
from app.core.security import generate_cdn_sign_url
from app.models.download_log import DownloadLog
from app.models.user import User
from app.models.user_license import UserLicense
from app.models.user_specialty import UserSpecialty
from app.schemas.download import (
    BundleDownloadRequest,
    BundleDownloadResponse,
    DownloadCompleteRequest,
    SoftwareDownloadRequest,
    SoftwareDownloadResponse,
    SpecialtyDownloadRequest,
    SpecialtyDownloadResponse,
)
from app.schemas.common import SuccessResponse
from app.services.cos import generate_presigned_download_url, read_manifest

router = APIRouter(prefix="/api/download", tags=["download"])


def _match_product(manifest: dict, product_id: str) -> tuple[dict | None, str, str | None]:
    """Case-insensitive product lookup; returns (matched_dict, canonical_id, latest_version)."""
    pid_lower = (product_id or "").lower()
    for prod in manifest.get("products", []):
        if (prod.get("id") or "").lower() == pid_lower:
            return prod, prod["id"], prod.get("latest_version")
    return None, product_id, None


# ---------- Software download (portal, session_token) ----------

@router.post("/software", response_model=SoftwareDownloadResponse)
async def download_software(
    req: SoftwareDownloadRequest,
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
):
    lic = (
        db.query(UserLicense)
        .filter(UserLicense.user_id == user.id, UserLicense.product_id == req.product_id)
        .first()
    )
    if not lic or lic.expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="no_valid_license")

    settings = get_settings()
    manifest = read_manifest()

    prod_matched, canonical_id, latest_ver = _match_product(manifest, req.product_id)
    if not latest_ver:
        latest_ver = manifest.get("latest_versions", {}).get(req.product_id, "0.0.0")

    allowed_platforms = (prod_matched or {}).get("platforms") or []
    if allowed_platforms and req.platform not in allowed_platforms:
        raise HTTPException(status_code=400, detail="platform_unavailable")

    platform_ext = {"win-x64": "zip", "mac-arm64": "dmg", "mac-x64": "dmg"}
    overrides = (prod_matched or {}).get("download_files") or {}
    if req.platform in overrides:
        filename = overrides[req.platform]
    else:
        ext = platform_ext.get(req.platform, "dmg")
        filename = f"LinScio-MedComm-{latest_ver}-{req.platform}.{ext}"
    cos_key = f"releases/{canonical_id}/v{latest_ver}/{filename}"
    download_url = generate_presigned_download_url(cos_key)

    log = DownloadLog(
        user_id=user.id,
        download_type="software",
        resource_id=f"{req.product_id}/v{latest_ver}/{req.platform}",
        platform=req.platform,
    )
    db.add(log)
    db.commit()

    return SoftwareDownloadResponse(
        download_url=download_url,
        filename=filename,
        download_log_id=log.id,
    )


# ---------- Specialty download (software client, access_token) ----------

@router.post("/specialty", response_model=SpecialtyDownloadResponse)
async def download_specialty(
    req: SpecialtyDownloadRequest,
    lic: UserLicense = Depends(get_license_by_access_token),
    db: Session = Depends(get_db),
):
    owned = db.query(UserSpecialty).filter_by(
        user_id=lic.user_id, product_id=req.product_id, specialty_id=req.specialty_id,
    ).first()
    if not owned:
        raise HTTPException(status_code=403, detail="specialty_not_purchased")

    settings = get_settings()
    manifest = read_manifest()

    pid_lower = (req.product_id or "").lower()
    spec_info = None
    for s in manifest.get("specialties", []):
        if s["id"] == req.specialty_id and (s.get("product_id") or "").lower() == pid_lower:
            spec_info = s
            break
    if not spec_info:
        raise HTTPException(status_code=404, detail="specialty_not_found")

    if req.from_version and req.from_version in spec_info.get("patch_from", {}):
        pkg = spec_info["patch_from"][req.from_version]
        package_type = "patch"
    else:
        pkg = spec_info.get("full_package", {})
        package_type = "full"

    filename = pkg.get("filename", "")
    path = f"/specialties/{req.product_id}/{req.specialty_id}/v{req.version}/{filename}"
    download_url = generate_cdn_sign_url(path, settings.CDN_AUTH_SECRET, settings.CDN_DOMAIN_SPECIALTIES)

    log = DownloadLog(
        user_id=lic.user_id,
        download_type="specialty",
        resource_id=f"{req.specialty_id}/v{req.version}",
    )
    db.add(log)
    db.commit()

    return SpecialtyDownloadResponse(
        package_type=package_type,
        download_url=download_url,
        filename=filename,
        size_mb=pkg.get("size_mb"),
        md5=pkg.get("md5"),
        download_log_id=log.id,
    )


# ---------- Drawing pack download (software client, access_token) ----------

@router.post("/drawing-pack", response_model=SpecialtyDownloadResponse)
async def download_drawing_pack(
    req: SpecialtyDownloadRequest,
    lic: UserLicense = Depends(get_license_by_access_token),
    db: Session = Depends(get_db),
):
    owned = db.query(UserSpecialty).filter_by(
        user_id=lic.user_id, product_id=req.product_id, specialty_id=req.specialty_id,
    ).first()
    if not owned:
        raise HTTPException(status_code=403, detail="drawing_pack_not_purchased")

    settings = get_settings()
    manifest = read_manifest()

    pid_lower = (req.product_id or "").lower()
    pack_info = None
    for p in manifest.get("drawing_packs", []):
        if p["id"] == req.specialty_id and (p.get("product_id") or "").lower() == pid_lower:
            pack_info = p
            break
    if not pack_info:
        raise HTTPException(status_code=404, detail="drawing_pack_not_found")

    if req.from_version and req.from_version in pack_info.get("patch_from", {}):
        pkg = pack_info["patch_from"][req.from_version]
        package_type = "patch"
    else:
        pkg = pack_info.get("full_package", {})
        package_type = "full"

    filename = pkg.get("filename", "")
    path = f"/drawing-packs/{req.product_id}/{req.specialty_id}/v{req.version}/{filename}"
    download_url = generate_cdn_sign_url(path, settings.CDN_AUTH_SECRET, settings.CDN_DOMAIN_SPECIALTIES)

    log = DownloadLog(
        user_id=lic.user_id,
        download_type="drawing_pack",
        resource_id=f"{req.specialty_id}/v{req.version}",
    )
    db.add(log)
    db.commit()

    return SpecialtyDownloadResponse(
        package_type=package_type,
        download_url=download_url,
        filename=filename,
        size_mb=pkg.get("size_mb"),
        md5=pkg.get("md5"),
        download_log_id=log.id,
    )


# ---------- Bundle download (ComfyUI, software client, access_token) ----------

@router.post("/bundle", response_model=BundleDownloadResponse)
async def download_bundle(
    req: BundleDownloadRequest,
    lic: UserLicense = Depends(get_license_by_access_token),
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()
    if lic.expires_at < now:
        raise HTTPException(status_code=403, detail="license_expired")

    manifest = read_manifest()

    pid_lower = (req.product_id or "").lower()
    bundle_info = None
    for b in manifest.get("bundles", []):
        if b["id"] == req.bundle_id and (b.get("product_id") or "").lower() == pid_lower:
            bundle_info = b
            break
    if not bundle_info:
        raise HTTPException(status_code=404, detail="bundle_not_found")

    plat_info = (bundle_info.get("platforms") or {}).get(req.platform)
    if not plat_info:
        raise HTTPException(status_code=400, detail="platform_unavailable")

    filename = plat_info.get("filename", "")
    version = bundle_info.get("version", "0.0.0")
    cos_key = f"bundles/{req.product_id}/{req.bundle_id}/v{version}/{filename}"
    download_url = generate_presigned_download_url(cos_key, expires=86400)

    log = DownloadLog(
        user_id=lic.user_id,
        download_type="bundle",
        resource_id=f"{req.bundle_id}/v{version}/{req.platform}",
        platform=req.platform,
    )
    db.add(log)
    db.commit()

    return BundleDownloadResponse(
        download_url=download_url,
        filename=filename,
        size_bytes=plat_info.get("size_bytes", 0),
        sha256=plat_info.get("sha256", ""),
        download_log_id=log.id,
    )


# ---------- Product info (public, for download pages) ----------

@router.get("/product-info")
async def get_product_info():
    """Public endpoint: returns product, bundle, specialty, drawing-pack info from manifest."""
    manifest = read_manifest()

    products = {}
    for prod in manifest.get("products", []):
        products[prod["id"]] = {
            "id": prod["id"],
            "name": prod.get("name", prod["id"]),
            "latest_version": prod.get("latest_version", "0.0.0"),
            "published_at": prod.get("published_at"),
            "release_notes": prod.get("release_notes"),
            "platforms": prod.get("platforms", []),
            "platform_status": prod.get("platform_status", {}),
            "download_files": prod.get("download_files", {}),
            "system_requirements": prod.get("system_requirements", {}),
            "changelog": prod.get("changelog", []),
        }

    bundles = []
    for b in manifest.get("bundles", []):
        bundles.append({
            "id": b["id"],
            "product_id": b.get("product_id"),
            "name": b.get("name", ""),
            "type": b.get("type", "basic"),
            "version": b.get("version", "0.0.0"),
            "description": b.get("description", ""),
            "authorization": b.get("authorization", ""),
            "platforms": {k: {"filename": v.get("filename"), "size_bytes": v.get("size_bytes", 0)}
                         for k, v in (b.get("platforms") or {}).items()},
        })

    specialties = []
    for s in manifest.get("specialties", []):
        specialties.append({
            "id": s["id"],
            "product_id": s.get("product_id"),
            "name": s.get("name", ""),
            "version": s.get("version", "0.0.0"),
            "description": s.get("description", ""),
            "includes": s.get("includes", []),
            "size_mb": s.get("full_package", {}).get("size_mb"),
        })

    drawing_packs = []
    for d in manifest.get("drawing_packs", []):
        drawing_packs.append({
            "id": d["id"],
            "product_id": d.get("product_id"),
            "name": d.get("name", ""),
            "version": d.get("version", "0.0.0"),
            "description": d.get("description", ""),
            "includes": d.get("includes", []),
            "size_mb": d.get("full_package", {}).get("size_mb"),
        })

    return {
        "schema_version": manifest.get("schema_version", "1.0"),
        "min_client_version": manifest.get("min_client_version"),
        "products": products,
        "bundles": bundles,
        "specialties": specialties,
        "drawing_packs": drawing_packs,
    }


# ---------- Download complete callback ----------

@router.post("/complete", response_model=SuccessResponse)
async def download_complete(
    req: DownloadCompleteRequest,
    lic: UserLicense = Depends(get_license_by_access_token),
    db: Session = Depends(get_db),
):
    log = db.query(DownloadLog).filter(
        DownloadLog.id == req.download_log_id, DownloadLog.user_id == lic.user_id,
    ).first()
    if log:
        log.completed = 1
        log.completed_at = datetime.utcnow()
        db.commit()
    return SuccessResponse()
