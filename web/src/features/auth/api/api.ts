import { mapCurrentUser } from "@/entities/user/api/mapper";
import type { CurrentUser } from "@/entities/user/model/user";
import { parseResponse } from "@/shared/api/parse";
import { request } from "@/shared/api/request";

import type { LoginParams } from "../schemas";
import { authResponseDtoSchema } from "./dto";

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
