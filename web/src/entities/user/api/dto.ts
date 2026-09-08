import { z } from "zod";

export const userDtoSchema = z.object({
  id: z.uuid(),
  displayName: z.string(),
  createdAt: z.iso.datetime(),
});

export type UserDto = z.infer<typeof userDtoSchema>;

export const currentUserDtoSchema = z.object({
  id: z.uuid(),
  email: z.email(),
  displayName: z.string(),
  createdAt: z.iso.datetime(),
  updatedAt: z.iso.datetime(),
});

export type CurrentUserDto = z.infer<typeof currentUserDtoSchema>;
