import { Link, useLocation, Outlet } from "react-router-dom";
import { Box, Flex, Text } from "@radix-ui/themes";
import {
  DashboardIcon,
  PersonIcon,
  CrossCircledIcon,
  RocketIcon,
  GearIcon,
} from "@radix-ui/react-icons";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard", icon: DashboardIcon },
  { to: "/players", label: "Players", icon: PersonIcon },
  { to: "/wars", label: "Wars", icon: CrossCircledIcon },
  { to: "/raids", label: "Capital Raids", icon: RocketIcon },
  { to: "/tracked-clans", label: "Tracked Clans", icon: GearIcon },
];

export function Layout() {
  const location = useLocation();

  return (
    <Flex className="min-h-screen">
      <Box
        asChild
        className="w-60 shrink-0 border-r border-[var(--gray-5)] bg-[var(--gray-2)]"
      >
        <nav>
          <Box px="4" py="5">
            <Text size="5" weight="bold">
              Clash Tracker
            </Text>
          </Box>
          <Flex direction="column" gap="1" px="2">
            {NAV_ITEMS.map(({ to, label, icon: Icon }) => {
              const active =
                to === "/" ? location.pathname === "/" : location.pathname.startsWith(to);
              return (
                <Link
                  key={to}
                  to={to}
                  className={`flex items-center gap-3 rounded-md px-3 py-2 text-sm no-underline transition-colors ${
                    active
                      ? "bg-[var(--accent-3)] text-[var(--accent-11)] font-medium"
                      : "text-[var(--gray-11)] hover:bg-[var(--gray-3)]"
                  }`}
                >
                  <Icon width={16} height={16} />
                  {label}
                </Link>
              );
            })}
          </Flex>
        </nav>
      </Box>
      <Box className="flex-1 overflow-auto" p="6">
        <Outlet />
      </Box>
    </Flex>
  );
}
