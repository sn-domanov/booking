import { httpClient } from "./client";

export async function checkHealth() {
  const response = await httpClient.get("/health/ready");

  return response.data;
}
