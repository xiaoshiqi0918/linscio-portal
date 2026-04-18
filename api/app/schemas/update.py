from pydantic import BaseModel


class CheckUpdateRequest(BaseModel):
    product_id: str
    platform: str
    software_version: str
    specialties: dict[str, str] | None = None
    drawing_packs: dict[str, str] | None = None
    bundles: dict[str, str] | None = None


class SpecialtyUpdateInfo(BaseModel):
    id: str
    latest_version: str
    has_update: bool
    category: str = "specialty"
    size_mb: float | None = None
    full_size_mb: float | None = None
    changelog: list[str] = []
    force_update: bool = False
    force_message: str | None = None


class BundleUpdateInfo(BaseModel):
    id: str
    name: str = ""
    latest_version: str
    has_update: bool
    platform: str | None = None
    size_bytes: int = 0
    sha256: str = ""
    download_url: str | None = None
    min_client_version: str | None = None


class CheckUpdateResponse(BaseModel):
    base_valid: bool
    has_software_update: bool = False
    latest_version: str | None = None
    download_url: str | None = None
    update_download_url: str | None = None
    update_filename: str | None = None
    update_size_bytes: int = 0
    update_sha256: str = ""
    min_client_version: str | None = None
    platform_status: str | None = None
    release_notes: str | None = None
    specialty_updates: list[SpecialtyUpdateInfo] = []
    drawing_pack_updates: list[SpecialtyUpdateInfo] = []
    bundle_updates: list[BundleUpdateInfo] = []
