import type { CurrentUser, User } from "../model/user";
import type { CurrentUserDto, UserDto } from "./dto";

export function mapUser(dto: UserDto): User {
  return {
    id: dto.id,
    displayName: dto.displayName,
    createdAt: new Date(dto.createdAt),
  };
}

export function mapCurrentUser(dto: CurrentUserDto): CurrentUser {
  return {
    id: dto.id,
    email: dto.email,
    displayName: dto.displayName,
    createdAt: new Date(dto.createdAt),
    updatedAt: new Date(dto.updatedAt),
  };
}
