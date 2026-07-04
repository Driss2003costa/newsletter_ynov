// Représentation d'un titre de la collection, sérialisable (dates en ISO string)
// pour passer du serveur aux composants clients.
export type BluRayItem = {
  id: number;
  tmdbId: number | null;
  title: string;
  originalTitle: string | null;
  year: number | null;
  posterPath: string | null;
  backdropPath: string | null;
  overview: string | null;
  rating: number | null;
  runtime: number | null;
  genres: string | null;
  director: string | null;
  format: string;
  notes: string | null;
  createdAt: string;
};
