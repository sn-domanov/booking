import asyncio

import httpx
import typer

from app.db.session import session_factory
from app.domains.listings.seed.seed import seed_listings
from app.main import app as fastapi_app

# ─────────────────────────────────────────
# Console helpers
# ─────────────────────────────────────────


def success(msg: str) -> None:
    typer.secho(msg, fg=typer.colors.GREEN, bold=True)


# ─────────────────────────────────────────
# Orchestration
# ─────────────────────────────────────────


def seed_command() -> None:
    asyncio.run(_seed())


async def _seed() -> None:
    transport = httpx.ASGITransport(app=fastapi_app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://localhost",
    ) as client:
        async with session_factory() as session:
            pass

        await seed_listings(client)

    success("\nDone!")
