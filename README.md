# Newsletter Ynov — Studio d'envoi

Dashboard admin pour **composer et envoyer des emails à partir de templates prédéfinis**.
Tu choisis un template, tu saisis une (ou plusieurs) adresse, tu édites le contenu, tu
prévisualises le rendu comme une œuvre encadrée, puis tu envoies.

Direction artistique : **« musée »** — galerie épurée, grands blancs, typographies serif,
filets fins, petites capitales, palette crème / encre / oxblood.

## Stack

- React 18 + Vite + TypeScript
- Tailwind CSS 3 (palette « musée » sur mesure)
- React Router v6 · Zustand (`persist`, localStorage) · Lucide React
- **Resend** via une **fonction serverless Vercel** (`api/send.ts`) pour l'envoi réel

## Démarrage

```bash
cd newsletter_ynov
npm install
npm run dev          # http://localhost:5174  (UI seule → mode démo)
```

En `npm run dev`, il n'y a pas de backend : l'app détecte l'absence de `/api/send`
et bascule en **mode démo** (aperçu + journal OK, aucun email envoyé).

### Envoi réel en local

```bash
npm i -g vercel
vercel dev           # sert aussi la fonction /api/send
```

## Envoi des emails (Resend)

1. Crée une clé sur https://resend.com/api-keys
2. Copie `.env.example` en `.env` et renseigne `RESEND_API_KEY`
   (ou configure-la dans Vercel → Settings → Environment Variables)
3. Vérifie ton domaine d'envoi dans Resend (ou utilise `onboarding@resend.dev` pour tester)

Sans clé, la fonction `/api/send` répond en **mode démo** : le flux est validé,
mais aucun email ne part. Aucun secret n'est jamais exposé côté navigateur —
la clé reste dans la fonction serverless.

## Pages

| Page | Rôle |
| --- | --- |
| **Tableau de bord** | Vue d'ensemble, stats, journal d'envoi |
| **Composer** | Panneau d'envoi : template → destinataires → contenu → aperçu → envoi |
| **Templates** | Galerie des modèles avec aperçu en grand |
| **Paramètres** | Expéditeur par défaut, statut Resend, journal |

## Templates inclus

1. **Invitation — Vernissage** (carton d'invitation : étiquette, date/lieu en cartel, RSVP)
2. **Bienvenue** (accueil sobre, une action)
3. **Programme du mois** (newsletter en rubriques numérotées, façon catalogue)

Chaque template vit dans `src/templates/`. Les briques de rendu (tables + styles inline,
compatibles clients mail) sont dans `src/templates/shell.ts`.

### Ajouter / modifier un template

Crée un fichier dans `src/templates/` qui exporte un objet `EmailTemplate`
(`id`, `name`, `category`, `defaultSubject`, `fields[]`, `render(vars)`), puis ajoute-le
au registre dans `src/templates/index.ts`. Les `fields` deviennent automatiquement des
champs éditables dans le Composer.

## Déploiement Vercel

`npm run build` produit `dist/`. La fonction `api/send.ts` est déployée automatiquement.
N'oublie pas de définir `RESEND_API_KEY` dans les variables d'environnement du projet.

---

> Les textes des templates sont des **exemples** : remplace-les par tes textes prédéfinis.
> Le style s'affinera avec ton moodboard (couleurs, typographies, visuels).
