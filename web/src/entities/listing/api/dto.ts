import { z } from "zod";

export const listingImageDtoSchema = z.object({
  id: z.uuid(),
  url: z.url(),
  contentType: z.string(),
  position: z.number().int(),
  createdAt: z.iso.datetime(),
  updatedAt: z.iso.datetime(),
});

export const listingDtoSchema = z.object({
  id: z.uuid(),
  slug: z.string(),
  name: z.string(),
  description: z.string(),
  pricePerNight: z.string(),
  maxGuests: z.number().int(),
  createdAt: z.iso.datetime(),
  updatedAt: z.iso.datetime(),
  images: z.array(listingImageDtoSchema),
});

export type ListingDto = z.infer<typeof listingDtoSchema>;
