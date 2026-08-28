export interface Listing {
  id: string;
  slug: string;
  name: string;
  description: string;
  pricePerNight: number;
  maxGuests: number;
  createdAt: Date;
  updatedAt: Date;
  images: ListingImage[];
}

export interface ListingImage {
  id: string;
  url: string;
  contentType: string;
  position: number;
  createdAt: Date;
  updatedAt: Date;
}
