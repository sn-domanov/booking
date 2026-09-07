from httpx import AsyncClient

from app.db.uow import UnitOfWork
from app.domains.users.models import User
from tests.factories.user import user_factory


async def create_user(uow: UnitOfWork, **overrides) -> User:
    user = user_factory(**overrides)

    async with uow.transaction():
        uow.users.add(user=user)

    return user


async def set_csrf_header(client: AsyncClient) -> None:
    response = await client.get(
        "/api/v1/csrf",
    )

    assert response.status_code == 200

    csrf_token = response.json()["csrfToken"]
    client.headers["X-CSRF-Token"] = csrf_token


async def login_as(
    client: AsyncClient,
    uow: UnitOfWork,
    *,
    email: str = "test@example.com",
    password: str = "testpass",
) -> User:
    user = await create_user(
        uow,
        email=email,
        password=password,
    )

    await set_csrf_header(client)

    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    return user
