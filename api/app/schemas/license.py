from pydantic import BaseModel


class ActivateLicenseRequest(BaseModel):
    code: str
    device_fingerprint: str | None = None
    device_name: str | None = None


class ActivateLicenseResponse(BaseModel):
    success: bool = True
    license_type: str
    is_trial: bool = False
    new_expires_at: str | None = None
    days_added: int | None = None
    deep_link: str | None = None
    token_unchanged: bool | None = None
    specialty_ids: list[str] | None = None
    specialty_names: list[str] | None = None


class LicenseStatusRequest(BaseModel):
    product_id: str
    reported_specialties: dict[str, str] | None = None


class BaseStatus(BaseModel):
    valid: bool
    is_trial: bool
    expires_at: str | None
    days_remaining: int | None
    device_name: str | None
    rebind_remaining: int


class SpecialtyInfo(BaseModel):
    id: str
    name: str
    remote_version: str | None = None
    local_version: str | None = None
    purchased_at: str | None = None


class VersionPolicyInfo(BaseModel):
    specialty_id: str
    force_min_version: str | None = None
    force_max_version: str | None = None
    policy_message: str | None = None


class LicenseStatusResponse(BaseModel):
    base: BaseStatus
    specialties: list[SpecialtyInfo] = []
    version_policies: list[VersionPolicyInfo] = []


class ProductLicenseInfo(BaseModel):
    product_id: str
    product_name: str
    status: str  # valid | expired | trial | not_activated
    is_trial: bool = False
    expires_at: str | None = None
    days_remaining: int | None = None
    device_name: str | None = None
    rebind_remaining: int | None = None


class LicenseStatusAllResponse(BaseModel):
    licenses: list[ProductLicenseInfo]
