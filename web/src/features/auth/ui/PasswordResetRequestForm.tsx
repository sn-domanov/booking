import { zodResolver } from "@hookform/resolvers/zod";
import { Controller, useForm } from "react-hook-form";

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

import { requestPasswordReset } from "../api/api";
import {
  type PasswordResetParams,
  passwordResetRequestSchema,
} from "../schemas";

function PasswordResetRequestForm() {
  const form = useForm<PasswordResetParams>({
    resolver: zodResolver(passwordResetRequestSchema),
    defaultValues: {
      email: "",
    },
  });

  async function onSubmit(values: PasswordResetParams) {
    try {
      await requestPasswordReset(values);

      toast.add({
        title: "Check your email",
        description:
          "If an account exists with this email, you'll receive instructions to reset your password.",
        type: "success",
      });
    } catch (error) {
      form.setError("root", {
        message: (error as AppError).message,
      });
    }
  }

  return (
    <Card className="w-full max-w-sm">
      <CardHeader>
        <CardTitle>Forgot your password?</CardTitle>
        <CardDescription>
          Enter your email address and we'll send you instructions to reset your
          password.
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
              name="email"
              control={form.control}
              render={({ field, fieldState }) => (
                <Field data-invalid={fieldState.invalid}>
                  <FieldLabel htmlFor={field.name}>Email</FieldLabel>

                  <Input
                    {...field}
                    id={field.name}
                    type="email"
                    autoComplete="email"
                    aria-invalid={fieldState.invalid}
                    placeholder="you@example.com"
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
              {form.formState.isSubmitting ? "Sending…" : "Send reset link"}
            </Button>
          </FieldGroup>
        </form>
      </CardContent>
    </Card>
  );
}

export default PasswordResetRequestForm;
