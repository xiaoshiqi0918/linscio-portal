from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


class VerifyRequest(BaseModel):
    email: EmailStr
    code: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    session_token: str
    expires_in: int = 86400
    is_admin: bool = False


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str


class ActivateByCodeRequest(BaseModel):
    activation_code: str
    device_fingerprint: str


class ActivateByCodeResponse(BaseModel):
    success: bool = True
    access_token: str
    expires_at: str
