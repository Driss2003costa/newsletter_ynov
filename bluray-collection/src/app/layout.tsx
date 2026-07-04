import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Ma collection Blu-ray",
  description: "Catalogue de ma collection de Blu-ray, avec affiches via l'API TMDB.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className="text-cream antialiased">
        <header className="sticky top-0 z-20 border-b border-line/70 bg-ink/80 backdrop-blur">
          <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3">
            <Link href="/" className="flex items-center gap-2 text-lg font-semibold tracking-tight">
              <span className="grid h-8 w-8 place-items-center rounded-md bg-blu/20 text-blu">🎬</span>
              <span>Ma collection <span className="text-blu">Blu-ray</span></span>
            </Link>
            <nav className="flex items-center gap-1 text-sm">
              <Link
                href="/"
                className="rounded-md px-3 py-1.5 text-muted transition-colors hover:bg-panel hover:text-cream"
              >
                Collection
              </Link>
              <Link
                href="/add"
                className="rounded-md bg-blu px-3 py-1.5 font-medium text-white transition-colors hover:bg-blu/90"
              >
                + Ajouter
              </Link>
            </nav>
          </div>
        </header>

        <main className="mx-auto max-w-6xl px-4 py-8">{children}</main>

        <footer className="mx-auto max-w-6xl px-4 py-10 text-center text-xs text-muted">
          Données & affiches fournies par{" "}
          <a
            href="https://www.themoviedb.org/"
            target="_blank"
            rel="noreferrer"
            className="text-blu hover:underline"
          >
            The Movie Database (TMDB)
          </a>
          . Ce produit n'est ni approuvé ni certifié par TMDB.
        </footer>
      </body>
    </html>
  );
}
