import { createContext } from "react";

import type { CurrentUser } from "@/entities/user/model";

export type AuthContextValue = {
  user: CurrentUser | null;
  isLoading: boolean;
  logout: () => Promise<void>;
};

export const AuthContext = createContext<AuthContextValue | null>(null);
