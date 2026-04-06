"""
Database-backed rate limiting using the security_limits table.
"""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.security_limit import SecurityLimit


def check_rate_limit(
    db: Session,
    limit_type: str,
    identifier: str,
    max_count: int,
    window_seconds: int | None,
    lock_seconds: int | None = None,
) -> tuple[bool, datetime | None]:
    """
    Check if a rate limit has been exceeded.

    Returns (is_allowed, locked_until).
    If is_allowed is False, locked_until is when the lock expires (or None for permanent locks).
    window_seconds=None means cumulative (never auto-reset).
    """
    now = datetime.utcnow()
    record = (
        db.query(SecurityLimit)
        .filter_by(limit_type=limit_type, identifier=identifier)
        .first()
    )

    if record and record.locked_until and record.locked_until > now:
        return False, record.locked_until

    if record and record.last_fail_at and window_seconds:
        window_start = now - timedelta(seconds=window_seconds)
        if record.last_fail_at < window_start:
            record.fail_count = 0

    return True, None


def record_failure(
    db: Session,
    limit_type: str,
    identifier: str,
    max_count: int,
    lock_seconds: int | None = None,
) -> tuple[int, datetime | None]:
    """
    Record a failed attempt. Lock if threshold exceeded.

    Returns (current_fail_count, locked_until_or_None).
    """
    now = datetime.utcnow()
    record = (
        db.query(SecurityLimit)
        .filter_by(limit_type=limit_type, identifier=identifier)
        .first()
    )

    if not record:
        record = SecurityLimit(
            limit_type=limit_type,
            identifier=identifier,
            fail_count=1,
            last_fail_at=now,
        )
        db.add(record)
    else:
        record.fail_count += 1
        record.last_fail_at = now

    locked_until = None
    if record.fail_count >= max_count:
        if lock_seconds is not None:
            locked_until = now + timedelta(seconds=lock_seconds)
            record.locked_until = locked_until
        else:
            record.locked_until = datetime(2099, 12, 31)
            locked_until = record.locked_until

    db.commit()
    return record.fail_count, locked_until


def clear_failures(db: Session, limit_type: str, identifier: str) -> None:
    """Clear failure count after a successful action."""
    record = (
        db.query(SecurityLimit)
        .filter_by(limit_type=limit_type, identifier=identifier)
        .first()
    )
    if record:
        record.fail_count = 0
        record.locked_until = None
        record.last_fail_at = None
        db.commit()
