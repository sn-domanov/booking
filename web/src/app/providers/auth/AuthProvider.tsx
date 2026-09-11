import { type ReactNode } from "react";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { currentUserQueryOptions } from "@/entities/user/api/queries";
import { logout } from "@/features/auth/api";

import { AuthContext } from "./AuthContext";

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const queryClient = useQueryClient();

  const { data: user, isPending } = useQuery(currentUserQueryOptions());

  const logoutMutation = useMutation({
    mutationFn: logout,
    onSuccess: () => {
      // N.B. update the query data explicitly so subscribed components re-render
      queryClient.setQueryData(currentUserQueryOptions().queryKey, null);
    },
  });

  return (
    <AuthContext.Provider
      value={{
        user: user ?? null,
        isLoading: isPending,
        logout: logoutMutation.mutateAsync,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
