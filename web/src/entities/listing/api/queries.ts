import { infiniteQueryOptions } from "@tanstack/react-query";

import { getListingsCursor } from "./api";

const LISTINGS_PAGE_SIZE = 20;

export const listingsQuery = infiniteQueryOptions({
  queryKey: ["listings"],

  queryFn: ({ pageParam, signal }) =>
    getListingsCursor({
      limit: LISTINGS_PAGE_SIZE,
      cursor: pageParam,
      signal,
    }),

  initialPageParam: null as string | null,

  getNextPageParam: (lastPage) => lastPage.nextCursor,
});
