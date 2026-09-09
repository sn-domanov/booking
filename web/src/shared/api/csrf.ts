import { z } from "zod";

import { httpClient } from "./client/http";
import { parseResponse } from "./parse";

const csrfTokenResponseSchema = z.object({
  csrfToken: z.string().min(1),
});

let csrfToken: string | null = null;

export async function ensureCsrfToken(): Promise<void> {
  if (csrfToken) {
    return;
  }

  const response = await httpClient.get("/api/v1/csrf");
  const data = parseResponse(csrfTokenResponseSchema, response.data);

  csrfToken = data.csrfToken;
}

export function getCsrfToken(): string | null {
  return csrfToken;
}

export function resetCsrfToken(): void {
  csrfToken = null;
}
