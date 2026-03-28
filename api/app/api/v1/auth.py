import re
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_client_ip, get_current_user_by_session
from app.core.security import (
    generate_token,
    generate_numeric_code,
    hash_password,
    verify_password,
)
from app.middleware.rate_limit import check_rate_limit, clear_failures, record_failure
from app.models.activation_code import ActivationCode
from app.models.email_verification_code import EmailVerificationCode
from app.models.user import User
from app.models.user_license import UserLicense
from app.models.user_session import UserSession
from app.schemas.auth import (
    ActivateByCodeRequest,
    ActivateByCodeResponse,
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    ResetPasswordRequest,
    VerifyRequest,
)
from app.schemas.common import ErrorResponse, SuccessResponse
from app.services.email import send_reset_password_link, send_verification_code

router = APIRouter(prefix="/api/auth", tags=["auth"])

PASSWORD_MIN_LEN = 8
PASSWORD_PATTERN = re.compile(r"^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?`~]{8,64}$")


def _validate_password(pw: str) -> None:
    if len(pw) < PASSWORD_MIN_LEN or not PASSWORD_PATTERN.match(pw):
        raise HTTPException(status_code=400, detail="密码长度 8-64 位，支持字母、数字和常用符号")


# ---------- Register ----------

@router.post("/register", response_model=SuccessResponse)
async def register(req: RegisterRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)

    allowed, locked = check_rate_limit(db, "register_ip", ip, 3, 60, 60)
    if not allowed:
        raise HTTPException(status_code=429, detail="请求过于频繁，请稍后再试")
    allowed, locked = check_rate_limit(db, "register_email", req.email, 1, 60, 60)
    if not allowed:
        raise HTTPException(status_code=429, detail="该邮箱验证码发送过于频繁")

    _validate_password(req.password)

    existing = db.query(User).filter(User.email == req.email).first()
    if existing and existing.is_active == 1:
        raise HTTPException(status_code=400, detail="该邮箱已注册")

    if not existing:
        user = User(email=req.email, password_hash=hash_password(req.password))
        db.add(user)
        db.commit()
    else:
        existing.password_hash = hash_password(req.password)
        db.commit()

    code = generate_numeric_code(6)
    expires = datetime.utcnow() + timedelta(minutes=10)
    db.add(EmailVerificationCode(email=req.email, code=code, purpose="register", expires_at=expires))
    db.commit()

    record_failure(db, "register_ip", ip, 3, 60)
    record_failure(db, "register_email", req.email, 1, 60)

    await send_verification_code(req.email, code, minutes=10)
    return SuccessResponse(message="验证邮件已发送，请在 10 分钟内完成验证")


# ---------- Verify ----------

@router.post("/verify", response_model=SuccessResponse)
async def verify_email(req: VerifyRequest, db: Session = Depends(get_db)):
    record = (
        db.query(EmailVerificationCode)
        .filter(
            EmailVerificationCode.email == req.email,
            EmailVerificationCode.code == req.code,
            EmailVerificationCode.purpose == "register",
            EmailVerificationCode.is_used == 0,
            EmailVerificationCode.expires_at > datetime.utcnow(),
        )
        .order_by(EmailVerificationCode.created_at.desc())
        .first()
    )
    if not record:
        raise HTTPException(status_code=400, detail="验证码无效或已过期")

    record.is_used = 1
    user = db.query(User).filter(User.email == req.email).first()
    if user:
        user.email_verified = 1
    db.commit()
    return SuccessResponse()


# ---------- Login ----------

@router.post("/login", response_model=LoginResponse)
async def login(req: LoginRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    allowed, locked = check_rate_limit(db, "login_ip", ip, 10, 3600, 3600)
    if not allowed:
        raise HTTPException(status_code=429, detail="登录尝试过于频繁，请 1 小时后再试")

    user = db.query(User).filter(User.email == req.email, User.is_active == 1).first()
    if not user or not verify_password(req.password, user.password_hash):
        record_failure(db, "login_ip", ip, 10, 3600)
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    clear_failures(db, "login_ip", ip)

    now = datetime.utcnow()
    db.query(UserSession).filter(
        UserSession.user_id == user.id, UserSession.expires_at < now
    ).delete()

    active_sessions = db.query(UserSession).filter(UserSession.user_id == user.id).count()
    if active_sessions >= 10:
        oldest = (
            db.query(UserSession)
            .filter(UserSession.user_id == user.id)
            .order_by(UserSession.created_at.asc())
            .first()
        )
        if oldest:
            db.delete(oldest)

    token = generate_token(32)
    session = UserSession(
        user_id=user.id,
        session_token=token,
        expires_at=now + timedelta(hours=24),
        client_ip=ip,
        user_agent=request.headers.get("User-Agent"),
    )
    db.add(session)
    db.commit()

    return LoginResponse(session_token=token, is_admin=bool(user.is_admin))


# ---------- Logout ----------

@router.post("/logout", response_model=SuccessResponse)
async def logout(
    user: User = Depends(get_current_user_by_session),
    authorization: str | None = None,
    db: Session = Depends(get_db),
    request: Request = None,
):
    raw = request.headers.get("Authorization", "")
    token = raw.replace("Bearer ", "") if raw.startswith("Bearer ") else ""
    db.query(UserSession).filter(UserSession.session_token == token).delete()
    db.commit()
    return SuccessResponse()


# ---------- Forgot password ----------

@router.post("/forgot-password", response_model=SuccessResponse)
async def forgot_password(req: ForgotPasswordRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    allowed, _ = check_rate_limit(db, "forgot_ip", ip, 10, 3600, 3600)
    if not allowed:
        raise HTTPException(status_code=429, detail="请求过于频繁")
    allowed, _ = check_rate_limit(db, "forgot_email", req.email, 3, 3600, 3600)
    if not allowed:
        raise HTTPException(status_code=429, detail="该邮箱重置请求过于频繁")

    user = db.query(User).filter(User.email == req.email, User.is_active == 1).first()
    if user:
        token = generate_token(16)  # 32 hex chars
        expires = datetime.utcnow() + timedelta(minutes=30)
        db.add(EmailVerificationCode(
            email=req.email, code=token, purpose="reset_password", expires_at=expires,
        ))
        db.commit()
        await send_reset_password_link(req.email, token)

    record_failure(db, "forgot_ip", ip, 10, 3600)
    record_failure(db, "forgot_email", req.email, 3, 3600)
    return SuccessResponse(message="重置链接已发送，30 分钟内有效")


# ---------- Reset password ----------

@router.post("/reset-password", response_model=SuccessResponse)
async def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    _validate_password(req.new_password)

    record = (
        db.query(EmailVerificationCode)
        .filter(
            EmailVerificationCode.code == req.token,
            EmailVerificationCode.purpose == "reset_password",
            EmailVerificationCode.is_used == 0,
            EmailVerificationCode.expires_at > datetime.utcnow(),
        )
        .first()
    )
    if not record:
        raise HTTPException(status_code=400, detail="重置链接无效或已过期")

    user = db.query(User).filter(User.email == record.email, User.is_active == 1).first()
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")

    user.password_hash = hash_password(req.new_password)
    record.is_used = 1

    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.query(UserLicense).filter(UserLicense.user_id == user.id).update(
        {UserLicense.access_token: None}, synchronize_session=False
    )
    db.commit()
    return SuccessResponse()


# ---------- Activate by code (software client) ----------

@router.post("/activate-by-code", response_model=ActivateByCodeResponse)
async def activate_by_code(req: ActivateByCodeRequest, db: Session = Depends(get_db)):
    ac = (
        db.query(ActivationCode)
        .filter(
            ActivationCode.code == req.activation_code,
            ActivationCode.is_used == 0,
            ActivationCode.expires_at > datetime.utcnow(),
        )
        .first()
    )
    if not ac:
        raise HTTPException(status_code=400, detail="激活码无效或已过期")

    ac.is_used = 1

    lic = (
        db.query(UserLicense)
        .filter(UserLicense.user_id == ac.user_id, UserLicense.product_id == ac.product_id)
        .first()
    )
    if not lic:
        raise HTTPException(status_code=400, detail="授权记录不存在")

    access_token = generate_token(32)
    lic.access_token = access_token
    lic.token_created_at = datetime.utcnow()
    lic.device_fingerprint = req.device_fingerprint
    db.commit()

    return ActivateByCodeResponse(
        access_token=access_token,
        expires_at=lic.expires_at.isoformat() + "Z",
    )
