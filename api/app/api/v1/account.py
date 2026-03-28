import time
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user_by_session
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.models.user_license import UserLicense
from app.models.user_session import UserSession
from app.schemas.account import (
    ChangePasswordRequest,
    ChangePasswordResponse,
    ChangePhoneRequest,
    DeleteAccountRequest,
)
from app.schemas.common import SuccessResponse

router = APIRouter(prefix="/api/account", tags=["account"])


@router.post("/change-password", response_model=ChangePasswordResponse)
async def change_password(
    req: ChangePasswordRequest,
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
):
    if not verify_password(req.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="原密码错误")
    if len(req.new_password) < 8:
        raise HTTPException(status_code=400, detail="新密码长度不能少于 8 位")

    user.password_hash = hash_password(req.new_password)
    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.query(UserLicense).filter(UserLicense.user_id == user.id).update(
        {UserLicense.access_token: None}, synchronize_session=False,
    )
    db.commit()
    return ChangePasswordResponse()


@router.patch("/phone", response_model=SuccessResponse)
async def change_phone(
    req: ChangePhoneRequest,
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.phone == req.phone, User.id != user.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="该手机号已被其他账号使用")

    user.phone = req.phone
    db.commit()
    return SuccessResponse()


@router.delete("", response_model=SuccessResponse)
async def delete_account(
    req: DeleteAccountRequest,
    user: User = Depends(get_current_user_by_session),
    db: Session = Depends(get_db),
):
    if not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=400, detail="密码错误")

    user.is_active = 0
    user.email = f"{user.email}_deleted_{int(time.time())}"
    if user.phone:
        user.phone = f"{user.phone}_deleted_{int(time.time())}"

    db.query(UserSession).filter(UserSession.user_id == user.id).delete()
    db.query(UserLicense).filter(UserLicense.user_id == user.id).update(
        {UserLicense.access_token: None}, synchronize_session=False,
    )
    db.commit()
    return SuccessResponse()
