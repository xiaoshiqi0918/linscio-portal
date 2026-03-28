from pydantic import BaseModel


class CheckUpdateRequest(BaseModel):
    product_id: str
    platform: str
    software_version: str
    specialties: dict[str, str] | None = None


class SpecialtyUpdateInfo(BaseModel):
    id: str
    latest_version: str
    has_update: bool
    size_mb: float | None = None
    full_size_mb: float | None = None
    changelog: list[str] = []
    force_update: bool = False
    force_message: str | None = None


class CheckUpdateResponse(BaseModel):
    base_valid: bool
    has_software_update: bool = False
    latest_version: str | None = None
    download_url: str | None = None
    specialty_updates: list[SpecialtyUpdateInfo] = []
