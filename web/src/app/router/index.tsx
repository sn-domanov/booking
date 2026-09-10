import { createBrowserRouter, RouterProvider } from "react-router-dom";

import LoginPage from "@/features/auth/ui/LoginPage";
import PasswordResetConfirmPage from "@/features/auth/ui/PasswordResetConfirmPage";
import PasswordResetRequestPage from "@/features/auth/ui/PasswordResetRequestPage";
import SignupPage from "@/features/auth/ui/SignupPage";
import AppLayout from "@/layouts/AppLayout";
import AuthLayout from "@/layouts/AuthLayout";
import HomePage from "@/pages/HomePage";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppLayout />,
    // TODO: errorElement
    children: [
      {
        index: true,
        element: <HomePage />,
      },
    ],
  },
  {
    element: <AuthLayout />,
    children: [
      {
        path: "/signup",
        element: <SignupPage />,
      },
      {
        path: "/login",
        element: <LoginPage />,
      },
      {
        path: "password-reset",
        children: [
          {
            path: "request",
            element: <PasswordResetRequestPage />,
          },
          {
            path: "confirm",
            element: <PasswordResetConfirmPage />,
          },
        ],
      },
    ],
  },
]);

function AppRouter() {
  return <RouterProvider router={router} />;
}

export default AppRouter;
