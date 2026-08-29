import type { AxiosRequestConfig } from "axios";

import { apiClient } from "./client";
import { normalizeError } from "./errors";

/**
 * Makes an API request, unwraps the Axios response,
 * and normalizes Axios errors into AppError.
 */
export async function request<T>(config: AxiosRequestConfig): Promise<T> {
  try {
    const response = await apiClient.request<T>(config);

    // N.B. request unwraps Axios response
    return response.data;
  } catch (error) {
    throw normalizeError(error);
  }
}
