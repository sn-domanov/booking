import axios from "axios";
import { z } from "zod";

export type AppError =
  | {
      type: "api";
      status: number;
      code: string;
      message: string;
      conflict?: string;
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
  conflict: z.string().optional(),
});

export type ApiError = z.infer<typeof apiErrorSchema>;

const fastApiErrorSchema = z.object({
  detail: z.union([z.string(), z.array(z.unknown())]),
});

export function normalizeError(error: unknown): AppError {
  if (axios.isAxiosError(error)) {
    if (!error.response) {
      return {
        type: "network",
        message: error.message,
      };
    }

    const { status, data } = error.response;

    // Check if API application error
    const result = apiErrorSchema.safeParse(data);

    if (result.success) {
      return {
        type: "api",
        status,
        code: result.data.code,
        message: result.data.detail,
        conflict: result.data.conflict,
      };
    }

    // Check if error comes from FastAPI
    const fastApiResult = fastApiErrorSchema.safeParse(data);

    if (fastApiResult.success) {
      return {
        type: "api",
        status,
        code: "http_error",
        detail:
          typeof fastApiResult.data.detail === "string"
            ? fastApiResult.data.detail
            : "The server returned a validation error.",
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
