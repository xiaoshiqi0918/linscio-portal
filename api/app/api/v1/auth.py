import logging
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.config import get_settings
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
    ClientLoginRequest,
    ClientLoginResponse,
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


async def _register_send_verification_email(email: str, code: str) -> None:
    """Send after HTTP response so Nginx/proxy timeouts (502) are not hit by slow SMTP."""
    try:
        ok = await send_verification_code(email, code, minutes=10)
        if not ok:
            logger.error("register: verification email send failed for %s", email)
    except Exception:
        logger.exception("register: verification email error for %s", email)


# ---------- Register ----------

@router.post("/register", response_model=SuccessResponse)
async def register(
    req: RegisterRequest,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    ip = get_client_ip(request)

    allowed, locked = check_rate_limit(db, "register_ip", ip, 3, 60, 60)
    if not allowed:
        raise HTTPException(status_code=429, detail="请求过于频繁，请稍后再试")
    allowed, locked = check_rate_limit(db, "register_email", req.email, 1, 60, 60)
    if not allowed:
        raise HTTPException(status_code=429, detail="该邮箱验证码发送过于频繁")

    _validate_password(req.password)

    existing = db.query(User).filter(User.email == req.email).first()
    # 仅「已激活且邮箱已验证」视为完成注册；未验证账号可能因历史 SMTP 失败等已入库，允许再次注册以更新密码并重发验证码
    if existing and existing.is_active == 1 and existing.email_verified == 1:
        raise HTTPException(status_code=400, detail="该邮箱已注册")

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    deleted_pattern = f"{req.email}_deleted_%"
    recently_deleted = (
        db.query(User)
        .filter(User.email.like(deleted_pattern), User.is_active == 0, User.updated_at >= thirty_days_ago)
        .first()
    )
    if recently_deleted:
        raise HTTPException(status_code=400, detail="该邮箱在注销后 30 天内不可重新注册")

    try:
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
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="该邮箱已注册")
    except SQLAlchemyError:
        db.rollback()
        logger.exception("register: database error for %s", req.email)
        raise HTTPException(status_code=503, detail="服务暂时不可用，请稍后重试")

    record_failure(db, "register_ip", ip, 3, 60)
    record_failure(db, "register_email", req.email, 1, 60)

    settings = get_settings()
    if settings.is_production and (not settings.SMTP_USER or not settings.SMTP_PASSWORD):
        msg = "账号已创建，但服务器未配置发信邮箱（SMTP），无法发送验证码。请联系管理员。"
    else:
        background_tasks.add_task(_register_send_verification_email, req.email, code)
        if not settings.is_production:
            msg = f"[开发模式] 验证码: {code}（邮件在后台发送中）"
        else:
            msg = (
                "验证邮件正在后台发送，请查收邮箱并在 10 分钟内完成验证（含垃圾箱）。"
                "若迟迟未收到，请检查 SMTP 或稍后重试。"
            )
    return SuccessResponse(message=msg)


# ---------- Verify ----------

@router.post("/verify", response_model=SuccessResponse)
async def verify_email(req: VerifyRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    allowed, _ = check_rate_limit(db, "verify_ip", ip, 10, 3600, 3600)
    if not allowed:
        raise HTTPException(status_code=429, detail="验证尝试过于频繁")

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
        record_failure(db, "verify_ip", ip, 10, 3600)
        raise HTTPException(status_code=400, detail="验证码无效或已过期")

    record.is_used = 1
    user = db.query(User).filter(User.email == req.email).first()
    if user:
        user.email_verified = 1
    clear_failures(db, "verify_ip", ip)
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
    request: Request,
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
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
        sent = await send_reset_password_link(req.email, token)
        if not sent:
            logger.error("Reset-password email failed for %s (token already stored)", req.email)

    record_failure(db, "forgot_ip", ip, 10, 3600)
    record_failure(db, "forgot_email", req.email, 3, 3600)
    return SuccessResponse(message="重置链接已发送，30 分钟内有效")


# ---------- Reset password ----------

@router.post("/reset-password", response_model=SuccessResponse)
async def reset_password(req: ResetPasswordRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    allowed, _ = check_rate_limit(db, "reset_pw_ip", ip, 5, 3600, 3600)
    if not allowed:
        raise HTTPException(status_code=429, detail="重置密码尝试过于频繁")

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
        record_failure(db, "reset_pw_ip", ip, 5, 3600)
        raise HTTPException(status_code=400, detail="重置链接无效或已过期")

    user = db.query(User).filter(User.email == record.email, User.is_active == 1).first()
    if not user:
        raise HTTPException(status_code=400, detail="用户不存在")

    user.password_hash = hash_password(req.new_password)
    record.is_used = 1

    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.query(UserLicense).filter(UserLicense.user_id == user.id).update(
        {UserLicense.access_token: None, UserLicense.token_created_at: None},
        synchronize_session=False,
    )
    db.commit()
    return SuccessResponse()


# ---------- Activate by code (software client) ----------

@router.post("/activate-by-code", response_model=ActivateByCodeResponse)
async def activate_by_code(req: ActivateByCodeRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    allowed, _ = check_rate_limit(db, "activate_code_ip", ip, 10, 3600, 3600)
    if not allowed:
        raise HTTPException(status_code=429, detail="激活尝试过于频繁")

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
        record_failure(db, "activate_code_ip", ip, 10, 3600)
        raise HTTPException(status_code=400, detail="激活码无效或已过期")

    user = db.query(User).filter(User.id == ac.user_id, User.is_active == 1).first()
    if not user:
        raise HTTPException(status_code=403, detail="账号已被禁用")

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


# ---------- Client login (software client, email+password → access_token) ----------

@router.post("/client-login", response_model=ClientLoginResponse)
async def client_login(req: ClientLoginRequest, request: Request, db: Session = Depends(get_db)):
    ip = get_client_ip(request)
    allowed, _ = check_rate_limit(db, "client_login_ip", ip, 10, 3600, 3600)
    if not allowed:
        raise HTTPException(status_code=429, detail="登录尝试过于频繁，请 1 小时后再试")

    user = db.query(User).filter(User.email == req.email, User.is_active == 1).first()
    if not user or not verify_password(req.password, user.password_hash):
        record_failure(db, "client_login_ip", ip, 10, 3600)
        raise HTTPException(status_code=401, detail="邮箱或密码错误")

    if not user.email_verified:
        raise HTTPException(status_code=400, detail="邮箱未验证，请先在门户完成注册验证")

    clear_failures(db, "client_login_ip", ip)

    lic = (
        db.query(UserLicense)
        .filter(UserLicense.user_id == user.id, UserLicense.product_id == req.product_id)
        .first()
    )
    if not lic:
        raise HTTPException(status_code=403, detail="该账号尚未激活此产品授权，请先在门户激活授权码")

    now = datetime.utcnow()
    if not lic.access_token:
        lic.access_token = generate_token(32)
        lic.token_created_at = now
    if req.device_fingerprint:
        lic.device_fingerprint = req.device_fingerprint
    if req.device_name:
        lic.device_name = req.device_name
    db.commit()

    days_remaining = max(0, (lic.expires_at - now).days) if lic.expires_at > now else 0

    return ClientLoginResponse(
        access_token=lic.access_token,
        email=user.email,
        expires_at=lic.expires_at.isoformat() + "Z" if lic.expires_at else None,
        is_trial=bool(lic.is_trial),
        days_remaining=days_remaining,
    )
