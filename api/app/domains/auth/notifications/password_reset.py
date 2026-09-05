from app.core.jinja import email_templates
from app.infrastructure.email.protocol import EmailSender


async def send_password_reset_email(
    *,
    email_sender: EmailSender,
    to_email: str,
    display_name: str,
    token: str,
    frontend_base_url: str,
) -> None:
    reset_url = f"{frontend_base_url.rstrip('/')}/reset-password?token={token}"

    template = email_templates.get_template("auth/password_reset.html")

    html = template.render(
        reset_url=reset_url,
        display_name=display_name,
    )

    text = f"""\
Hi {display_name},

You requested to reset your password. Click the link below to set a new password:

{reset_url}

This link will expire in 1 hour.

If you didn't request this, you can safely ignore this email.

Best regards,
The Booking Team
"""

    await email_sender.send(
        to=to_email,
        subject="Reset your password",
        text=text,
        html=html,
    )
