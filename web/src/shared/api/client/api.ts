import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";

import { env } from "@/shared/config/env";

import { ensureCsrfToken, getCsrfToken, resetCsrfToken } from "../csrf";
import type { ApiError } from "../errors";

// ─────────────────────────────────────────
// Client
// ─────────────────────────────────────────

export const apiClient = axios.create({
  baseURL: `${env.apiBaseURL}/api/v1`,
  timeout: 10_000,

  withCredentials: true,

  // withXSRFToken won't work because `fastapi-csrf-protect` used in this project
  // expects base64 encoded and signed token in cookie, but plaintext token in header.
  // Plaintext token is acquired from `/csrf` response body.
});

// ─────────────────────────────────────────
// Interceptors
// ─────────────────────────────────────────

const unsafeMethods = new Set(["post", "put", "patch", "delete"]);

apiClient.interceptors.request.use((config) => {
  const token = getCsrfToken();
  const method = config.method?.toLowerCase();

  if (token && method && unsafeMethods.has(method)) {
    config.headers.set("X-CSRF-Token", token);
  }

  return config;
});

type RequestConfig = InternalAxiosRequestConfig & {
  _csrfRetry?: boolean;
};

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const request = error.config as RequestConfig;

    if (!request) {
      throw error;
    }

    // CSRF expired/missing
    if (
      (error.response?.data as ApiError | undefined)?.code === "csrf_error" &&
      !request._csrfRetry
    ) {
      request._csrfRetry = true;

      resetCsrfToken();
      await ensureCsrfToken();

      return apiClient(request);
    }

    throw error;
  },
);
