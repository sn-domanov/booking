from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.domains.auth.api.deps import AuthServiceDep
from app.domains.auth.api.schemas import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def token(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
) -> TokenResponse:
    result = await service.login(
        # TODO: add email normalization
        email=data.username,
        password=data.password,
    )

    return TokenResponse(
        access_token=result.tokens.access_token,
        token_type="bearer",
    )
