import {
  type CursorPage,
  cursorPageSchema,
  type OffsetPage,
  offsetPageSchema,
} from "@/shared/api/pagination";
import { parseResponse } from "@/shared/api/parse";
import { request } from "@/shared/api/request";

import type { Listing } from "../model/listing";
import { type ListingDto, listingDtoSchema } from "./dto";
import { mapListing } from "./mapper";

export async function getListingsCursor(params: {
  limit: number;
  cursor: string | null;
  signal?: AbortSignal;
}): Promise<CursorPage<Listing>> {
  const data = await request<CursorPage<ListingDto>>({
    method: "GET",
    url: "/listings",
    params: {
      pagination: "cursor",
      limit: params.limit,
      cursor: params.cursor,
    },
    signal: params.signal,
  });

  const dto = parseResponse(cursorPageSchema(listingDtoSchema), data);

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
  const data = await request<OffsetPage<ListingDto>>({
    method: "GET",
    url: "/listings",
    params: {
      pagination: "offset",
      limit: params.limit,
      offset: params.offset,
    },
    signal: params.signal,
  });

  const dto = parseResponse(offsetPageSchema(listingDtoSchema), data);

  return {
    items: dto.items.map(mapListing),
    hasNext: dto.hasNext,
    total: dto.total,
  };
}

export async function getListingBySlug(slug: string): Promise<Listing> {
  const data = await request({
    method: "GET",
    url: `/listings/by-slug/${slug}`,
  });

  const dto = parseResponse(listingDtoSchema, data);

  return mapListing(dto);
}
