from functools import lru_cache
from urllib.parse import quote_plus

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "development"
    API_BASE_URL: str = "http://localhost:8000"

    # Database — set DATABASE_URL to override; leave empty to auto-build from DB_* fields
    DATABASE_URL: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "linscio_db"
    DB_USER: str = "linscio"
    DB_PASSWORD: str = ""

    # COS
    COS_SECRET_ID: str = ""
    COS_SECRET_KEY: str = ""
    COS_APPID: str = "1363203425"
    COS_BUCKET_RELEASES: str = "linscio-releases-1363203425"
    COS_BUCKET_SPECIALTIES: str = "linscio-specialties-1363203425"
    COS_REGION: str = "ap-shanghai"

    # CDN
    CDN_DOMAIN_RELEASES: str = "linscio-releases-1363203425.cos.ap-shanghai.myqcloud.com"
    CDN_DOMAIN_SPECIALTIES: str = "cdn.linscio.com.cn"
    CDN_AUTH_SECRET: str = ""

    # Email
    SMTP_HOST: str = "smtp.163.com"
    SMTP_PORT: int = 465
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    # Security
    SECRET_KEY: str = ""
    ADMIN_IPS: str = "127.0.0.1"

    # CORS
    CORS_ORIGINS: str = ""

    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        # quote user/password so @ : / ? # in passwords do not break the URL
        u = quote_plus(self.DB_USER, safe="")
        p = quote_plus(self.DB_PASSWORD, safe="")
        return (
            f"mysql+pymysql://{u}:{p}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            "?charset=utf8mb4"
        )

    @property
    def is_sqlite(self) -> bool:
        return self.database_url.startswith("sqlite")

    @property
    def cors_origins_list(self) -> list[str]:
        if not self.CORS_ORIGINS:
            return []
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    @property
    def admin_ips_list(self) -> list[str]:
        return [ip.strip() for ip in self.ADMIN_IPS.split(",") if ip.strip()]

    @property
    def is_production(self) -> bool:
        return self.ENV == "production"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
