import { z } from "zod";

import { currentUserDtoSchema } from "@/entities/user/api/dto";

export const authResponseDtoSchema = z.object({
  user: currentUserDtoSchema,
});

export type AuthResponseDto = z.infer<typeof authResponseDtoSchema>;
