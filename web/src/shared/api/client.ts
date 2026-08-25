import axios from "axios";

import { env } from "../config/env";

export const httpClient = axios.create({
  baseURL: `${env.apiBaseURL}`,
  timeout: 10_000,
});

export const apiClient = axios.create({
  baseURL: `${env.apiBaseURL}/api/v1`,
  timeout: 10_000,
});
