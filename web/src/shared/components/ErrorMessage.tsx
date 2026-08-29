import type { AppError } from "@/shared/api/errors";
import { getErrorPresentation } from "@/shared/errors/presentation";

import { Button } from "./ui/button";

type ErrorMessageProps = {
  error: AppError;
  onRetry: () => void;
};

export function ErrorMessage({ error, onRetry }: ErrorMessageProps) {
  const { title, description } = getErrorPresentation(error);

  return (
    <div
      className="flex min-h-64 flex-col items-center justify-center gap-4 rounded-lg border border-destructive/20 bg-destructive/5 p-8 text-center"
      role="alert"
    >
      <div className="space-y-1">
        <p className="font-medium text-destructive">{title}</p>
        <p className="text-sm text-muted-foreground">{description}</p>
      </div>

      <Button variant="outline" onClick={onRetry}>
        Try again
      </Button>
    </div>
  );
}
