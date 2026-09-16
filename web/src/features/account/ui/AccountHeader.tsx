import { PanelLeftIcon, UserRound } from "lucide-react";

import { useAuth } from "@/app/providers/auth/useAuth";
import { Avatar, AvatarFallback } from "@/shared/components/ui/avatar";
import { Button } from "@/shared/components/ui/button";
import { useSidebar } from "@/shared/components/ui/sidebar";

function AccountHeader() {
  const { user, isLoading } = useAuth();
  const { toggleSidebar } = useSidebar();

  return (
    <header>
      <div className="page flex flex-col items-start gap-2 py-2">
        <div className="flex items-center gap-3">
          <Avatar>
            <AvatarFallback>
              <UserRound />
            </AvatarFallback>
          </Avatar>

          <div>
            {isLoading ? (
              <div className="bg-muted h-8 w-40 animate-pulse rounded" />
            ) : (
              <>
                <div className="text-sm font-medium">{user?.displayName}</div>
                <div className="text-muted-foreground text-sm">
                  {user?.email}
                </div>
              </>
            )}
          </div>
        </div>

        <Button
          variant="secondary"
          className="md:hidden"
          onClick={toggleSidebar}
        >
          <PanelLeftIcon />
          Menu
        </Button>
      </div>
    </header>
  );
}

export default AccountHeader;
