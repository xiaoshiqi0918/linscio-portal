import asyncio
import logging
import smtplib
import ssl
import time
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Template

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# 避免 SMTP 网络不可达时无限阻塞，导致 Nginx proxy_read_timeout 返回 502
SMTP_SOCKET_TIMEOUT_SEC = 25

_email_send_times: list[float] = []
_email_lock = threading.Lock()
MAX_EMAILS_PER_MINUTE = 20

VERIFICATION_TEMPLATE = """\
<html><body>
<h2>LinScio 邮箱验证</h2>
<p>您的验证码是：<strong>{{ code }}</strong></p>
<p>此验证码 {{ minutes }} 分钟内有效。</p>
<p>如果您未请求此验证，请忽略此邮件。</p>
<hr><p style="color:#999">LinScio · linscio.com.cn</p>
</body></html>
"""

RESET_PASSWORD_TEMPLATE = """\
<html><body>
<h2>LinScio 密码重置</h2>
<p>点击以下链接重置密码（{{ minutes }} 分钟内有效）：</p>
<p><a href="{{ link }}">{{ link }}</a></p>
<p>如果您未请求此操作，请忽略此邮件。</p>
<hr><p style="color:#999">LinScio · linscio.com.cn</p>
</body></html>
"""

DEVICE_ACTIVATION_TEMPLATE = """\
<html><body>
<h2>LinScio 新设备激活通知</h2>
<p>您的 {{ product }} 授权已在新设备上激活：</p>
<ul>
  <li>设备名称：{{ device_name }}</li>
  <li>激活时间：{{ activated_at }}</li>
</ul>
<p>如果这不是您的操作，请立即修改密码。</p>
<hr><p style="color:#999">LinScio · linscio.com.cn</p>
</body></html>
"""

EXPIRY_REMINDER_TEMPLATE = """\
<html><body>
<h2>LinScio 授权即将到期</h2>
<p>您的 {{ product }} 授权将于 {{ expires_at }} 到期，剩余 {{ days }} 天。</p>
<p>请联系我们续费以继续使用完整功能。</p>
<p>联系邮箱：linscio@163.com</p>
<hr><p style="color:#999">LinScio · linscio.com.cn</p>
</body></html>
"""

SPECIALTY_UPDATE_TEMPLATE = """\
<html><body>
<h2>LinScio 学科包更新通知</h2>
<p>{{ product }} 的「{{ specialty_name }}」学科包有新版本：</p>
<ul>
  <li>最新版本：{{ version }}</li>
  <li>更新内容：{{ changelog }}</li>
</ul>
<p>请打开软件检查更新以获取最新学科包。</p>
<hr><p style="color:#999">LinScio · linscio.com.cn</p>
</body></html>
"""

BACKUP_RESULT_TEMPLATE = """\
<html><body>
<h2>LinScio 数据库备份{{ '成功' if success else '失败' }}</h2>
<p>备份时间：{{ timestamp }}</p>
<p>备份文件：{{ filename }}</p>
{% if not success %}
<p style="color:red;font-weight:bold">备份失败，请尽快人工介入检查！</p>
<p>错误信息：{{ error_message }}</p>
{% else %}
<p>备份已成功上传至 COS 存储。</p>
{% endif %}
<hr><p style="color:#999">LinScio · linscio.com.cn</p>
</body></html>
"""


def _wait_for_rate_limit() -> None:
    """Block until we're within the 20 emails/minute limit."""
    with _email_lock:
        now = time.time()
        cutoff = now - 60
        _email_send_times[:] = [t for t in _email_send_times if t > cutoff]
        if len(_email_send_times) >= MAX_EMAILS_PER_MINUTE:
            wait = _email_send_times[0] - cutoff + 0.1
            time.sleep(wait)
        _email_send_times.append(time.time())


def _send_sync(to: str, subject: str, html_body: str) -> None:
    _wait_for_rate_limit()
    settings = get_settings()
    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        settings.SMTP_HOST,
        settings.SMTP_PORT,
        context=ctx,
        timeout=SMTP_SOCKET_TIMEOUT_SEC,
    ) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)


async def send_email(to: str, subject: str, html_body: str) -> bool:
    settings = get_settings()
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        logger.warning("SMTP_USER/SMTP_PASSWORD not set; skip sending to %s", to)
        return False
    loop = asyncio.get_running_loop()
    try:
        await loop.run_in_executor(None, _send_sync, to, subject, html_body)
        logger.info("Email sent to %s: %s", to, subject)
        return True
    except Exception:
        logger.exception("Failed to send email to %s", to)
        return False


async def send_verification_code(email: str, code: str, minutes: int = 10) -> bool:
    settings = get_settings()
    if not settings.is_production:
        logger.info("=== DEV MODE === Verification code for %s: %s", email, code)
    html = Template(VERIFICATION_TEMPLATE).render(code=code, minutes=minutes)
    return await send_email(email, "LinScio 邮箱验证码", html)


async def send_reset_password_link(email: str, token: str, minutes: int = 30) -> bool:
    settings = get_settings()
    portal_base = "https://portal.linscio.com.cn"
    if not settings.is_production:
        portal_base = "http://localhost:5173"
    link = f"{portal_base}/reset-password?token={token}"
    html = Template(RESET_PASSWORD_TEMPLATE).render(link=link, minutes=minutes)
    return await send_email(email, "LinScio 密码重置", html)


async def send_device_activation_notice(
    email: str, product: str, device_name: str, activated_at: str
) -> bool:
    html = Template(DEVICE_ACTIVATION_TEMPLATE).render(
        product=product, device_name=device_name, activated_at=activated_at
    )
    return await send_email(email, f"LinScio {product} 新设备激活通知", html)


async def send_expiry_reminder(
    email: str, product: str, expires_at: str, days: int
) -> bool:
    html = Template(EXPIRY_REMINDER_TEMPLATE).render(
        product=product, expires_at=expires_at, days=days
    )
    return await send_email(email, f"LinScio {product} 授权即将到期提醒", html)


async def send_specialty_update_notice(
    email: str, product: str, specialty_name: str, version: str, changelog: str
) -> bool:
    html = Template(SPECIALTY_UPDATE_TEMPLATE).render(
        product=product, specialty_name=specialty_name,
        version=version, changelog=changelog,
    )
    return await send_email(email, f"LinScio {product}「{specialty_name}」学科包更新通知", html)


async def send_backup_result(
    success: bool, filename: str, timestamp: str, error_message: str = ""
) -> bool:
    settings = get_settings()
    html = Template(BACKUP_RESULT_TEMPLATE).render(
        success=success, filename=filename,
        timestamp=timestamp, error_message=error_message,
    )
    status = "成功" if success else "失败"
    return await send_email(settings.SMTP_USER, f"LinScio 数据库备份{status} - {timestamp}", html)
