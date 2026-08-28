import { EuroIcon, MapPinIcon, UsersRoundIcon } from "lucide-react";

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
} from "@/shared/components/ui/card";

import type { Listing } from "../model/listing";
import { ListingCardImages } from "./ListingCardImages";

type ListingCardProps = {
  listing: Listing;
};

function ListingCard({ listing }: ListingCardProps) {
  return (
    <Card className="pt-0">
      <div className="relative">
        <ListingCardImages listing={listing} />

        <div className="absolute inset-x-0 top-0 p-4 text-white">
          {listing.name}
        </div>
      </div>

      <CardHeader>
        <CardDescription className="line-clamp-2">
          {listing.description}
        </CardDescription>
      </CardHeader>

      <CardContent className="space-y-3">
        <div className="flex items-center gap-2">
          <EuroIcon className="text-primary size-4" />

          <span>
            <span className="font-semibold">{listing.pricePerNight}</span>
            <span className="text-muted-foreground"> / night</span>
          </span>
        </div>

        <div className="flex items-center gap-2">
          <MapPinIcon className="text-primary size-4" />

          {/* TODO: add location on API side and replace */}
          <span className="text-muted-foreground">Location</span>
        </div>

        <div className="flex items-center gap-2">
          <UsersRoundIcon className="text-primary size-4" />

          <span className="text-muted-foreground">
            {listing.maxGuests} guests
          </span>
        </div>
      </CardContent>
    </Card>
  );
}

export default ListingCard;
