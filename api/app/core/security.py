import hashlib
import os
import time

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def generate_token(nbytes: int = 32) -> str:
    """Generate a cryptographically secure hex token."""
    return os.urandom(nbytes).hex()


def generate_numeric_code(length: int = 6) -> str:
    """Generate a random numeric code (e.g. '483921')."""
    return "".join([str(int.from_bytes(os.urandom(1)) % 10) for _ in range(length)])


def generate_short_code(length: int = 8) -> str:
    """Generate a short alphanumeric code (e.g. 'ABCD1234')."""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "".join(chars[int.from_bytes(os.urandom(1)) % len(chars)] for _ in range(length))


def generate_cdn_sign_url(
    path: str, secret: str, domain: str, expire_seconds: int = 7200
) -> str:
    """Generate a Tencent Cloud CDN TypeC signed URL."""
    timestamp = int(time.time()) + expire_seconds
    sign_str = secret + path + str(timestamp)
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    return f"https://{domain}{path}?sign={sign}&t={timestamp}"
