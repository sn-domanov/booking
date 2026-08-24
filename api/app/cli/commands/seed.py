import asyncio

import httpx
import typer

from app.core.config import get_settings
from app.db.session import session_factory
from app.domains.listings.seed.seed import clear_listing_data, seed_listings
from app.infrastructure.storage.factory import create_object_storage
from app.main import app as fastapi_app

# ─────────────────────────────────────────
# Console helpers
# ─────────────────────────────────────────


def success(msg: str) -> None:
    typer.secho(msg, fg=typer.colors.GREEN, bold=True)


# ─────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────


def seed_command(
    clear: bool = typer.Option(
        False,
        "--clear",
        help="Clear existing data from database and object storage.",
    ),
) -> None:
    asyncio.run(_seed(clear=clear))


async def _seed(
    *,
    clear: bool,
) -> None:
    if clear:
        typer.confirm(
            "This will delete existing data from database and object storage. Continue?",
            abort=True,
        )

    settings = get_settings()
    storage = create_object_storage(settings)
    transport = httpx.ASGITransport(app=fastapi_app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://localhost",
    ) as client:
        # Clear data (using infrastructure directly)
        async with session_factory() as session:
            await clear_listing_data(session, storage)

        # Seed data (using API calls)
        await seed_listings(client)

    success("\nDone!")
