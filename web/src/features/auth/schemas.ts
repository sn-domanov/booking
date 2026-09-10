import { z } from "zod";

export const loginSchema = z.object({
  email: z.email(),
  password: z.string().min(8).max(1024),
});

export type LoginParams = z.infer<typeof loginSchema>;

export const signupSchema = z.object({
  email: z.email(),
  password: z.string().min(8).max(1024),
  displayName: z.string().min(3).max(150),
});

export type SignupParams = z.infer<typeof signupSchema>;

export const signupFormSchema = signupSchema
  .extend({
    passwordConfirmation: z.string(),
  })
  .refine((data) => data.password === data.passwordConfirmation, {
    path: ["passwordConfirmation"],
    message: "Passwords do not match.",
  });

export type SignupFormValues = z.infer<typeof signupFormSchema>;

export const passwordResetRequestSchema = z.object({
  email: z.email(),
});

export type PasswordResetRequestParams = z.infer<
  typeof passwordResetRequestSchema
>;

export const passwordResetConfirmSchema = z.object({
  token: z.string,
  newPassword: z.string().min(8).max(1024),
});

export type PasswordResetConfirmParams = z.infer<
  typeof passwordResetConfirmSchema
>;

export const passwordResetConfirmFormSchema = z
  .object({
    newPassword: z.string().min(8).max(1024),
    newPasswordConfirmation: z.string(),
  })
  .refine((data) => data.newPassword === data.newPasswordConfirmation, {
    path: ["newPasswordConfirmation"],
    message: "Passwords do not match.",
  });

export type PasswordResetConfirmFormValues = z.infer<
  typeof passwordResetConfirmFormSchema
>;
