import { useState } from "react";

import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/shared/components/ui/carousel";

import type { Listing } from "../model/listing";

type ListingCardImagesProps = {
  listing: Listing;
};

export function ListingCardImages({ listing }: ListingCardImagesProps) {
  const [isHovering, setIsHovering] = useState(false);

  return (
    <Carousel
      className="w-full"
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      <CarouselContent>
        {listing.images.map((image, index) => (
          <CarouselItem key={image.id}>
            <img
              src={image.url}
              alt={`${listing.name} image ${index + 1}`}
              className="aspect-video w-full object-cover dark:brightness-75"
            />
          </CarouselItem>
        ))}
      </CarouselContent>

      {isHovering && (
        <>
          <CarouselPrevious className="left-4" variant="secondary" />
          <CarouselNext className="right-4" variant="secondary" />
        </>
      )}
    </Carousel>
  );
}
