import { Outlet } from "react-router-dom";

import AppHeader from "./components/AppHeader";

function AppLayout() {
  return (
    <div className="min-h-svh flex flex-col">
      <AppHeader />

      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  );
}

export default AppLayout;
