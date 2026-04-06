import json
import logging

from qcloud_cos import CosConfig, CosS3Client

from app.core.config import get_settings

logger = logging.getLogger(__name__)

_client: CosS3Client | None = None


def _get_client() -> CosS3Client:
    global _client
    if _client is None:
        settings = get_settings()
        config = CosConfig(
            Region=settings.COS_REGION,
            SecretId=settings.COS_SECRET_ID,
            SecretKey=settings.COS_SECRET_KEY,
        )
        _client = CosS3Client(config)
    return _client


def read_manifest() -> dict:
    """Read manifest.json from specialties bucket (no caching, always fresh)."""
    settings = get_settings()
    client = _get_client()
    try:
        response = client.get_object(
            Bucket=settings.COS_BUCKET_SPECIALTIES,
            Key="manifest.json",
        )
        body = response["Body"].get_raw_stream().read()
        return json.loads(body)
    except Exception:
        logger.exception("Failed to read manifest.json from COS")
        return {"specialties": []}


def generate_presigned_download_url(key: str, expires: int = 3600) -> str:
    """Generate a pre-signed URL for downloading a file from the releases bucket."""
    settings = get_settings()
    client = _get_client()
    return client.get_presigned_download_url(
        Bucket=settings.COS_BUCKET_RELEASES,
        Key=key,
        Expired=expires,
    )


def list_release_files(prefix: str = "releases/") -> list[dict]:
    """List files under releases bucket."""
    settings = get_settings()
    client = _get_client()
    try:
        response = client.list_objects(
            Bucket=settings.COS_BUCKET_RELEASES,
            Prefix=prefix,
            MaxKeys=1000,
        )
        return response.get("Contents", [])
    except Exception:
        logger.exception("Failed to list release files")
        return []


def upload_backup(local_path: str, cos_key: str) -> bool:
    """Upload a backup file to specialties bucket under /backups/."""
    settings = get_settings()
    client = _get_client()
    try:
        client.upload_file(
            Bucket=settings.COS_BUCKET_SPECIALTIES,
            Key=cos_key,
            LocalFilePath=local_path,
        )
        return True
    except Exception:
        logger.exception("Failed to upload backup %s", cos_key)
        return False
