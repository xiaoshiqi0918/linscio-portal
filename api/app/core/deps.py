"""FastAPI dependency injectors for auth and admin verification."""
import logging
from datetime import datetime

from fastapi import Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models.user import User
from app.models.user_license import UserLicense
from app.models.user_session import UserSession

logger = logging.getLogger(__name__)


def _expand_ip_variants(ip: str) -> set[str]:
    p = (ip or "").strip()
    if not p:
        return set()
    out = {p}
    low = p.lower()
    if low.startswith("::ffff:"):
        out.add(p[7:].strip())
    return out


def _admin_client_ip_allowed(client_ip: str, allowed: list[str]) -> bool:
    cv = _expand_ip_variants(client_ip)
    for a in allowed:
        if cv & _expand_ip_variants(a):
            return True
    return False


def _extract_bearer(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return authorization[7:]


async def get_current_user_by_session(
    authorization: str | None = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> User:
    """Validate session_token (portal/admin browser sessions)."""
    token = _extract_bearer(authorization)
    session = (
        db.query(UserSession)
        .filter(UserSession.session_token == token, UserSession.expires_at > datetime.utcnow())
        .first()
    )
    if not session:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    user = db.query(User).filter(User.id == session.user_id, User.is_active == 1).first()
    if not user:
        raise HTTPException(status_code=401, detail="Account is disabled")
    return user


async def get_current_admin(
    request: Request,
    user: User = Depends(get_current_user_by_session),
) -> User:
    """Ensure current user is admin. In production, also verify IP whitelist."""
    if user.is_admin != 1:
        raise HTTPException(status_code=403, detail="Admin access required")
    settings = get_settings()
    if settings.is_production and settings.admin_ips_list:
        client_ip = get_client_ip(request)
        if not _admin_client_ip_allowed(client_ip, settings.admin_ips_list):
            logger.warning(
                "Admin IP rejected: client_ip=%r X-Forwarded-For=%r X-Real-IP=%r allowed=%r",
                client_ip,
                request.headers.get("X-Forwarded-For"),
                request.headers.get("X-Real-IP"),
                settings.admin_ips_list,
            )
            raise HTTPException(status_code=403, detail="IP not allowed for admin access")
    return user


async def get_license_by_access_token(
    authorization: str | None = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
) -> UserLicense:
    """Validate access_token (software client calls)."""
    token = _extract_bearer(authorization)
    lic = db.query(UserLicense).filter(UserLicense.access_token == token).first()
    if not lic:
        raise HTTPException(status_code=401, detail="Invalid access token")
    user = db.query(User).filter(User.id == lic.user_id, User.is_active == 1).first()
    if not user:
        raise HTTPException(status_code=401, detail="Account is disabled")
    lic.last_seen_at = datetime.utcnow()
    db.commit()
    return lic


def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Real-IP") or request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
