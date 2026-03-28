import asyncio
import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from jinja2 import Template

from app.core.config import get_settings

logger = logging.getLogger(__name__)

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


def _send_sync(to: str, subject: str, html_body: str) -> None:
    settings = get_settings()
    msg = MIMEMultipart("alternative")
    msg["From"] = settings.SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=ctx) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)


async def send_email(to: str, subject: str, html_body: str) -> None:
    settings = get_settings()
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, _send_sync, to, subject, html_body)
        logger.info("Email sent to %s: %s", to, subject)
    except Exception:
        logger.exception("Failed to send email to %s", to)
        if settings.is_production:
            raise
        logger.warning("Email sending skipped in development mode")


async def send_verification_code(email: str, code: str, minutes: int = 10) -> None:
    html = Template(VERIFICATION_TEMPLATE).render(code=code, minutes=minutes)
    await send_email(email, "LinScio 邮箱验证码", html)


async def send_reset_password_link(email: str, token: str, minutes: int = 30) -> None:
    settings = get_settings()
    portal_base = "https://portal.linscio.com.cn"
    if not settings.is_production:
        portal_base = "http://localhost:5173"
    link = f"{portal_base}/reset-password?token={token}"
    html = Template(RESET_PASSWORD_TEMPLATE).render(link=link, minutes=minutes)
    await send_email(email, "LinScio 密码重置", html)


async def send_device_activation_notice(
    email: str, product: str, device_name: str, activated_at: str
) -> None:
    html = Template(DEVICE_ACTIVATION_TEMPLATE).render(
        product=product, device_name=device_name, activated_at=activated_at
    )
    await send_email(email, f"LinScio {product} 新设备激活通知", html)


async def send_expiry_reminder(
    email: str, product: str, expires_at: str, days: int
) -> None:
    html = Template(EXPIRY_REMINDER_TEMPLATE).render(
        product=product, expires_at=expires_at, days=days
    )
    await send_email(email, f"LinScio {product} 授权即将到期提醒", html)
