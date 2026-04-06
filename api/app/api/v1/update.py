from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_license_by_access_token
from app.models.user_license import UserLicense
from app.models.specialty_version_policy import SpecialtyVersionPolicy
from app.schemas.update import CheckUpdateRequest, CheckUpdateResponse, SpecialtyUpdateInfo, BundleUpdateInfo
from app.services.cos import generate_presigned_download_url, read_manifest

router = APIRouter(prefix="/api/update", tags=["update"])


def _compare_versions(local: str, remote: str) -> bool:
    """Return True if remote > local using simple semver comparison."""
    try:
        local_parts = [int(x) for x in local.split(".")]
        remote_parts = [int(x) for x in remote.split(".")]
        return remote_parts > local_parts
    except (ValueError, AttributeError):
        return False


def _match_product(manifest: dict, product_id: str) -> tuple[dict | None, str]:
    """Case-insensitive product lookup; returns (matched_dict, canonical_id)."""
    pid_lower = (product_id or "").lower()
    for prod in manifest.get("products", []):
        if (prod.get("id") or "").lower() == pid_lower:
            return prod, prod["id"]
    return None, product_id


@router.post("/check", response_model=CheckUpdateResponse)
async def check_update(
    req: CheckUpdateRequest,
    lic: UserLicense = Depends(get_license_by_access_token),
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()
    base_valid = lic.expires_at > now

    manifest = read_manifest()

    has_software_update = False
    latest_version: str | None = None
    download_url: str | None = None

    prod_matched, canonical_id = _match_product(manifest, req.product_id)
    if prod_matched:
        latest_version = prod_matched.get("latest_version")
    if not latest_version:
        lv_map = manifest.get("latest_versions") or {}
        latest_version = lv_map.get(req.product_id) or lv_map.get(canonical_id)

    update_download_url: str | None = None
    update_filename: str | None = None
    update_size_bytes: int = 0
    update_sha256: str = ""
    release_notes: str | None = None

    if base_valid and latest_version and _compare_versions(req.software_version, latest_version):
        has_software_update = True
        platform_ext = {"win-x64": "exe", "mac-arm64": "dmg", "mac-x64": "dmg"}
        overrides = (prod_matched or {}).get("download_files") or {}
        if req.platform in overrides:
            filename = overrides[req.platform]
        else:
            ext = platform_ext.get(req.platform, "dmg")
            filename = f"LinScio-MedComm-{latest_version}-{req.platform}.{ext}"
        cos_key = f"releases/{canonical_id}/v{latest_version}/{filename}"
        download_url = generate_presigned_download_url(cos_key, expires=86400)

        update_files = (prod_matched or {}).get("update_files") or {}
        uf = update_files.get(req.platform) or {}
        if uf.get("filename"):
            update_filename = uf["filename"]
            update_size_bytes = uf.get("size_bytes", 0)
            update_sha256 = uf.get("sha256", "")
            uf_cos_key = f"releases/{canonical_id}/v{latest_version}/{update_filename}"
            update_download_url = generate_presigned_download_url(uf_cos_key, expires=86400)

        release_notes = (prod_matched or {}).get("release_notes")

    pid_lower = (req.product_id or "").lower()

    specialty_updates: list[SpecialtyUpdateInfo] = []
    if req.specialties:
        for spec_data in manifest.get("specialties", []):
            if (spec_data.get("product_id") or "").lower() != pid_lower:
                continue
            sid = spec_data["id"]
            local_ver = req.specialties.get(sid)
            if local_ver is None:
                continue

            remote_ver = spec_data.get("version", "0.0.0")
            has_update = _compare_versions(local_ver, remote_ver)

            patch_info = spec_data.get("patch_from", {}).get(local_ver)
            full_info = spec_data.get("full_package", {})

            policy = db.query(SpecialtyVersionPolicy).filter_by(
                specialty_id=sid, product_id=req.product_id,
            ).first()

            force_update = False
            force_message = None
            if policy and policy.force_min_version:
                force_update = _compare_versions(local_ver, policy.force_min_version)
                force_message = policy.policy_message

            changelog_entries = []
            for cl in spec_data.get("changelog", []):
                if _compare_versions(local_ver, cl.get("version", "0.0.0")):
                    changelog_entries.extend(cl.get("changes", []))

            specialty_updates.append(SpecialtyUpdateInfo(
                id=sid,
                latest_version=remote_ver,
                has_update=has_update,
                size_mb=patch_info.get("size_mb") if patch_info else full_info.get("size_mb"),
                full_size_mb=full_info.get("size_mb"),
                changelog=changelog_entries,
                force_update=force_update,
                force_message=force_message,
            ))

    drawing_pack_updates: list[SpecialtyUpdateInfo] = []
    if req.drawing_packs:
        for pack_data in manifest.get("drawing_packs", []):
            if (pack_data.get("product_id") or "").lower() != pid_lower:
                continue
            pid = pack_data["id"]
            local_ver = req.drawing_packs.get(pid)
            if local_ver is None:
                continue

            remote_ver = pack_data.get("version", "0.0.0")
            has_update = _compare_versions(local_ver, remote_ver)
            full_info = pack_data.get("full_package", {})

            changelog_entries = []
            for cl in pack_data.get("changelog", []):
                if _compare_versions(local_ver, cl.get("version", "0.0.0")):
                    changelog_entries.extend(cl.get("changes", []))

            drawing_pack_updates.append(SpecialtyUpdateInfo(
                id=pid,
                latest_version=remote_ver,
                has_update=has_update,
                category="drawing",
                size_mb=full_info.get("size_mb"),
                full_size_mb=full_info.get("size_mb"),
                changelog=changelog_entries,
            ))

    # ── Bundle updates (ComfyUI etc.) ──
    bundle_updates: list[BundleUpdateInfo] = []
    if True:  # always return bundle info regardless of client request
        for bundle_data in manifest.get("bundles", []):
            if (bundle_data.get("product_id") or "").lower() != pid_lower:
                continue
            bid = bundle_data["id"]
            remote_ver = bundle_data.get("version", "0.0.0")
            local_ver = (req.bundles or {}).get(bid)
            has_bundle_update = local_ver is None or _compare_versions(local_ver, remote_ver)

            plat_info = (bundle_data.get("platforms") or {}).get(req.platform, {})

            bundle_updates.append(BundleUpdateInfo(
                id=bid,
                name=bundle_data.get("name", ""),
                latest_version=remote_ver,
                has_update=has_bundle_update,
                size_bytes=plat_info.get("size_bytes", 0),
                sha256=plat_info.get("sha256", ""),
                min_client_version=bundle_data.get("min_client_version"),
            ))

    # ── Platform status ──
    platform_status_val = None
    if prod_matched:
        ps = prod_matched.get("platform_status", {})
        platform_status_val = ps.get(req.platform)

    # ── Global min_client_version ──
    global_min_ver = manifest.get("min_client_version")

    return CheckUpdateResponse(
        base_valid=base_valid,
        has_software_update=has_software_update,
        latest_version=latest_version,
        download_url=download_url,
        update_download_url=update_download_url,
        update_filename=update_filename,
        update_size_bytes=update_size_bytes,
        update_sha256=update_sha256,
        min_client_version=global_min_ver,
        platform_status=platform_status_val,
        release_notes=release_notes,
        specialty_updates=specialty_updates,
        drawing_pack_updates=drawing_pack_updates,
        bundle_updates=bundle_updates,
    )
