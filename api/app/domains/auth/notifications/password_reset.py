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

    await email_sender.send(
        to=to_email,
        subject="Reset your password",
        text=(
            f"Hi {display_name},\n\n"
            f"Reset your password:\n{reset_url}\n\n"
            "If you didn't request this, you can ignore this email."
        ),
        # TODO: replace with a template
        html=(
            f"<p>Hi {display_name},</p>"
            f'<p><a href="{reset_url}">Reset your password</a></p>'
            "<p>If you didn't request this, you can ignore this email.</p>"
        ),
    )
