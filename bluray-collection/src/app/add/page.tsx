"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import Link from "next/link";
import { Poster } from "@/components/Poster";
import { FORMATS, DEFAULT_FORMAT } from "@/lib/formats";

type Result = {
  tmdbId: number;
  title: string;
  originalTitle: string | null;
  year: number | null;
  posterPath: string | null;
  overview: string | null;
  rating: number | null;
};

type AddState = "idle" | "adding" | "added" | "exists" | "error";

export default function AddPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Result[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [format, setFormat] = useState<string>(DEFAULT_FORMAT);
  const [states, setStates] = useState<Record<number, AddState>>({});
  const [searched, setSearched] = useState(false);

  // tmdbId déjà présents dans la collection (chargés au montage).
  const [owned, setOwned] = useState<Set<number>>(new Set());

  useEffect(() => {
    fetch("/api/collection")
      .then((r) => (r.ok ? r.json() : { items: [] }))
      .then((data) => {
        const ids = (data.items ?? [])
          .map((i: { tmdbId: number | null }) => i.tmdbId)
          .filter((x: number | null): x is number => x != null);
        setOwned(new Set<number>(ids));
      })
      .catch(() => {});
  }, []);

  // Recherche avec anti-rebond (debounce 400ms).
  const abortRef = useRef<AbortController | null>(null);
  useEffect(() => {
    const q = query.trim();
    if (q.length < 2) {
      setResults([]);
      setSearched(false);
      setError(null);
      return;
    }
    const timer = setTimeout(async () => {
      abortRef.current?.abort();
      const ctrl = new AbortController();
      abortRef.current = ctrl;
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`, { signal: ctrl.signal });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || "Erreur de recherche");
        setResults(data.results ?? []);
        setSearched(true);
      } catch (e: any) {
        if (e?.name !== "AbortError") {
          setError(e?.message || "Erreur de recherche");
          setResults([]);
        }
      } finally {
        setLoading(false);
      }
    }, 400);
    return () => clearTimeout(timer);
  }, [query]);

  const add = useCallback(
    async (r: Result) => {
      setStates((s) => ({ ...s, [r.tmdbId]: "adding" }));
      try {
        const res = await fetch("/api/collection", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ tmdbId: r.tmdbId, format }),
        });
        if (res.status === 409) {
          setStates((s) => ({ ...s, [r.tmdbId]: "exists" }));
          setOwned((prev) => new Set(prev).add(r.tmdbId));
          return;
        }
        if (!res.ok) throw new Error();
        setStates((s) => ({ ...s, [r.tmdbId]: "added" }));
        setOwned((prev) => new Set(prev).add(r.tmdbId));
      } catch {
        setStates((s) => ({ ...s, [r.tmdbId]: "error" }));
      }
    },
    [format],
  );

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Ajouter un film</h1>
          <p className="text-sm text-muted">Recherche par titre, puis clique pour ajouter à ta collection.</p>
        </div>
        <label className="flex items-center gap-2 text-sm text-muted">
          Format
          <select
            value={format}
            onChange={(e) => setFormat(e.target.value)}
            className="rounded-md border border-line bg-panel px-2 py-1.5 text-cream focus:border-blu focus:outline-none"
          >
            {FORMATS.map((f) => (
              <option key={f} value={f}>
                {f}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className="relative mb-6">
        <input
          autoFocus
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ex : Inception, Le Parrain, Dune…"
          className="w-full rounded-lg border border-line bg-panel px-4 py-3 text-cream placeholder:text-muted focus:border-blu focus:outline-none"
        />
        {loading && (
          <span className="absolute right-4 top-1/2 -translate-y-1/2 text-sm text-muted">Recherche…</span>
        )}
      </div>

      {error && (
        <div className="mb-6 rounded-md border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-300">
          {error}
          <span className="mt-1 block text-xs text-red-300/70">
            Astuce : vérifie que ta clé TMDB est bien renseignée dans le fichier <code>.env</code>.
          </span>
        </div>
      )}

      {!searched && !loading && query.trim().length < 2 && (
        <p className="py-16 text-center text-sm text-muted">Commence à taper un titre pour lancer la recherche.</p>
      )}

      {searched && !loading && results.length === 0 && !error && (
        <p className="py-16 text-center text-sm text-muted">Aucun résultat pour « {query} ».</p>
      )}

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        {results.map((r) => {
          const state: AddState = states[r.tmdbId] ?? (owned.has(r.tmdbId) ? "exists" : "idle");
          return (
            <div key={r.tmdbId} className="group flex flex-col">
              <div className="relative aspect-[2/3] overflow-hidden rounded-lg border border-line bg-panel shadow-poster">
                <Poster path={r.posterPath} title={r.title} />
                {r.rating != null && r.rating > 0 && (
                  <span className="absolute left-2 top-2 rounded bg-black/70 px-1.5 py-0.5 text-xs font-semibold text-gold">
                    ★ {r.rating.toFixed(1)}
                  </span>
                )}
              </div>

              <div className="mt-2 flex-1">
                <p className="line-clamp-1 text-sm font-medium" title={r.title}>
                  {r.title}
                </p>
                <p className="text-xs text-muted">{r.year ?? "—"}</p>
              </div>

              <button
                onClick={() => add(r)}
                disabled={state === "adding" || state === "added" || state === "exists"}
                className={`mt-2 w-full rounded-md px-2 py-1.5 text-xs font-medium transition-colors ${
                  state === "added"
                    ? "bg-green-600/20 text-green-400"
                    : state === "exists"
                      ? "cursor-default bg-panel2 text-muted"
                      : state === "error"
                        ? "bg-red-600/20 text-red-300 hover:bg-red-600/30"
                        : "bg-blu text-white hover:bg-blu/90 disabled:opacity-60"
                }`}
              >
                {state === "adding" && "Ajout…"}
                {state === "added" && "✓ Ajouté"}
                {state === "exists" && "Déjà dans la collection"}
                {state === "error" && "Erreur — réessayer"}
                {state === "idle" && "+ Ajouter"}
              </button>
            </div>
          );
        })}
      </div>

      <div className="mt-10 text-center">
        <Link href="/" className="text-sm text-blu hover:underline">
          ← Retour à ma collection
        </Link>
      </div>
    </div>
  );
}
