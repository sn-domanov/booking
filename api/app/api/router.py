from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi_csrf_protect import CsrfProtect

from app.api.deps.csrf import require_csrf
from app.api.schemas import CsrfTokenResponse
from app.domains.auth.api.router import router as auth_router
from app.domains.listings.api.router import router as listings_router
from app.domains.users.api.router import router as users_router

api_v1_router = APIRouter(
    prefix="/api/v1",
    # `dependencies` expects `list[Depends]` - not `list[Annotated]``
    dependencies=[Depends(require_csrf)],
)


@api_v1_router.get("/csrf", tags=["security"])
async def get_csrf_token(
    response: Response,
    csrf_protect: Annotated[CsrfProtect, Depends()],
) -> CsrfTokenResponse:
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    csrf_protect.set_csrf_cookie(signed_token, response)

    return CsrfTokenResponse(csrf_token=csrf_token)


api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(listings_router)
