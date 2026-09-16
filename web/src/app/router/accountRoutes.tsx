import { Navigate } from "react-router-dom";

import { AccountLayout } from "@/pages/account/AccountLayout";
import { AccountSecurityPage } from "@/pages/account/AccountSecurityPage";

export const accountRoutes = {
  path: "/account",
  element: <AccountLayout />,
  children: [
    {
      index: true,
      element: <Navigate to="security" replace />,
    },
    {
      path: "security",
      element: <AccountSecurityPage />,
    },
  ],
};
