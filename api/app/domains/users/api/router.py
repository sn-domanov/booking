from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps.auth import CurrentUserDep
from app.api.deps.users import UserServiceDep
from app.api.schemas import MessageResponse
from app.domains.users.api.schemas import (
    CurrentUserResponse,
    PasswordChangeRequest,
    UserCreate,
    UserResponse,
)
from app.domains.users.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep) -> User:
    user = await service.create_user(data=data)

    return user


@router.get("/me", response_model=CurrentUserResponse)
async def get_current_user(current_user: CurrentUserDep) -> User:
    return current_user


@router.patch("/me/password", response_model=MessageResponse)
async def change_password(
    data: PasswordChangeRequest,
    current_user: CurrentUserDep,
    service: UserServiceDep,
) -> MessageResponse:
    await service.change_password(
        user=current_user,
        current_password=data.current_password,
        new_password=data.new_password,
    )

    return MessageResponse.from_message("Password changed successfully.")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserServiceDep) -> User:
    user = await service.get_user(user_id=user_id)

    return user
