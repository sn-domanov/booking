import asyncio

import typer

from app.db.uow import create_uow
from app.domains.users.api.schemas import UserCreate
from app.domains.users.service import UserService


def create_admin_command(
    email: str = typer.Option(..., prompt=True),
    display_name: str = typer.Option(..., prompt=True),
) -> None:
    password = typer.prompt(
        "Password",
        hide_input=True,
        confirmation_prompt=True,
    )

    asyncio.run(
        _create_admin(
            email=email,
            display_name=display_name,
            password=password,
        )
    )


async def _create_admin(
    *,
    email: str,
    display_name: str,
    password: str,
) -> None:
    # Avoiding DTO and using Pydantic schema at this step
    data = UserCreate(
        email=email,
        display_name=display_name,
        password=password,
    )

    async with create_uow() as uow:
        service = UserService(uow)

        await service.create_admin(data=data)

    typer.echo(f"Admin user {email} created.")
