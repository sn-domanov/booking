import { Link } from "react-router-dom";

import { useAuth } from "@/app/providers/auth/useAuth";
import { toast } from "@/shared/components/ui/toast";

import GuestNav from "./GuestNav";
import UserMenu from "./UserMenu";

function AppHeader() {
  const { user, logout } = useAuth();

  async function handleLogout() {
    await logout();

    toast.add({
      title: "Logged out",
      description: "You have been successfully logged out.",
      type: "success",
    });
  }

  return (
    <header className="border-b">
      <div className="page flex h-16 items-center justify-between">
        <Link to="/" className="text-lg font-semibold">
          Booking
        </Link>

        {/* UserMenu is an account control, not navigation. Hence div - not nav. */}
        <div className="flex items-center gap-1">
          {user ? (
            <UserMenu user={user} onLogout={handleLogout} />
          ) : (
            <GuestNav />
          )}
        </div>
      </div>
    </header>
  );
}

export default AppHeader;
