import { Outlet } from "react-router-dom";

import AccountHeader from "@/features/account/ui/AccountHeader";
import { AccountNavigation } from "@/features/account/ui/AccountNavigation";
import AppHeader from "@/layouts/components/AppHeader";
import { SidebarProvider } from "@/shared/components/ui/sidebar";

export function AccountLayout() {
  return (
    <SidebarProvider className="flex h-dvh flex-col">
      <AppHeader />

      <AccountHeader />

      <div className="flex flex-1">
        <AccountNavigation />

        <main className="flex-1 p-6">
          <Outlet />
        </main>
      </div>
    </SidebarProvider>
  );
}
