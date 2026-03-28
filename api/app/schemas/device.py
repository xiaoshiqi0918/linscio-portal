from pydantic import BaseModel


class DeviceChangeCodeRequest(BaseModel):
    product_id: str
    credential: str
    password: str
    new_fingerprint: str
    new_device_name: str | None = None


class DeviceChangeCodeResponse(BaseModel):
    success: bool = True
    code: str | None = None
    expires_in: int = 300


class DeviceVerifyRequest(BaseModel):
    product_id: str
    code: str


class DeviceVerifyResponse(BaseModel):
    success: bool = True
    new_device_name: str | None = None
    rebind_remaining: int | None = None
    deep_link: str | None = None
