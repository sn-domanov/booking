import { apiClient } from "@/shared/api/client";
import {
  type CursorPage,
  cursorPageSchema,
  type OffsetPage,
  offsetPageSchema,
} from "@/shared/api/pagination";

import type { Listing } from "../model/listing";
import { listingDtoSchema } from "./dto";
import { mapListing } from "./mapper";

export async function getListingsCursor(params: {
  limit: number;
  cursor: string | null;
  signal?: AbortSignal;
}): Promise<CursorPage<Listing>> {
  const response = await apiClient.get("/listings", {
    params: {
      pagination: "cursor",
      limit: params.limit,
      cursor: params.cursor,
    },
    signal: params.signal,
  });

  const dto = cursorPageSchema(listingDtoSchema).parse(response.data);

  return {
    items: dto.items.map(mapListing),
    nextCursor: dto.nextCursor,
  };
}

export async function getListingsOffset(params: {
  limit: number;
  offset: number;
  signal?: AbortSignal;
}): Promise<OffsetPage<Listing>> {
  const response = await apiClient.get("/listings", {
    params: {
      pagination: "offset",
      limit: params.limit,
      offset: params.offset,
    },
    signal: params.signal,
  });

  const dto = offsetPageSchema(listingDtoSchema).parse(response.data);

  return {
    items: dto.items.map(mapListing),
    hasNext: dto.hasNext,
    total: dto.total,
  };
}

export async function getListingBySlug(slug: string): Promise<Listing> {
  const response = await apiClient.get(
    `/listings/by-slug/${encodeURIComponent(slug)}`,
  );

  const dto = listingDtoSchema.parse(response.data);

  return mapListing(dto);
}
