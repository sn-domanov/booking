import { Outlet } from "react-router-dom";

import AppHeader from "./components/AppHeader";

function AuthLayout() {
  return (
    <div className="flex min-h-svh flex-col">
      <AppHeader />

      <main className="bg-muted/40 flex flex-1 items-center justify-center px-4 py-12">
        <div className="w-full max-w-sm">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

export default AuthLayout;
