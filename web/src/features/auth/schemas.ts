import { z } from "zod";

export const loginSchema = z.object({
  email: z.email(),
  password: z.string().min(8).max(1024),
});

export type LoginParams = z.infer<typeof loginSchema>;
