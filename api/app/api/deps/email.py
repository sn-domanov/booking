from typing import Annotated

from fastapi import Depends

from app.api.deps.settings import SettingsDep
from app.infrastructure.email.protocol import EmailSender
from app.infrastructure.email.smtp import SmtpEmailSender


def get_email_sender(settings: SettingsDep) -> EmailSender:
    return SmtpEmailSender(settings.smtp)


EmailSenderDep = Annotated[
    EmailSender,
    Depends(get_email_sender),
]
