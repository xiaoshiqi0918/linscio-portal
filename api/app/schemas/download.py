from pydantic import BaseModel


class SoftwareDownloadRequest(BaseModel):
    product_id: str
    platform: str


class SoftwareDownloadResponse(BaseModel):
    success: bool = True
    download_url: str | None = None
    filename: str | None = None
    size_mb: float | None = None
    download_log_id: int | None = None


class SpecialtyDownloadRequest(BaseModel):
    product_id: str
    specialty_id: str
    version: str
    from_version: str | None = None
    resume_offset: int = 0


class SpecialtyDownloadResponse(BaseModel):
    success: bool = True
    package_type: str = "full"  # 'full' | 'patch'
    download_url: str | None = None
    filename: str | None = None
    size_mb: float | None = None
    md5: str | None = None
    download_log_id: int | None = None
    expires_in: int = 7200


class BundleDownloadRequest(BaseModel):
    product_id: str
    bundle_id: str
    platform: str


class BundleDownloadResponse(BaseModel):
    success: bool = True
    download_url: str | None = None
    filename: str | None = None
    size_bytes: int = 0
    sha256: str = ""
    download_log_id: int | None = None


class DownloadCompleteRequest(BaseModel):
    download_log_id: int
