from pydantic import BaseModel


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class ChangePasswordResponse(BaseModel):
    success: bool = True
    access_token_revoked: bool = True


class ChangePhoneRequest(BaseModel):
    phone: str


class DeleteAccountRequest(BaseModel):
    password: str
