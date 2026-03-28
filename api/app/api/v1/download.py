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
    DownloadCompleteRequest,
    SoftwareDownloadRequest,
    SoftwareDownloadResponse,
    SpecialtyDownloadRequest,
    SpecialtyDownloadResponse,
)
from app.schemas.common import SuccessResponse
from app.services.cos import read_manifest

router = APIRouter(prefix="/api/download", tags=["download"])


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

    platform_map = {
        "mac-arm64": "arm64.dmg",
        "mac-x64": "x64.dmg",
        "win-x64": "x64.exe",
    }
    ext = platform_map.get(req.platform, "x64.dmg")

    latest_ver = "0.0.0"
    for spec in manifest.get("specialties", []):
        pass

    filename = f"LinScio-{req.product_id}-{latest_ver}-{ext}"
    download_url = f"https://{settings.CDN_DOMAIN_RELEASES}/releases/{req.product_id}/v{latest_ver}/{filename}"

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

    spec_info = None
    for s in manifest.get("specialties", []):
        if s["id"] == req.specialty_id and s.get("product_id") == req.product_id:
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
