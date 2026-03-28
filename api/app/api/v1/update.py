from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_license_by_access_token
from app.models.user_license import UserLicense
from app.models.specialty_version_policy import SpecialtyVersionPolicy
from app.schemas.update import CheckUpdateRequest, CheckUpdateResponse, SpecialtyUpdateInfo
from app.services.cos import read_manifest

router = APIRouter(prefix="/api/update", tags=["update"])


def _compare_versions(local: str, remote: str) -> bool:
    """Return True if remote > local using simple semver comparison."""
    try:
        local_parts = [int(x) for x in local.split(".")]
        remote_parts = [int(x) for x in remote.split(".")]
        return remote_parts > local_parts
    except (ValueError, AttributeError):
        return False


@router.post("/check", response_model=CheckUpdateResponse)
async def check_update(
    req: CheckUpdateRequest,
    lic: UserLicense = Depends(get_license_by_access_token),
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()
    base_valid = lic.expires_at > now

    manifest = read_manifest()
    specialty_updates: list[SpecialtyUpdateInfo] = []

    if req.specialties:
        for spec_data in manifest.get("specialties", []):
            if spec_data.get("product_id") != req.product_id:
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

    return CheckUpdateResponse(
        base_valid=base_valid,
        specialty_updates=specialty_updates,
    )
