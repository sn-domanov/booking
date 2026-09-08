import { parseResponse } from "@/shared/api/parse";
import { request } from "@/shared/api/request";

import type { CurrentUser, User } from "../model/user";
import { currentUserDtoSchema, userDtoSchema } from "./dto";
import { mapCurrentUser, mapUser } from "./mapper";

export type GetUserParams = {
  userId: string;
};

export async function getUser({ userId }: GetUserParams): Promise<User> {
  const data = await request({
    method: "GET",
    url: `/users/${userId}`,
  });

  const dto = parseResponse(userDtoSchema, data);

  return mapUser(dto);
}

export async function getCurrentUser(): Promise<CurrentUser> {
  const data = await request({
    method: "GET",
    url: "/users/me",
  });

  const dto = parseResponse(currentUserDtoSchema, data);

  return mapCurrentUser(dto);
}
