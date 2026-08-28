import type { ListingDto } from "../api/dto";
import type { Listing, ListingImage } from "../model/listing";

function mapListingImage(dto: ListingDto["images"][number]): ListingImage {
  return {
    id: dto.id,
    url: dto.url,
    contentType: dto.contentType,
    position: dto.position,
    createdAt: new Date(dto.createdAt),
    updatedAt: new Date(dto.updatedAt),
  };
}

export function mapListing(dto: ListingDto): Listing {
  return {
    id: dto.id,
    slug: dto.slug,
    name: dto.name,
    description: dto.description,
    pricePerNight: Number(dto.pricePerNight),
    maxGuests: dto.maxGuests,
    createdAt: new Date(dto.createdAt),
    updatedAt: new Date(dto.updatedAt),
    images: dto.images.map(mapListingImage),
  };
}
