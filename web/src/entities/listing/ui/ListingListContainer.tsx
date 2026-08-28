import { useInfiniteQuery } from "@tanstack/react-query";

import { Button } from "@/shared/components/ui/button";

import { listingsQuery } from "../api/queries";
import { ListingList } from "./ListingList";

function ListingListContainer() {
  const query = useInfiniteQuery(listingsQuery);

  const listings = query.data?.pages.flatMap((page) => page.items) ?? [];

  return (
    <div className="space-y-8">
      <ListingList
        listings={listings}
        isLoading={query.isPending}
        error={query.error?.message}
      />

      {query.hasNextPage && (
        <div className="flex justify-center">
          <Button
            disabled={query.isFetchingNextPage}
            // query.fetchNextPage returns Promise, onClick handler expects nothing
            onClick={() => void query.fetchNextPage()}
          >
            {query.isFetchingNextPage ? "Loading..." : "Load more"}
          </Button>
        </div>
      )}
    </div>
  );
}

export default ListingListContainer;
