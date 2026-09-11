import { Outlet } from "react-router-dom";

import AppHeader from "./components/AppHeader";

function AuthLayout() {
  return (
    <div className="min-h-svh flex flex-col">
      <AppHeader />

      <main className="flex flex-1 items-center justify-center bg-muted/40 px-4 py-12">
        <div className="w-full max-w-sm">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

export default AuthLayout;
