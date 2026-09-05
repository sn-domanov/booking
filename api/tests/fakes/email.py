from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SentEmail:
    to: str
    subject: str
    text: str
    html: str | None = None


class FakeEmailSender:
    def __init__(self) -> None:
        self.messages: list[SentEmail] = []

    async def send(
        self,
        *,
        to: str,
        subject: str,
        text: str,
        html: str | None = None,
    ) -> None:
        self.messages.append(
            SentEmail(
                to=to,
                subject=subject,
                text=text,
                html=html,
            )
        )
