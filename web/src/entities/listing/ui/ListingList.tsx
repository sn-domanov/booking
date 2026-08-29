import type { Listing } from "../model/listing";
import ListingCard from "./ListingCard";
import { ListingCardSkeleton } from "./ListingCardSkeleton";

type ListingListProps = {
  listings: Listing[];
  isLoading: boolean;
};

export function ListingList({ listings, isLoading }: ListingListProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {Array.from({ length: 8 }, (_, index) => (
          <ListingCardSkeleton key={index} />
        ))}
      </div>
    );
  }

  if (listings.length === 0) {
    return <p>No listings found.</p>;
  }

  return (
    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {listings.map((listing) => (
        <ListingCard key={listing.id} listing={listing} />
      ))}
    </div>
  );
}
