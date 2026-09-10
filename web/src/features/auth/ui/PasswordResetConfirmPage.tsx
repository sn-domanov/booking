import { Navigate, useSearchParams } from "react-router-dom";

import PasswordResetConfirmForm from "./PasswordResetConfirmForm";

export default function PasswordResetConfirmPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");

  if (!token) {
    return <Navigate to="/password-reset/request" replace />;
  }

  return <PasswordResetConfirmForm token={token} />;
}
