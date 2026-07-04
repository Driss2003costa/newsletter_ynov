"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { Poster } from "./Poster";
import type { BluRayItem } from "@/lib/types";
import { FORMATS } from "@/lib/formats";

function chipClass(active: boolean) {
  return `rounded-full border px-3 py-1 text-xs transition-colors ${
    active ? "border-blu bg-blu/15 text-blu" : "border-line text-muted hover:text-cream"
  }`;
}

export function CollectionGrid({ initialItems }: { initialItems: BluRayItem[] }) {
  const [items, setItems] = useState<BluRayItem[]>(initialItems);
  const [query, setQuery] = useState("");
  const [formatFilter, setFormatFilter] = useState<string>("all");
  const [deleting, setDeleting] = useState<number | null>(null);

  const counts = useMemo(() => {
    const m = new Map<string, number>();
    for (const it of items) m.set(it.format, (m.get(it.format) ?? 0) + 1);
    return m;
  }, [items]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return items.filter((it) => {
      if (formatFilter !== "all" && it.format !== formatFilter) return false;
      if (!q) return true;
      return (
        it.title.toLowerCase().includes(q) ||
        (it.originalTitle?.toLowerCase().includes(q) ?? false) ||
        (it.director?.toLowerCase().includes(q) ?? false)
      );
    });
  }, [items, query, formatFilter]);

  async function remove(it: BluRayItem) {
    if (!window.confirm(`Retirer « ${it.title} » de ta collection ?`)) return;
    setDeleting(it.id);
    try {
      const res = await fetch(`/api/collection/${it.id}`, { method: "DELETE" });
      if (res.ok) {
        setItems((prev) => prev.filter((x) => x.id !== it.id));
      } else {
        window.alert("Suppression impossible.");
      }
    } catch {
      window.alert("Erreur réseau lors de la suppression.");
    } finally {
      setDeleting(null);
    }
  }

  if (items.length === 0) {
    return (
      <div className="grid place-items-center rounded-xl border border-dashed border-line py-24 text-center">
        <div className="text-5xl">🎬</div>
        <h2 className="mt-4 text-xl font-semibold">Ta collection est vide</h2>
        <p className="mt-1 max-w-sm text-sm text-muted">
          Recherche un film et ajoute-le en un clic. Les affiches et infos sont
          récupérées automatiquement via TMDB.
        </p>
        <Link
          href="/add"
          className="mt-5 rounded-md bg-blu px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blu/90"
        >
          + Ajouter un premier Blu-ray
        </Link>
      </div>
    );
  }

  return (
    <div>
      <div className="mb-5 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Ma collection</h1>
          <p className="text-sm text-muted">
            {items.length} titre{items.length > 1 ? "s" : ""}
          </p>
        </div>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Filtrer par titre, réalisateur…"
          className="w-full max-w-xs rounded-md border border-line bg-panel px-3 py-2 text-sm text-cream placeholder:text-muted focus:border-blu focus:outline-none"
        />
      </div>

      <div className="mb-6 flex flex-wrap gap-2">
        <button className={chipClass(formatFilter === "all")} onClick={() => setFormatFilter("all")}>
          Tous · {items.length}
        </button>
        {FORMATS.filter((f) => counts.get(f)).map((f) => (
          <button key={f} className={chipClass(formatFilter === f)} onClick={() => setFormatFilter(f)}>
            {f} · {counts.get(f)}
          </button>
        ))}
      </div>

      {filtered.length === 0 ? (
        <p className="py-16 text-center text-sm text-muted">Aucun titre ne correspond à ce filtre.</p>
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
          {filtered.map((it) => (
            <div key={it.id} className="group">
              <div className="relative aspect-[2/3] overflow-hidden rounded-lg border border-line bg-panel shadow-poster">
                <Poster path={it.posterPath} title={it.title} />

                {it.rating != null && it.rating > 0 && (
                  <span className="absolute left-2 top-2 rounded bg-black/70 px-1.5 py-0.5 text-xs font-semibold text-gold">
                    ★ {it.rating.toFixed(1)}
                  </span>
                )}

                <span className="absolute bottom-2 left-2 rounded bg-blu/90 px-1.5 py-0.5 text-[11px] font-medium text-white">
                  {it.format}
                </span>

                <button
                  onClick={() => remove(it)}
                  disabled={deleting === it.id}
                  aria-label={`Retirer ${it.title}`}
                  className="absolute right-2 top-2 grid h-7 w-7 place-items-center rounded-full bg-black/70 text-sm text-cream opacity-0 transition-all hover:bg-red-600 group-hover:opacity-100 disabled:opacity-50"
                >
                  {deleting === it.id ? "…" : "✕"}
                </button>
              </div>

              <div className="mt-2">
                <p className="line-clamp-1 text-sm font-medium" title={it.title}>
                  {it.title}
                </p>
                <p className="text-xs text-muted">
                  {[it.year, it.runtime ? `${it.runtime} min` : null].filter(Boolean).join(" · ") || "—"}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
