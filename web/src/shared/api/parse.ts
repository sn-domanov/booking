import { z } from "zod";

import { normalizeError } from "./errors";

/**
 * Parses an API response and normalizes Zod errors into AppError.
 */
export function parseResponse<T>(schema: z.ZodType<T>, data: unknown): T {
  try {
    return schema.parse(data);
  } catch (error) {
    throw normalizeError(error);
  }
}
