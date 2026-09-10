import { userDtoSchema } from "@/entities/user/api/dto";
import { mapCurrentUser, mapUser } from "@/entities/user/api/mapper";
import type { CurrentUser, User } from "@/entities/user/model/user";
import { parseResponse } from "@/shared/api/parse";
import { request } from "@/shared/api/request";

import type {
  LoginParams,
  PasswordResetConfirmParams,
  PasswordResetRequestParams,
  SignupParams,
} from "../schemas";
import { authResponseDtoSchema } from "./dto";

export async function signup(params: SignupParams): Promise<User> {
  const data = await request({
    method: "POST",
    url: "/users",
    data: params,
  });

  const dto = parseResponse(userDtoSchema, data);

  return mapUser(dto);
}

export async function login(params: LoginParams): Promise<CurrentUser> {
  const data = await request({
    method: "POST",
    url: "/auth/login",
    data: params,
  });

  const dto = parseResponse(authResponseDtoSchema, data);

  return mapCurrentUser(dto.user);
}

export async function logout(): Promise<void> {
  await request({
    method: "POST",
    url: "/auth/logout",
  });
}

export async function requestPasswordReset(
  params: PasswordResetRequestParams,
): Promise<void> {
  await request({
    method: "POST",
    url: "/auth/password-reset/request",
    data: params,
  });
}

export async function confirmPasswordReset(
  params: PasswordResetConfirmParams,
): Promise<void> {
  await request({
    method: "POST",
    url: "/auth/password-reset/confirm",
    data: params,
  });
}
