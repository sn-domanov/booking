import ChangePasswordForm from "@/features/user/change-password/ui/ChangePasswordForm";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/shared/components/ui/card";

export function AccountSecurityPage() {
  return (
    <div className="mx-auto w-full max-w-xl space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Security</h1>

        <p className="text-muted-foreground">
          Manage your password and account security.
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Password</CardTitle>

          <CardDescription>
            Change the password you use to sign in.
          </CardDescription>
        </CardHeader>

        <CardContent>
          <ChangePasswordForm />
        </CardContent>
      </Card>
    </div>
  );
}
