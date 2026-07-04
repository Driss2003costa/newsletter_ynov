# 🎬 Ma collection Blu-ray

Site web pour cataloguer ma collection de **Blu-ray / 4K UHD / Steelbook / DVD**.
On recherche un film par son titre, on clique, et l'**affiche** + les infos
(année, durée, genres, réalisateur, note) sont récupérées automatiquement via
l'**API TMDB** puis stockées en base.

## Stack

- **Next.js 14** (App Router, TypeScript) — front + routes API dans un seul projet
- **Prisma** + **SQLite** — base de données locale (fichier `prisma/dev.db`)
- **API TMDB** (The Movie Database) — recherche de films et affiches
- **Tailwind CSS** — interface sombre facon cinéma

La clé TMDB reste **toujours côté serveur** : le navigateur passe par les routes
`/api/*`, il ne voit jamais la clé.

## Démarrage

```bash
cd bluray-collection
npm install

# 1) Configurer les variables d'environnement
cp .env.example .env
#   puis éditer .env pour y coller ta clé TMDB (voir plus bas)

# 2) Créer la base de données SQLite + le client Prisma
npx prisma migrate dev --name init

# 3) Lancer le site
npm run dev            # http://localhost:3000
```

## Obtenir une clé TMDB (gratuit)

1. Crée un compte sur https://www.themoviedb.org/
2. Va dans **Paramètres → API** : https://www.themoviedb.org/settings/api
3. Demande une clé (usage « Developer », c'est gratuit)
4. Colle-la dans `.env` :

```env
TMDB_API_KEY="ta_cle_api_v3"
# ou, au choix, le Read Access Token v4 (prioritaire s'il est défini) :
# TMDB_ACCESS_TOKEN="ton_read_access_token_v4"
```

Sans clé, la recherche renvoie une erreur explicite (le reste du site fonctionne).

## Fonctionnement

| Page | Rôle |
| --- | --- |
| **`/`** (Collection) | Grille des affiches, filtres par format, recherche locale, suppression |
| **`/add`** (Ajouter) | Recherche TMDB en direct, choix du format, ajout en un clic |

### Routes API

| Méthode & route | Rôle |
| --- | --- |
| `GET /api/search?q=` | Recherche de films sur TMDB (proxy, clé cachée) |
| `GET /api/collection` | Liste la collection |
| `POST /api/collection` | Ajoute un film (`{ tmdbId, format }`) — récupère les détails sur TMDB |
| `PATCH /api/collection/:id` | Modifie le format ou les notes |
| `DELETE /api/collection/:id` | Retire un film |

### Modèle de données (`prisma/schema.prisma`)

Un modèle `BluRay` : `title`, `year`, `posterPath`, `overview`, `rating`,
`runtime`, `genres`, `director`, `format`, `notes`, `tmdbId` (unique)…

## Outils utiles

```bash
npm run db:studio     # explorer la base dans le navigateur (Prisma Studio)
npm run build         # build de production
npm start             # servir le build
```

## Déploiement

> ⚠️ **SQLite & serverless** — Le fichier SQLite vit sur le disque local. Sur
> une plateforme serverless (Vercel), le système de fichiers est éphémère et en
> lecture seule : la base ne persistera pas entre les requêtes. Pour un
> déploiement en ligne, remplace le `provider` par `postgresql` dans
> `prisma/schema.prisma` et pointe `DATABASE_URL` vers une base Postgres
> (Neon, Supabase, Railway…). En local ou sur un serveur classique
> (VPS, Docker), SQLite fonctionne parfaitement.

## Crédit

Ce produit utilise l'API TMDB mais n'est ni approuvé ni certifié par TMDB.
