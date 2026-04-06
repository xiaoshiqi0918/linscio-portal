from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_client_ip, get_current_user_by_session
from app.core.security import generate_numeric_code, generate_short_code, generate_token, verify_password
from app.middleware.rate_limit import check_rate_limit, record_failure
from app.models.activation_code import ActivationCode
from app.models.device_change_code import DeviceChangeCode
from app.models.device_rebind_log import DeviceRebindLog
from app.models.user import User
from app.models.user_license import UserLicense
from app.schemas.device import (
    DeviceChangeCodeRequest,
    DeviceChangeCodeResponse,
    DeviceVerifyRequest,
    DeviceVerifyResponse,
)
from app.services.email import send_device_activation_notice

router = APIRouter(prefix="/api/device", tags=["device"])


# ---------- Request change code (software client, no token) ----------

@router.post("/change-code/request", response_model=DeviceChangeCodeResponse)
async def request_change_code(
    req: DeviceChangeCodeRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    ip = get_client_ip(request)
    allowed, _ = check_rate_limit(db, "device_change_user", req.credential, 5, 1800, 1800)
    if not allowed:
        raise HTTPException(status_code=429, detail="请求过于频繁，请 30 分钟后再试")

    user = db.query(User).filter(User.email == req.credential, User.is_active == 1).first()
    if not user or not verify_password(req.password, user.password_hash):
        record_failure(db, "device_change_user", req.credential, 5, 1800)
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    lic = (
        db.query(UserLicense)
        .filter(UserLicense.user_id == user.id, UserLicense.product_id == req.product_id)
        .first()
    )
    if not lic:
        raise HTTPException(status_code=400, detail="no_license_found")
    if lic.rebind_count >= 2:
        raise HTTPException(status_code=400, detail="rebind_limit_exceeded")

    code = generate_numeric_code(6)
    now = datetime.utcnow()

    db.add(DeviceChangeCode(
        user_id=user.id,
        product_id=req.product_id,
        code=code,
        new_fingerprint=req.new_fingerprint,
        new_device_name=req.new_device_name,
        expires_at=now + timedelta(minutes=5),
    ))
    db.commit()

    return DeviceChangeCodeResponse(code=code, expires_in=300)


# ---------- Verify change code (portal, session_token) ----------

@router.post("/change-code/verify", response_model=DeviceVerifyResponse)
async def verify_change_code(
    req: DeviceVerifyRequest,
    request: Request,
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
):
    allowed, _ = check_rate_limit(db, "device_verify_user", str(user.id), 5, 1800, 1800)
    if not allowed:
        raise HTTPException(status_code=429, detail="验证过于频繁，请 30 分钟后再试")

    dcc = (
        db.query(DeviceChangeCode)
        .filter(
            DeviceChangeCode.user_id == user.id,
            DeviceChangeCode.product_id == req.product_id,
            DeviceChangeCode.code == req.code,
            DeviceChangeCode.is_used == 0,
            DeviceChangeCode.expires_at > datetime.utcnow(),
        )
        .first()
    )
    if not dcc:
        record_failure(db, "device_verify_user", str(user.id), 5, 1800)
        raise HTTPException(status_code=400, detail="code_invalid")

    lic = (
        db.query(UserLicense)
        .filter(UserLicense.user_id == user.id, UserLicense.product_id == req.product_id)
        .first()
    )
    if not lic:
        raise HTTPException(status_code=400, detail="no_license_found")

    old_fp = lic.device_fingerprint
    old_name = lic.device_name

    lic.access_token = None
    lic.token_created_at = None
    lic.device_fingerprint = dcc.new_fingerprint
    lic.device_name = dcc.new_device_name
    lic.rebind_count += 1

    dcc.is_used = 1

    db.add(DeviceRebindLog(
        user_id=user.id,
        product_id=req.product_id,
        old_fingerprint=old_fp,
        new_fingerprint=dcc.new_fingerprint,
        old_device_name=old_name,
        new_device_name=dcc.new_device_name,
        rebind_type="self_service",
        operator_ip=get_client_ip(request),
    ))

    now = datetime.utcnow()
    db.query(ActivationCode).filter(
        ActivationCode.user_id == user.id,
        ActivationCode.product_id == req.product_id,
        ActivationCode.is_used == 0,
    ).update({ActivationCode.is_used: 1}, synchronize_session=False)

    ac_code = generate_short_code(8)
    db.add(ActivationCode(
        code=ac_code, user_id=user.id, product_id=req.product_id,
        device_fingerprint=dcc.new_fingerprint,
        expires_at=now + timedelta(minutes=5),
    ))
    db.commit()

    await send_device_activation_notice(
        email=user.email,
        product=req.product_id,
        device_name=dcc.new_device_name or "未知设备",
        activated_at=now.strftime("%Y-%m-%d %H:%M"),
    )

    return DeviceVerifyResponse(
        new_device_name=dcc.new_device_name,
        rebind_remaining=max(0, 2 - lic.rebind_count),
        deep_link=f"linscio://auth?activation_code={ac_code}",
    )
