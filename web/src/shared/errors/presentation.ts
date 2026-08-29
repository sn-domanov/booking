import type { AppError } from "@/shared/api/errors";

export type ErrorPresentation = {
  title: string;
  description: string;
};

// i18n
// type ErrorPresentation = {
//   title: TranslationKey;
//   description: TranslationKey;
// };

export function getErrorPresentation(error: AppError): ErrorPresentation {
  switch (error.type) {
    case "api":
      return getApiErrorPresentation(error);

    case "network":
      return {
        title: "Connection problem",
        description: "Unable to reach the server.",
      };

    case "validation":
      return {
        title: "Invalid data",
        description: "The submitted data could not be validated.",
      };

    case "unknown":
      return {
        title: "Something went wrong",
        description: "Please try again.",
      };
  }
}

function getApiErrorPresentation(
  error: Extract<AppError, { type: "api" }>,
): ErrorPresentation {
  switch (error.code) {
    case "not_found":
      return {
        title: "Not found",
        description: error.detail,
      };

    case "conflict":
      return {
        title: "Conflict",
        description: error.detail,
      };

    case "validation_error":
      return {
        title: "Invalid data",
        description: error.detail,
      };

    case "image_processing_error":
      return {
        title: "Image processing failed",
        description: error.detail,
      };

    case "image_too_large":
      return {
        title: "Image is too large",
        description: error.detail,
      };

    case "invalid_image":
      return {
        title: "Invalid image",
        description: error.detail,
      };

    case "image_dimensions_too_large":
      return {
        title: "Image dimensions are too large",
        description: error.detail,
      };

    case "storage_error":
      return {
        title: "Storage error",
        description: error.detail,
      };

    case "invalid_storage_key":
      return {
        title: "Invalid storage key",
        description: error.detail,
      };

    case "invalid_cursor":
      return {
        title: "Invalid cursor",
        description: error.detail,
      };

    default:
      return {
        title: "Request failed",
        description: error.detail,
      };
  }
}
