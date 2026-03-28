import logging
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import and_

from app.core.database import SessionLocal
from app.models.activation_code import ActivationCode
from app.models.device_change_code import DeviceChangeCode
from app.models.email_verification_code import EmailVerificationCode
from app.models.user_license import UserLicense
from app.models.user_session import UserSession
from app.models.user import User

logger = logging.getLogger(__name__)
scheduler = BackgroundScheduler()


def cleanup_expired_records() -> None:
    """Daily cleanup at 04:00: remove expired codes, sessions, verification codes."""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        one_day_ago = now - timedelta(days=1)

        deleted = db.query(ActivationCode).filter(
            ActivationCode.created_at < one_day_ago
        ).delete()
        logger.info("Cleaned %d expired activation_codes", deleted)

        deleted = db.query(DeviceChangeCode).filter(
            DeviceChangeCode.created_at < one_day_ago
        ).delete()
        logger.info("Cleaned %d expired device_change_codes", deleted)

        deleted = db.query(UserSession).filter(
            UserSession.expires_at < now
        ).delete()
        logger.info("Cleaned %d expired user_sessions", deleted)

        deleted = db.query(EmailVerificationCode).filter(
            EmailVerificationCode.expires_at < one_day_ago
        ).delete()
        logger.info("Cleaned %d expired email_verification_codes", deleted)

        db.commit()
    except Exception:
        db.rollback()
        logger.exception("Error during cleanup_expired_records")
    finally:
        db.close()


def send_expiry_reminders() -> None:
    """Daily at 02:00: send email reminders 7 days before expiry."""
    from app.services.email import send_expiry_reminder
    import asyncio

    db = SessionLocal()
    try:
        now = datetime.utcnow()
        seven_days_later = now + timedelta(days=7)

        licenses = (
            db.query(UserLicense, User)
            .join(User, User.id == UserLicense.user_id)
            .filter(
                and_(
                    UserLicense.expires_at.between(now, seven_days_later),
                    User.is_active == 1,
                    User.email_notified_7d.is_(None),
                )
            )
            .limit(20)
            .all()
        )

        loop = asyncio.new_event_loop()
        for lic, user in licenses:
            days_remaining = (lic.expires_at - now).days
            try:
                loop.run_until_complete(
                    send_expiry_reminder(
                        email=user.email,
                        product=lic.product_id,
                        expires_at=lic.expires_at.isoformat(),
                        days=days_remaining,
                    )
                )
                user.email_notified_7d = now
                db.commit()
            except Exception:
                logger.exception("Failed to send expiry reminder to %s", user.email)
        loop.close()
    except Exception:
        logger.exception("Error during send_expiry_reminders")
    finally:
        db.close()


def init_scheduler() -> None:
    scheduler.add_job(
        send_expiry_reminders,
        trigger="cron", hour=2, minute=0,
        id="expiry_reminder",
        replace_existing=True,
    )
    scheduler.add_job(
        cleanup_expired_records,
        trigger="cron", hour=4, minute=0,
        id="cleanup",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("APScheduler started with 2 jobs")


def shutdown_scheduler() -> None:
    scheduler.shutdown(wait=False)
