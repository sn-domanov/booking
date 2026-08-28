import { Card, CardContent, CardHeader } from "@/shared/components/ui/card";
import { Skeleton } from "@/shared/components/ui/skeleton";

export function ListingCardSkeleton() {
  return (
    <Card className="overflow-hidden pt-0">
      <div className="relative">
        <Skeleton className="aspect-video w-full" />
        <Skeleton className="absolute inset-x-4 top-4 h-5 w-2/3" />
      </div>

      <CardHeader>
        <Skeleton className="h-5 w-2/3" />
        <Skeleton className="h-4 w-full" />
        <Skeleton className="h-4 w-4/5" />
      </CardHeader>

      <CardContent className="space-y-3">
        <div className="flex items-center gap-2">
          <Skeleton className="size-4 rounded-full" />
          <Skeleton className="h-4 w-24" />
        </div>

        <div className="flex items-center gap-2">
          <Skeleton className="size-4 rounded-full" />
          <Skeleton className="h-4 w-28" />
        </div>

        <div className="flex items-center gap-2">
          <Skeleton className="size-4 rounded-full" />
          <Skeleton className="h-4 w-20" />
        </div>
      </CardContent>
    </Card>
  );
}
