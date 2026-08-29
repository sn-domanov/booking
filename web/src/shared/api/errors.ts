import axios from "axios";
import { z } from "zod";

export type AppError =
  | {
      type: "api";
      status: number;
      code: string;
      detail: string;
    }
  | {
      type: "network";
      message: string;
    }
  | {
      type: "validation";
      message: string;
      issues: z.core.$ZodIssue[];
    }
  | {
      type: "unknown";
      message: string;
    };

const apiErrorSchema = z.object({
  code: z.string(),
  detail: z.string(),
});

export function normalizeError(error: unknown): AppError {
  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return {
        type: "network",
        message: error.message,
      };
    }

    const result = apiErrorSchema.safeParse(error.response.data);

    if (result.success) {
      return {
        type: "api",
        status: error.response.status,
        code: result.data.code,
        detail: result.data.detail,
      };
    }

    return {
      type: "api",
      status: error.response.status,
      code: "unknown_api_error",
      detail: "The server returned an unexpected error.",
    };
  }

  if (error instanceof z.ZodError) {
    return {
      type: "validation",
      message: "Validation failed.",
      issues: error.issues,
    };
  }

  if (error instanceof Error) {
    return {
      type: "unknown",
      message: error.message,
    };
  }

  return {
    type: "unknown",
    message: "An unknown error occurred.",
  };
}
