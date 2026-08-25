import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles/index.css";
import App from "./App.tsx";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import AppProviders from "./providers/AppProviders.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AppProviders>
      <App />

      {import.meta.env.DEV && <ReactQueryDevtools initialIsOpen={false} />}
    </AppProviders>
  </StrictMode>,
);
