import axios from "axios";

import { env } from "@/shared/config/env";

export const httpClient = axios.create({
  baseURL: env.apiBaseURL,
  timeout: 10_000,
  withCredentials: true,
});
