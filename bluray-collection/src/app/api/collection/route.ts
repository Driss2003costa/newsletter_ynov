import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getMovieDetails, TmdbError } from "@/lib/tmdb";
import { DEFAULT_FORMAT, isFormat } from "@/lib/formats";

export const dynamic = "force-dynamic";

// GET /api/collection → liste complète de la collection
export async function GET() {
  const items = await prisma.bluRay.findMany({ orderBy: { createdAt: "desc" } });
  return NextResponse.json({ items });
}

// POST /api/collection → ajoute un film
// Corps attendu : { tmdbId: number, format?: string, notes?: string }
// ou (saisie manuelle) : { title: string, year?, posterPath?, format? }
export async function POST(req: NextRequest) {
  let body: any;
  try {
    body = await req.json();
  } catch {
    return NextResponse.json({ error: "Corps JSON invalide" }, { status: 400 });
  }

  const format = isFormat(body?.format) ? body.format : DEFAULT_FORMAT;
  const notes = typeof body?.notes === "string" ? body.notes.trim() || null : null;

  try {
    // Cas 1 : ajout depuis TMDB (recherche + clic)
    if (body?.tmdbId != null) {
      const tmdbId = Number(body.tmdbId);
      if (!Number.isInteger(tmdbId)) {
        return NextResponse.json({ error: "tmdbId invalide" }, { status: 400 });
      }

      const existing = await prisma.bluRay.findUnique({ where: { tmdbId } });
      if (existing) {
        return NextResponse.json(
          { error: "Ce film est déjà dans ta collection", item: existing },
          { status: 409 },
        );
      }

      const d = await getMovieDetails(tmdbId);
      const item = await prisma.bluRay.create({
        data: {
          tmdbId: d.tmdbId,
          title: d.title,
          originalTitle: d.originalTitle,
          year: d.year,
          posterPath: d.posterPath,
          backdropPath: d.backdropPath,
          overview: d.overview,
          rating: d.rating,
          runtime: d.runtime,
          genres: d.genres,
          director: d.director,
          format,
          notes,
        },
      });
      return NextResponse.json({ item }, { status: 201 });
    }

    // Cas 2 : saisie manuelle (sans TMDB)
    const title = typeof body?.title === "string" ? body.title.trim() : "";
    if (!title) {
      return NextResponse.json({ error: "Titre requis" }, { status: 400 });
    }
    const item = await prisma.bluRay.create({
      data: {
        title,
        year: Number.isInteger(body?.year) ? body.year : null,
        posterPath: typeof body?.posterPath === "string" ? body.posterPath : null,
        overview: typeof body?.overview === "string" ? body.overview : null,
        format,
        notes,
      },
    });
    return NextResponse.json({ item }, { status: 201 });
  } catch (err) {
    const status = err instanceof TmdbError ? err.status : 500;
    const message = err instanceof Error ? err.message : "Erreur serveur";
    return NextResponse.json({ error: message }, { status });
  }
}
