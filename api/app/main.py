from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.exception_handlers import application_exception_handler
from app.api.router import api_v1_router
from app.core.config import get_settings
from app.core.exceptions import ApplicationError
from app.db.session import engine
from app.health.router import router as health_router

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Startup event

    yield

    # Shutdown event
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=settings.app_name,
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url="/redoc" if settings.docs_enabled else None,
        openapi_url="/openapi.json" if settings.docs_enabled else None,
    )

    register_exception_handlers(app)
    register_routers(app)

    return app


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, application_exception_handler)


def register_routers(app: FastAPI) -> None:
    app.include_router(health_router)
    app.include_router(api_v1_router)


app = create_app()
