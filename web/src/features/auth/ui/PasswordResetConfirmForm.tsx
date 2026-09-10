import { zodResolver } from "@hookform/resolvers/zod";
import { Controller, useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";

import type { AppError } from "@/shared/api/errors";
import { Alert, AlertDescription } from "@/shared/components/ui/alert";
import { Button } from "@/shared/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/shared/components/ui/card";
import {
  Field,
  FieldError,
  FieldGroup,
  FieldLabel,
} from "@/shared/components/ui/field";
import { Input } from "@/shared/components/ui/input";
import { toast } from "@/shared/components/ui/toast";

import { confirmPasswordReset } from "../api/api";
import {
  passwordResetConfirmFormSchema,
  type PasswordResetConfirmFormValues,
} from "../schemas";

type PasswordResetConfirmFormProps = {
  token: string;
};

function PasswordResetConfirmForm({ token }: PasswordResetConfirmFormProps) {
  const navigate = useNavigate();

  const form = useForm<PasswordResetConfirmFormValues>({
    resolver: zodResolver(passwordResetConfirmFormSchema),
    defaultValues: {
      newPassword: "",
      newPasswordConfirmation: "",
    },
  });

  async function onSubmit(values: PasswordResetConfirmFormValues) {
    try {
      await confirmPasswordReset({
        token,
        ...values,
      });

      toast.add({
        title: "Password updated",
        description: "You can now sign in with your new password.",
        type: "success",
      });

      navigate("/login");
    } catch (error) {
      form.setError("root", {
        message: (error as AppError).message,
      });
    }
  }

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Reset your password</CardTitle>
        <CardDescription>
          Enter a new password for your account.
        </CardDescription>
      </CardHeader>

      <CardContent>
        <form onSubmit={form.handleSubmit(onSubmit)}>
          <FieldGroup>
            {form.formState.errors.root && (
              <Alert variant="destructive">
                <AlertDescription>
                  {form.formState.errors.root.message}
                </AlertDescription>
              </Alert>
            )}

            <Controller
              name="newPassword"
              control={form.control}
              render={({ field, fieldState }) => (
                <Field data-invalid={fieldState.invalid}>
                  <FieldLabel htmlFor={field.name}>New password</FieldLabel>

                  <Input
                    {...field}
                    id={field.name}
                    type="password"
                    autoComplete="new-password"
                    aria-invalid={fieldState.invalid}
                  />

                  {fieldState.invalid && (
                    <FieldError errors={[fieldState.error]} />
                  )}
                </Field>
              )}
            />

            <Controller
              name="newPasswordConfirmation"
              control={form.control}
              render={({ field, fieldState }) => (
                <Field data-invalid={fieldState.invalid}>
                  <FieldLabel htmlFor={field.name}>
                    Confirm new password
                  </FieldLabel>

                  <Input
                    {...field}
                    id={field.name}
                    type="password"
                    autoComplete="new-password"
                    aria-invalid={fieldState.invalid}
                  />

                  {fieldState.invalid && (
                    <FieldError errors={[fieldState.error]} />
                  )}
                </Field>
              )}
            />

            <Button
              type="submit"
              className="w-full"
              disabled={form.formState.isSubmitting}
            >
              {form.formState.isSubmitting
                ? "Updating password…"
                : "Update password"}
            </Button>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  );
}

export default PasswordResetConfirmForm;
