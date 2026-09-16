import { request } from "@/shared/api/request";

import type { ChangePasswordParams } from "./schemas";

export async function changePassword(
  params: ChangePasswordParams,
): Promise<void> {
  await request({
    method: "PATCH",
    url: "/users/me/password",
    data: params,
  });
}
