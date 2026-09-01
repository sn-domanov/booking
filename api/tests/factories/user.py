from app.core.security import get_password_hash
from app.domains.users.models import User


def user_factory(
    *,
    email: str = "test@example.com",
    display_name: str = "Test User",
    password: str = "testpass",
    is_active: bool = True,
    is_admin: bool = False,
) -> User:
    return User(
        email=email,
        display_name=display_name,
        # TODO: this uses expensive argon2 in tests, reconsider if tests are slow
        password_hash=get_password_hash(password),
        is_active=is_active,
        is_admin=is_admin,
    )
