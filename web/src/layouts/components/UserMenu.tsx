import { LogOut, User } from "lucide-react";
import { Link } from "react-router-dom";

import type { CurrentUser } from "@/entities/user/model";
import { Button } from "@/shared/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/shared/components/ui/dropdown-menu";

type UserMenuProps = {
  user: CurrentUser;
  onLogout: () => void;
};

function UserMenu({ user, onLogout }: UserMenuProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger render={<Button variant="outline" size="lg" />}>
        {user.displayName}
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end">
        <DropdownMenuItem render={<Link to="/profile" />}>
          <User />
          Profile
        </DropdownMenuItem>

        <DropdownMenuSeparator />

        <DropdownMenuItem onClick={onLogout}>
          <LogOut />
          Log out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export default UserMenu;
