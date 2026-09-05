from email.message import EmailMessage

import aiosmtplib

from app.core.config import SMTPSettings


class SmtpEmailSender:
    def __init__(self, settings: SMTPSettings) -> None:
        self._settings = settings

    async def send(
        self,
        *,
        to: str,
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        message = EmailMessage()

        message["From"] = f"{self._settings.from_name} <{self._settings.from_email}>"
        message["To"] = to
        message["Subject"] = subject

        # Fallback in case client doesn't render HTML content
        message.set_content(text)
        if html is not None:
            message.add_alternative(html, subtype="html")

        await aiosmtplib.send(
            message,
            hostname=self._settings.hostname,
            port=self._settings.port,
            username=self._settings.username,
            password=self._settings.password.get_secret_value()
            if self._settings.password
            else None,
            start_tls=self._settings.start_tls,
            timeout=self._settings.timeout,
        )
