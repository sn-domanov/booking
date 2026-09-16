import { CalendarDays, House, LockKeyhole, UserRound } from "lucide-react";
import { Link, useLocation } from "react-router-dom";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/shared/components/ui/sidebar";
import { useIsMobile } from "@/shared/hooks/use-mobile";

const items = [
  {
    title: "Profile",
    href: "/account/profile",
    icon: UserRound,
  },
  {
    title: "Security",
    href: "/account/security",
    icon: LockKeyhole,
  },
  {
    title: "Bookings",
    href: "/account/bookings",
    icon: CalendarDays,
  },
  {
    title: "Listings",
    href: "/account/listings",
    icon: House,
  },
];

export function AccountNavigation() {
  const location = useLocation();
  const isMobile = useIsMobile();

  return (
    <Sidebar collapsible={isMobile ? "offcanvas" : "none"}>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>My account</SidebarGroupLabel>

          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.href}>
                  <SidebarMenuButton
                    isActive={location.pathname === item.href}
                    render={<Link to={item.href} />}
                  >
                    <item.icon />
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  );
}
