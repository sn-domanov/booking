import { Outlet } from "react-router-dom";

function AuthLayout() {
  return (
    <main className="flex min-h-svh items-center justify-center bg-muted/40 px-4 py-12">
      <div className="w-full max-w-sm">
        <Outlet />
      </div>
    </main>
  );
}

export default AuthLayout;
