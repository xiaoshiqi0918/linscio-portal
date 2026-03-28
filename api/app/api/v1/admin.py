import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_admin, get_client_ip
from app.core.security import generate_short_code, generate_token
from app.models.admin_log import AdminLog
from app.models.device_rebind_log import DeviceRebindLog
from app.models.download_log import DownloadLog
from app.models.license_code import LicenseCode
from app.models.product import Product
from app.models.security_limit import SecurityLimit
from app.models.account_migration_request import AccountMigrationRequest
from app.models.activation_code import ActivationCode
from app.models.specialty_version_policy import SpecialtyVersionPolicy
from app.models.user import User
from app.models.user_license import UserLicense
from app.models.user_session import UserSession
from app.schemas.admin import (
    BanUserRequest,
    ForceRebindRequest,
    GenerateLicenseRequest,
    GenerateLicenseResponse,
    MigrationHandleRequest,
    StatsOverview,
    UnlockSecurityRequest,
    UpdatePolicyRequest,
    UpdateProductRequest,
)
from app.schemas.common import SuccessResponse
from app.services.cos import list_release_files, read_manifest

router = APIRouter(prefix="/admin", tags=["admin"])


def _log_action(db: Session, admin_id: int, action: str, target_type: str, target_id: str, detail: dict, ip: str):
    db.add(AdminLog(
        admin_user_id=admin_id, action_type=action,
        target_type=target_type, target_id=str(target_id),
        detail=detail, client_ip=ip,
    ))


# ---------- Stats overview ----------

@router.get("/stats/overview", response_model=StatsOverview)
async def stats_overview(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    now = datetime.utcnow()
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    total_users = db.query(func.count(User.id)).filter(User.is_active == 1).scalar()
    active_licenses = db.query(func.count(UserLicense.id)).filter(UserLicense.expires_at > now).scalar()
    expiring_soon = db.query(func.count(UserLicense.id)).filter(
        UserLicense.expires_at.between(now, now + timedelta(days=30)),
    ).scalar()

    monthly_sw = db.query(func.count(DownloadLog.id)).filter(
        DownloadLog.download_type == "software", DownloadLog.created_at >= month_start,
    ).scalar()
    monthly_sp = db.query(func.count(DownloadLog.id)).filter(
        DownloadLog.download_type == "specialty", DownloadLog.created_at >= month_start,
    ).scalar()

    total_dl = db.query(func.count(DownloadLog.id)).filter(DownloadLog.created_at >= month_start).scalar()
    completed_dl = db.query(func.count(DownloadLog.id)).filter(
        DownloadLog.created_at >= month_start, DownloadLog.completed == 1,
    ).scalar()
    rate = (completed_dl / total_dl * 100) if total_dl else 0

    return StatsOverview(
        total_users=total_users,
        active_licenses=active_licenses,
        expiring_soon=expiring_soon,
        monthly_downloads=monthly_sw,
        monthly_specialty_downloads=monthly_sp,
        download_success_rate=round(rate, 1),
    )


# ---------- User management ----------

@router.get("/users")
async def list_users(
    q: str = Query("", description="Search email or phone"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if q:
        query = query.filter(User.email.contains(q) | User.phone.contains(q))
    total = query.count()
    users = query.order_by(User.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total, "page": page, "size": size,
        "items": [
            {
                "id": u.id, "email": u.email, "phone": u.phone,
                "is_active": u.is_active, "is_admin": u.is_admin,
                "email_verified": u.email_verified,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
    }


@router.post("/users/{user_id}/ban", response_model=SuccessResponse)
async def ban_user(
    user_id: int,
    req: BanUserRequest,
    request: Request,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="用户不存在")

    target.is_active = 0
    db.query(UserSession).filter(UserSession.user_id == user_id).delete()
    db.query(UserLicense).filter(UserLicense.user_id == user_id).update(
        {UserLicense.access_token: None}, synchronize_session=False,
    )

    _log_action(db, admin.id, "ban_user", "user", str(user_id), {"reason": req.reason}, get_client_ip(request))
    db.commit()
    return SuccessResponse()


@router.post("/users/{user_id}/unban", response_model=SuccessResponse)
async def unban_user(
    user_id: int,
    request: Request,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="用户不存在")
    target.is_active = 1
    _log_action(db, admin.id, "unban_user", "user", str(user_id), {}, get_client_ip(request))
    db.commit()
    return SuccessResponse()


# ---------- License code management ----------

def _generate_license_code() -> str:
    seg = lambda: uuid.uuid4().hex[:4].upper()
    return f"LINSCIO-{seg()}-{seg()}-{seg()}"


@router.post("/licenses/generate", response_model=GenerateLicenseResponse)
async def generate_licenses(
    req: GenerateLicenseRequest,
    request: Request,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.product_id == req.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="产品不存在")
    if req.count > 100:
        raise HTTPException(status_code=400, detail="单次最多生成 100 个")

    codes: list[str] = []
    for _ in range(req.count):
        code = _generate_license_code()
        lc = LicenseCode(
            code=code,
            product_id=req.product_id,
            license_type=req.license_type,
            duration_months=req.duration_months,
            is_trial=1 if req.is_trial else 0,
            specialty_ids=req.specialty_ids,
            recipient_note=req.recipient_note,
            created_by_admin=admin.id,
        )
        db.add(lc)
        codes.append(code)

    _log_action(
        db, admin.id, "generate_codes", "license_code", "",
        {"count": req.count, "product": req.product_id, "type": req.license_type},
        get_client_ip(request),
    )
    db.commit()
    return GenerateLicenseResponse(codes=codes)


@router.get("/licenses")
async def list_licenses(
    product_id: str = Query("", description="Filter by product"),
    is_activated: int | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(LicenseCode)
    if product_id:
        query = query.filter(LicenseCode.product_id == product_id)
    if is_activated is not None:
        query = query.filter(LicenseCode.is_activated == is_activated)
    total = query.count()
    items = query.order_by(LicenseCode.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total, "page": page, "size": size,
        "items": [
            {
                "id": lc.id, "code": lc.code, "product_id": lc.product_id,
                "license_type": lc.license_type, "duration_months": lc.duration_months,
                "is_trial": lc.is_trial, "is_activated": lc.is_activated,
                "activated_by": lc.activated_by, "activated_at": lc.activated_at.isoformat() if lc.activated_at else None,
                "recipient_note": lc.recipient_note,
                "created_at": lc.created_at.isoformat() if lc.created_at else None,
            }
            for lc in items
        ],
    }


@router.post("/licenses/{code_id}/void", response_model=SuccessResponse)
async def void_license_code(
    code_id: int,
    request: Request,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    lc = db.query(LicenseCode).filter(LicenseCode.id == code_id).first()
    if not lc:
        raise HTTPException(status_code=404, detail="授权码不存在")
    if lc.is_activated:
        raise HTTPException(status_code=400, detail="已激活的授权码不可作废")
    db.delete(lc)
    _log_action(db, admin.id, "void_code", "license_code", str(code_id), {"code": lc.code}, get_client_ip(request))
    db.commit()
    return SuccessResponse()


# ---------- Device management ----------

@router.get("/devices")
async def list_devices(
    q: str = Query(""),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(UserLicense, User).join(User, User.id == UserLicense.user_id)
    if q:
        query = query.filter(User.email.contains(q) | UserLicense.device_name.contains(q))
    total = query.count()
    items = query.order_by(UserLicense.updated_at.desc().nullslast()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total, "page": page, "size": size,
        "items": [
            {
                "user_id": lic.user_id, "email": u.email,
                "product_id": lic.product_id, "device_name": lic.device_name,
                "device_fingerprint": lic.device_fingerprint,
                "rebind_count": lic.rebind_count,
                "last_seen_at": lic.last_seen_at.isoformat() if lic.last_seen_at else None,
                "expires_at": lic.expires_at.isoformat() if lic.expires_at else None,
            }
            for lic, u in items
        ],
    }


@router.post("/devices/reset", response_model=SuccessResponse)
async def force_rebind(
    req: ForceRebindRequest,
    request: Request,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    lic = db.query(UserLicense).filter(
        UserLicense.user_id == req.user_id, UserLicense.product_id == req.product_id,
    ).first()
    if not lic:
        raise HTTPException(status_code=404, detail="授权记录不存在")

    old_fp = lic.device_fingerprint
    old_name = lic.device_name
    lic.device_fingerprint = None
    lic.device_name = None
    lic.access_token = None
    lic.rebind_count = 0

    db.add(DeviceRebindLog(
        user_id=req.user_id, product_id=req.product_id,
        old_fingerprint=old_fp, old_device_name=old_name,
        rebind_type="admin", operator_ip=get_client_ip(request),
    ))
    _log_action(
        db, admin.id, "force_rebind", "device", str(req.user_id),
        {"product_id": req.product_id, "reason": req.reason}, get_client_ip(request),
    )
    db.commit()
    return SuccessResponse()


# ---------- Account migration ----------

@router.get("/migrations")
async def list_migrations(
    status: str = Query("pending"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(AccountMigrationRequest)
    if status:
        query = query.filter(AccountMigrationRequest.status == status)
    total = query.count()
    items = query.order_by(AccountMigrationRequest.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total, "page": page, "size": size,
        "items": [
            {
                "id": m.id, "from_user_id": m.from_user_id,
                "to_credential": m.to_credential, "reason": m.reason,
                "status": m.status,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in items
        ],
    }


@router.post("/migrations/{migration_id}/handle", response_model=SuccessResponse)
async def handle_migration(
    migration_id: int,
    req: MigrationHandleRequest,
    request: Request,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    m = db.query(AccountMigrationRequest).filter(AccountMigrationRequest.id == migration_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="申请不存在")
    if m.status != "pending":
        raise HTTPException(status_code=400, detail="该申请已处理")

    m.status = "approved" if req.action == "approve" else "rejected"
    m.handled_by = admin.id
    m.handled_at = datetime.utcnow()

    action_type = "approve_migration" if req.action == "approve" else "reject_migration"
    _log_action(db, admin.id, action_type, "migration", str(migration_id), {"reason": req.reason}, get_client_ip(request))
    db.commit()
    return SuccessResponse()


# ---------- Specialty management ----------

@router.get("/specialties")
async def list_specialties(admin: User = Depends(get_current_admin)):
    manifest = read_manifest()
    return {"specialties": manifest.get("specialties", [])}


@router.put("/specialties/{specialty_id}/policy", response_model=SuccessResponse)
async def update_specialty_policy(
    specialty_id: str,
    req: UpdatePolicyRequest,
    request: Request,
    product_id: str = Query(...),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    policy = db.query(SpecialtyVersionPolicy).filter_by(
        specialty_id=specialty_id, product_id=product_id,
    ).first()
    if not policy:
        policy = SpecialtyVersionPolicy(specialty_id=specialty_id, product_id=product_id)
        db.add(policy)

    if req.force_min_version is not None:
        policy.force_min_version = req.force_min_version
    if req.force_max_version is not None:
        policy.force_max_version = req.force_max_version
    if req.policy_message is not None:
        policy.policy_message = req.policy_message

    _log_action(
        db, admin.id, "update_policy", "specialty", specialty_id,
        {"product_id": product_id, **req.model_dump()}, get_client_ip(request),
    )
    db.commit()
    return SuccessResponse()


# ---------- Releases ----------

@router.get("/releases")
async def list_releases(admin: User = Depends(get_current_admin)):
    files = list_release_files()
    return {
        "files": [
            {"key": f.get("Key"), "size": f.get("Size"), "last_modified": f.get("LastModified")}
            for f in files
        ]
    }


# ---------- Product management ----------

@router.get("/products")
async def list_all_products(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    products = db.query(Product).order_by(Product.sort_order).all()
    return {
        "products": [
            {
                "product_id": p.product_id, "name": p.name,
                "description": p.description, "is_active": p.is_active,
                "sort_order": p.sort_order,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in products
        ]
    }


@router.patch("/products/{product_id}", response_model=SuccessResponse)
async def update_product(
    product_id: str,
    req: UpdateProductRequest,
    request: Request,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")
    if req.name is not None:
        product.name = req.name
    if req.description is not None:
        product.description = req.description
    if req.is_active is not None:
        product.is_active = req.is_active
    if req.sort_order is not None:
        product.sort_order = req.sort_order

    _log_action(
        db, admin.id, "update_product", "product", product_id,
        req.model_dump(exclude_unset=True), get_client_ip(request),
    )
    db.commit()
    return SuccessResponse()


# ---------- Download logs ----------

@router.get("/logs/downloads")
async def list_download_logs(
    download_type: str = Query(""),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(DownloadLog)
    if download_type:
        query = query.filter(DownloadLog.download_type == download_type)
    total = query.count()
    items = query.order_by(DownloadLog.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total, "page": page, "size": size,
        "items": [
            {
                "id": dl.id, "user_id": dl.user_id,
                "download_type": dl.download_type, "resource_id": dl.resource_id,
                "platform": dl.platform, "completed": dl.completed,
                "created_at": dl.created_at.isoformat() if dl.created_at else None,
            }
            for dl in items
        ],
    }


# ---------- Security ----------

@router.get("/security/limits")
async def list_security_limits(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(SecurityLimit).filter(SecurityLimit.fail_count > 0)
    total = query.count()
    items = query.order_by(SecurityLimit.updated_at.desc()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total, "page": page, "size": size,
        "items": [
            {
                "limit_type": sl.limit_type, "identifier": sl.identifier,
                "fail_count": sl.fail_count,
                "locked_until": sl.locked_until.isoformat() if sl.locked_until else None,
                "updated_at": sl.updated_at.isoformat() if sl.updated_at else None,
            }
            for sl in items
        ],
    }


@router.post("/security/unlock", response_model=SuccessResponse)
async def unlock_security(
    req: UnlockSecurityRequest,
    request: Request,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    record = db.query(SecurityLimit).filter_by(
        limit_type=req.limit_type, identifier=req.identifier,
    ).first()
    if record:
        record.fail_count = 0
        record.locked_until = None
        _log_action(
            db, admin.id, "unlock_security", "security", req.identifier,
            {"limit_type": req.limit_type}, get_client_ip(request),
        )
        db.commit()
    return SuccessResponse()


# ---------- Admin operation logs ----------

@router.get("/logs/admin")
async def list_admin_logs(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    query = db.query(AdminLog)
    total = query.count()
    items = query.order_by(AdminLog.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return {
        "total": total, "page": page, "size": size,
        "items": [
            {
                "id": al.id, "admin_user_id": al.admin_user_id,
                "action_type": al.action_type, "target_type": al.target_type,
                "target_id": al.target_id, "detail": al.detail,
                "client_ip": al.client_ip,
                "created_at": al.created_at.isoformat() if al.created_at else None,
            }
            for al in items
        ],
    }
