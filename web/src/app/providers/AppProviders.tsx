import { QueryClientProvider } from "@tanstack/react-query";
import type React from "react";
import queryClient from "./query/queryClient";

type AppProvidersProps = {
  children: React.ReactNode;
};

function AppProviders({ children }: AppProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

export default AppProviders;
