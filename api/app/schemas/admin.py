from pydantic import BaseModel


class StatsOverview(BaseModel):
    total_users: int = 0
    active_licenses: int = 0
    expiring_soon: int = 0
    monthly_downloads: int = 0
    monthly_bundle_downloads: int = 0
    monthly_specialty_downloads: int = 0
    download_success_rate: float = 0.0


class GenerateLicenseRequest(BaseModel):
    product_id: str
    license_type: str  # 'basic' | 'specialty'
    count: int = 1
    duration_months: int | None = None
    duration_days: int | None = None
    is_trial: bool = False
    specialty_ids: list[str] | None = None
    recipient_note: str | None = None


class GenerateLicenseResponse(BaseModel):
    success: bool = True
    codes: list[str] = []


class BanUserRequest(BaseModel):
    reason: str | None = None


class DeleteUserRequest(BaseModel):
    reason: str | None = None


class ForceRebindRequest(BaseModel):
    user_id: int
    product_id: str
    reason: str | None = None


class MigrationHandleRequest(BaseModel):
    action: str  # 'approve' | 'reject'
    reason: str | None = None


class UpdatePolicyRequest(BaseModel):
    force_min_version: str | None = None
    force_max_version: str | None = None
    policy_message: str | None = None


class UpdateProductRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: int | None = None
    sort_order: int | None = None


class UnlockSecurityRequest(BaseModel):
    limit_type: str
    identifier: str
