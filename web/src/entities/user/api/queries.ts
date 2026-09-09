import { queryOptions } from "@tanstack/react-query";

import { getCurrentUser, getUser, type GetUserParams } from "./api";

export function userQueryOptions(params: GetUserParams) {
  return queryOptions({
    queryKey: ["users", params],
    queryFn: () => getUser(params),
  });
}

export function currentUserQueryOptions() {
  return queryOptions({
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
