import { type ReactNode } from "react";

import { useQuery } from "@tanstack/react-query";

import { currentUserQueryOptions } from "@/entities/user/api/queries";

import { AuthContext } from "./AuthContext";

type AuthProviderProps = {
  children: ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const { data: user, isPending } = useQuery(currentUserQueryOptions());

  return (
    <AuthContext.Provider
      value={{
        user: user ?? null,
        isLoading: isPending,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export default AuthProvider;
