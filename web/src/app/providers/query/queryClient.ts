import { QueryClient } from "@tanstack/react-query";

import type { AppError } from "@/shared/api/errors";

declare module "@tanstack/react-query" {
  interface Register {
    defaultError: AppError;
  }
}

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 60_000,
    },
  },
});

export default queryClient;
