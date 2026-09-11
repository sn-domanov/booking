import { queryOptions } from "@tanstack/react-query";

import type { CurrentUser } from "../model";
import { getCurrentUser, getUser, type GetUserParams } from "./api";

export function userQueryOptions(params: GetUserParams) {
  return queryOptions({
    queryKey: ["users", params],
    queryFn: () => getUser(params),
  });
}

export function currentUserQueryOptions() {
  return queryOptions<CurrentUser | null>({
    queryKey: ["users", "me"],
    queryFn: async () => {
      // TODO: consider initializing CSRF explicitly
      // instead of relying on Axios interceptor
      // This would couple CSRF to authentication
      // await ensureCsrfToken();
      return getCurrentUser();
    },
    staleTime: Infinity,
  });
}
