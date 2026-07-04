// Helpers d'URL d'images TMDB — module pur (utilisable côté client).

/** Base des images TMDB. Tailles utiles : w185, w342, w500, original. */
export const TMDB_IMG = "https://image.tmdb.org/t/p";

export function posterUrl(
  path: string | null | undefined,
  size: "w185" | "w342" | "w500" | "original" = "w500",
): string | null {
  if (!path) return null;
  return `${TMDB_IMG}/${size}${path}`;
}
