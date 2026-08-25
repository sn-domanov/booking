import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { ReactQueryDevtools } from "@tanstack/react-query-devtools";

import App from "./App.tsx";
import AppProviders from "./providers/AppProviders.tsx";

import "./styles/index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AppProviders>
      <App />

      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </AppProviders>
  </StrictMode>,
);
