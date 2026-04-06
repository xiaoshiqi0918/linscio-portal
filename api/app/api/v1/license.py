import re
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_client_ip, get_current_user_by_session, get_license_by_access_token
from app.core.security import generate_short_code, generate_token
from app.middleware.rate_limit import check_rate_limit, record_failure
from app.models.activation_code import ActivationCode
from app.models.license_code import LicenseCode
from app.models.product import Product
from app.models.user import User
from app.models.user_license import UserLicense
from app.models.user_specialty import UserSpecialty
from app.models.specialty_version_policy import SpecialtyVersionPolicy
from app.schemas.common import ProductListResponse, ProductOut
from app.services.cos import read_manifest
from app.schemas.license import (
    ActivateLicenseRequest,
    ActivateLicenseResponse,
    BaseStatus,
    LicenseStatusAllResponse,
    LicenseStatusRequest,
    LicenseStatusResponse,
    ProductLicenseInfo,
    ProductSpecialtyInfo,
    SpecialtyInfo,
    VersionPolicyInfo,
)

router = APIRouter(tags=["license"])

CODE_PATTERN = re.compile(r"^LINSCIO-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$")


# ---------- Public: product list ----------

@router.get("/api/products", response_model=ProductListResponse)
async def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.is_active == 1).order_by(Product.sort_order).all()
    return ProductListResponse(
        products=[
            ProductOut(
                product_id=p.product_id, name=p.name,
                description=p.description, sort_order=p.sort_order,
            )
            for p in products
        ]
    )


# ---------- Activate license code (portal) ----------

@router.post("/api/license/activate", response_model=ActivateLicenseResponse)
async def activate_license(
    req: ActivateLicenseRequest,
    request: Request,
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
):
    if not user.email_verified:
        raise HTTPException(status_code=400, detail="email_not_verified")

    ip = get_client_ip(request)
    allowed, _ = check_rate_limit(db, "activate_ip", ip, 5, 3600, 3600)
    if not allowed:
        raise HTTPException(status_code=429, detail="rate_limit_exceeded")
    allowed, _ = check_rate_limit(db, "activate_user", str(user.id), 10, None, None)
    if not allowed:
        raise HTTPException(status_code=429, detail="rate_limit_exceeded")

    if not CODE_PATTERN.match(req.code):
        record_failure(db, "activate_ip", ip, 5, 3600)
        raise HTTPException(status_code=400, detail="code_format_invalid")

    lc = db.query(LicenseCode).filter(LicenseCode.code == req.code, LicenseCode.is_activated == 0).first()
    if not lc:
        record_failure(db, "activate_ip", ip, 5, 3600)
        record_failure(db, "activate_user", str(user.id), 10, None)
        raise HTTPException(status_code=400, detail="code_invalid_or_used")

    now = datetime.utcnow()

    # --- basic license ---
    if lc.license_type == "basic":
        existing = (
            db.query(UserLicense)
            .filter(UserLicense.user_id == user.id, UserLicense.product_id == lc.product_id)
            .first()
        )
        if lc.is_trial and lc.duration_days:
            delta = timedelta(days=lc.duration_days)
            days_count = lc.duration_days
        else:
            months = lc.duration_months or 12
            delta = timedelta(days=months * 30)
            days_count = months * 30

        if not existing:
            new_expires = now + delta
            lic = UserLicense(
                user_id=user.id,
                product_id=lc.product_id,
                is_trial=lc.is_trial,
                started_at=now,
                expires_at=new_expires,
                device_fingerprint=req.device_fingerprint,
                device_name=req.device_name,
                rebind_count=0,
            )
            db.add(lic)
            db.flush()

            db.query(ActivationCode).filter(
                ActivationCode.user_id == user.id,
                ActivationCode.product_id == lc.product_id,
                ActivationCode.is_used == 0,
            ).update({ActivationCode.is_used: 1}, synchronize_session=False)

            ac_code = generate_short_code(8)
            ac = ActivationCode(
                code=ac_code, user_id=user.id, product_id=lc.product_id,
                device_fingerprint=req.device_fingerprint,
                expires_at=now + timedelta(minutes=5),
            )
            db.add(ac)

            lc.is_activated = 1
            lc.activated_by = user.id
            lc.activated_at = now
            db.commit()

            deep_link = f"linscio://auth?activation_code={ac_code}"
            return ActivateLicenseResponse(
                license_type="basic", is_trial=bool(lc.is_trial),
                new_expires_at=new_expires.isoformat() + "Z",
                days_added=days_count, deep_link=deep_link,
            )

        if existing.is_trial == 1 and not lc.is_trial:
            existing.expires_at = now + delta
            existing.is_trial = 0
            existing.rebind_count = 0
        elif existing.is_trial == 0:
            if lc.is_trial:
                raise HTTPException(status_code=400, detail="already_has_formal_license")
            base = max(now, existing.expires_at)
            existing.expires_at = base + delta
            existing.rebind_count = 0
        else:
            existing.expires_at = now + delta
            existing.rebind_count = 0

        lc.is_activated = 1
        lc.activated_by = user.id
        lc.activated_at = now
        db.commit()

        return ActivateLicenseResponse(
            license_type="basic", is_trial=bool(existing.is_trial),
            new_expires_at=existing.expires_at.isoformat() + "Z",
            days_added=days_count, token_unchanged=True,
        )

    # --- specialty license ---
    if lc.license_type == "specialty":
        existing_lic = (
            db.query(UserLicense)
            .filter(UserLicense.user_id == user.id, UserLicense.product_id == lc.product_id)
            .first()
        )
        if not existing_lic or existing_lic.is_trial == 1:
            raise HTTPException(status_code=400, detail="trial_cannot_activate_specialty")

        specialty_ids = lc.specialty_ids or []
        for sid in specialty_ids:
            exists = db.query(UserSpecialty).filter_by(
                user_id=user.id, product_id=lc.product_id, specialty_id=sid,
            ).first()
            if not exists:
                db.add(UserSpecialty(
                    user_id=user.id, product_id=lc.product_id,
                    specialty_id=sid, license_code_id=lc.id,
                ))

        lc.is_activated = 1
        lc.activated_by = user.id
        lc.activated_at = now
        db.commit()

        deep_link = f"linscio://specialty/new?ids={','.join(specialty_ids)}&product={lc.product_id}"
        return ActivateLicenseResponse(
            license_type="specialty",
            specialty_ids=specialty_ids,
            deep_link=deep_link,
        )

    raise HTTPException(status_code=400, detail="unknown_license_type")


# ---------- License status (software client, POST) ----------

@router.post("/api/license/status", response_model=LicenseStatusResponse)
async def license_status(
    req: LicenseStatusRequest,
    lic: UserLicense = Depends(get_license_by_access_token),
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()

    if req.reported_specialties:
        lic.reported_specialties = req.reported_specialties
        lic.reported_at = now
        db.commit()

    days_remaining = max(0, (lic.expires_at - now).days) if lic.expires_at > now else 0
    base = BaseStatus(
        valid=lic.expires_at > now,
        is_trial=bool(lic.is_trial),
        expires_at=lic.expires_at.isoformat() + "Z" if lic.expires_at else None,
        days_remaining=days_remaining,
        device_name=lic.device_name,
        rebind_remaining=max(0, 2 - lic.rebind_count),
    )

    user_specs = db.query(UserSpecialty).filter(
        UserSpecialty.user_id == lic.user_id, UserSpecialty.product_id == req.product_id,
    ).all()

    manifest = read_manifest()
    manifest_map: dict[str, dict] = {}
    for s in manifest.get("specialties", []):
        if s.get("product_id") == req.product_id:
            manifest_map[s["id"]] = s
    for dp in manifest.get("drawing_packs", []):
        if dp.get("product_id") == req.product_id:
            manifest_map[dp["id"]] = dp

    reported = req.reported_specialties or {}
    specialties = []
    for us in user_specs:
        m = manifest_map.get(us.specialty_id, {})
        specialties.append(SpecialtyInfo(
            id=us.specialty_id,
            name=m.get("name", us.specialty_id),
            remote_version=m.get("version"),
            local_version=reported.get(us.specialty_id),
            purchased_at=us.purchased_at.isoformat() + "Z" if us.purchased_at else None,
        ))

    policies = db.query(SpecialtyVersionPolicy).filter(
        SpecialtyVersionPolicy.product_id == req.product_id,
    ).all()
    version_policies = [
        VersionPolicyInfo(
            specialty_id=p.specialty_id,
            force_min_version=p.force_min_version,
            force_max_version=p.force_max_version,
            policy_message=p.policy_message,
        )
        for p in policies
    ]

    return LicenseStatusResponse(base=base, specialties=specialties, version_policies=version_policies)


# ---------- License status all (portal, GET) ----------

@router.get("/api/license/status/all", response_model=LicenseStatusAllResponse)
async def license_status_all(
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
):
    products = db.query(Product).filter(Product.is_active == 1).order_by(Product.sort_order).all()
    now = datetime.utcnow()
    result = []

    manifest = read_manifest()
    manifest_map: dict[str, dict[str, dict]] = {}
    for s in manifest.get("specialties", []):
        manifest_map.setdefault(s.get("product_id", ""), {})[s["id"]] = s
    for dp in manifest.get("drawing_packs", []):
        manifest_map.setdefault(dp.get("product_id", ""), {})[dp["id"]] = dp

    for p in products:
        lic = (
            db.query(UserLicense)
            .filter(UserLicense.user_id == user.id, UserLicense.product_id == p.product_id)
            .first()
        )
        if not lic:
            result.append(ProductLicenseInfo(
                product_id=p.product_id, product_name=p.name,
                status="not_activated",
            ))
            continue

        if lic.is_trial:
            status = "trial" if lic.expires_at > now else "expired"
        else:
            status = "valid" if lic.expires_at > now else "expired"

        days_remaining = max(0, (lic.expires_at - now).days) if lic.expires_at > now else 0

        user_specs = db.query(UserSpecialty).filter(
            UserSpecialty.user_id == user.id, UserSpecialty.product_id == p.product_id,
        ).all()
        reported = lic.reported_specialties or {}
        spec_list = []
        for us in user_specs:
            m = manifest_map.get(p.product_id, {}).get(us.specialty_id, {})
            spec_list.append(ProductSpecialtyInfo(
                id=us.specialty_id,
                name=m.get("name", us.specialty_id),
                remote_version=m.get("version"),
                local_version=reported.get(us.specialty_id),
                purchased_at=us.purchased_at.isoformat() + "Z" if us.purchased_at else None,
            ))

        result.append(ProductLicenseInfo(
            product_id=p.product_id, product_name=p.name,
            status=status, is_trial=bool(lic.is_trial),
            expires_at=lic.expires_at.isoformat() + "Z",
            days_remaining=days_remaining,
            device_name=lic.device_name,
            rebind_remaining=max(0, 2 - lic.rebind_count),
            specialties=spec_list,
        ))

    return LicenseStatusAllResponse(licenses=result)


# ---------- User specialties (portal, GET) ----------

@router.get("/api/license/specialties")
async def user_specialties(
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
):
    rows = db.query(UserSpecialty).filter(UserSpecialty.user_id == user.id).all()
    return {
        "specialties": [
            {
                "id": r.specialty_id,
                "product_id": r.product_id,
                "purchased_at": r.purchased_at.isoformat() + "Z" if r.purchased_at else None,
            }
            for r in rows
        ]
    }
