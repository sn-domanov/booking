import { z } from "zod";

export const offsetPageSchema = <T extends z.ZodType>(itemSchema: T) =>
  z.object({
    items: z.array(itemSchema),
    hasNext: z.boolean(),
    total: z.number().int().nonnegative(),
  });

export type OffsetPage<T> = {
  items: T[];
  hasNext: boolean;
  total: number;
};

export const cursorPageSchema = <T extends z.ZodType>(itemSchema: T) =>
  z.object({
    items: z.array(itemSchema),
    nextCursor: z.string().nullable(),
  });

export type CursorPage<T> = {
  items: T[];
  nextCursor: string | null;
};
