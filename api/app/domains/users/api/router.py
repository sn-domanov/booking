from uuid import UUID

from fastapi import APIRouter, status

from app.api.deps.users import UserServiceDep
from app.domains.users.api.schemas import UserCreate, UserResponse
from app.domains.users.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep) -> User:
    user = await service.create_user(data=data)

    return user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, service: UserServiceDep) -> User:
    user = await service.get_user(user_id=user_id)

    return user
