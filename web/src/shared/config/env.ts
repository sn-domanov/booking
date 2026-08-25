import z from "zod";

const envSchema = z.object({
  VITE_API_BASE_URL: z.url(),
});

const parsed = envSchema.parse(import.meta.env);

export const env = {
  apiBaseURL: parsed.VITE_API_BASE_URL,
} as const;
