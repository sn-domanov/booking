import z from "zod";

export const changePasswordSchema = z.object({
  currentPassword: z.string(),
  newPassword: z.string().min(8).max(1024),
});

export type ChangePasswordParams = z.infer<typeof changePasswordSchema>;

export const changePasswordFormSchema = changePasswordSchema
  .extend({
    newPasswordConfirmation: z.string(),
  })
  .refine((data) => data.newPassword === data.newPasswordConfirmation, {
    path: ["newPasswordConfirmation"],
    message: "Passwords do not match.",
  });

export type ChangePasswordFormValues = z.infer<typeof changePasswordFormSchema>;
