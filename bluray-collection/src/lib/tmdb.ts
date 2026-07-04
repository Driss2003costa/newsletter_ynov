// Client minimal pour l'API TMDB (The Movie Database).
// La clé reste TOUJOURS côté serveur : le navigateur ne la voit jamais,
// il passe par nos routes /api/*.

const TMDB_BASE = "https://api.themoviedb.org/3";

export class TmdbError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = "TmdbError";
    this.status = status;
  }
}

async function tmdbFetch(path: string, params: Record<string, string> = {}) {
  const token = process.env.TMDB_ACCESS_TOKEN?.trim();
  const apiKey = process.env.TMDB_API_KEY?.trim();

  if (!token && !apiKey) {
    throw new TmdbError(
      "Identifiants TMDB manquants. Renseigne TMDB_API_KEY (ou TMDB_ACCESS_TOKEN) dans .env",
      500,
    );
  }

  const url = new URL(TMDB_BASE + path);
  url.searchParams.set("language", "fr-FR");
  for (const [k, v] of Object.entries(params)) url.searchParams.set(k, v);

  const headers: Record<string, string> = { accept: "application/json" };
  if (token) {
    // Jeton v4 (Bearer) prioritaire.
    headers.Authorization = `Bearer ${token}`;
  } else {
    url.searchParams.set("api_key", apiKey!);
  }

  const res = await fetch(url, { headers, cache: "no-store" });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new TmdbError(`Erreur TMDB (${res.status}) ${body}`.trim(), res.status);
  }
  return res.json();
}

export type MovieSearchResult = {
  tmdbId: number;
  title: string;
  originalTitle: string | null;
  year: number | null;
  posterPath: string | null;
  overview: string | null;
  rating: number | null;
};

function yearFromDate(date?: string | null): number | null {
  if (!date) return null;
  const y = parseInt(date.slice(0, 4), 10);
  return Number.isFinite(y) ? y : null;
}

/** Recherche de films par titre. */
export async function searchMovies(query: string): Promise<MovieSearchResult[]> {
  const data = await tmdbFetch("/search/movie", {
    query,
    include_adult: "false",
    page: "1",
  });
  return (data.results ?? []).map((m: any) => ({
    tmdbId: m.id,
    title: m.title || m.original_title || "Sans titre",
    originalTitle: m.original_title ?? null,
    year: yearFromDate(m.release_date),
    posterPath: m.poster_path ?? null,
    overview: m.overview || null,
    rating: typeof m.vote_average === "number" ? Math.round(m.vote_average * 10) / 10 : null,
  }));
}

export type MovieDetails = MovieSearchResult & {
  backdropPath: string | null;
  runtime: number | null;
  genres: string | null;
  director: string | null;
};

/** Détails complets d'un film (durée, genres, réalisateur...). */
export async function getMovieDetails(tmdbId: number): Promise<MovieDetails> {
  const data = await tmdbFetch(`/movie/${tmdbId}`, { append_to_response: "credits" });
  const director =
    data.credits?.crew?.find((c: any) => c.job === "Director")?.name ?? null;
  const genres =
    Array.isArray(data.genres) && data.genres.length
      ? data.genres.map((g: any) => g.name).join(", ")
      : null;

  return {
    tmdbId: data.id,
    title: data.title || data.original_title || "Sans titre",
    originalTitle: data.original_title ?? null,
    year: yearFromDate(data.release_date),
    posterPath: data.poster_path ?? null,
    backdropPath: data.backdrop_path ?? null,
    overview: data.overview || null,
    rating: typeof data.vote_average === "number" ? Math.round(data.vote_average * 10) / 10 : null,
    runtime: typeof data.runtime === "number" && data.runtime > 0 ? data.runtime : null,
    genres,
    director,
  };
}
