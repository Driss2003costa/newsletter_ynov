import { NextRequest, NextResponse } from "next/server";
import { searchMovies, TmdbError } from "@/lib/tmdb";

// Proxy vers TMDB : garde la clé API côté serveur.
export const dynamic = "force-dynamic";

export async function GET(req: NextRequest) {
  const q = req.nextUrl.searchParams.get("q")?.trim();
  if (!q) return NextResponse.json({ results: [] });

  try {
    const results = await searchMovies(q);
    return NextResponse.json({ results });
  } catch (err) {
    const status = err instanceof TmdbError ? err.status : 502;
    const message = err instanceof Error ? err.message : "Erreur inconnue";
    return NextResponse.json({ error: message }, { status });
  }
}
