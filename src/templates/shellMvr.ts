/**
 * Thème email « Musée de la Vie Romantique » (MVR).
 *
 * Même philosophie que `shell.ts` (tables imbriquées + styles inline pour la
 * compatibilité clients mail, polices web-safe), mais avec l'identité du musée
 * tirée du moodboard : palette vert sauge / mauve / charbon / crème, masthead
 * monogramme MVR, esprit « galerie / exposition d'art » moderne.
 *
 * On réutilise `esc` / `nl2br` de `shell.ts` (pas de duplication).
 */
import { esc, nl2br } from './shell'

/** Palette MVR (issue du moodboard). */
const C = {
  canvas: '#ECE8DF', // crème (fond extérieur)
  paper: '#FBFAF6', // ivoire (carte)
  ink: '#2E2F29', // charbon (titres)
  body: '#45463F', // gris encre (corps)
  muted: '#8C8E82', // sauge-gris (labels secondaires)
  line: '#DBDCD1', // filet
  sage: '#7C9A77', // vert sauge (accent structurel)
  sageDeep: '#4E6B49', // sauge profond (boutons — contraste AA)
  sageBg: '#EEF2EA', // fond sauge très clair
  mauve: '#856E90', // mauve (accent romantique, lisible)
  mauveBg: '#F1ECF3', // fond mauve très clair
}

const SERIF = "Georgia, 'Times New Roman', Times, serif"
const SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"

/**
 * URL du logo affiché dans l'en-tête des emails.
 *
 * - En préversion locale (vite-node) et avec `vercel dev`, ce chemin relatif
 *   suffit : le fichier est servi depuis `public/logo-mvr.png`.
 * - Pour de VRAIS envois, les clients mail ne savent pas charger « localhost » :
 *   l'image doit être une URL ABSOLUE publique. Une fois le site déployé sur
 *   Vercel, remplace par l'URL complète, ex. :
 *     export const LOGO_MVR = 'https://ton-app.vercel.app/logo-mvr.png'
 */
export const LOGO_MVR = '/logo-mvr.png'

type Accent = 'mauve' | 'sage'
const accentColor = (a: Accent = 'mauve') => (a === 'sage' ? C.sage : C.mauve)

/** Petite étiquette en petites capitales espacées (accent mauve ou sauge). */
export function eyebrow(text: string, accent: Accent = 'mauve'): string {
  if (!text) return ''
  return `<p style="margin:0 0 16px;font-family:${SANS};font-size:11px;line-height:1.5;letter-spacing:3.5px;text-transform:uppercase;color:${accentColor(accent)};">${esc(text)}</p>`
}

/** Titre principal, serif. */
export function headline(text: string): string {
  if (!text) return ''
  return `<h1 style="margin:0 0 10px;font-family:${SERIF};font-weight:400;font-size:32px;line-height:1.18;letter-spacing:0.2px;color:${C.ink};">${esc(text)}</h1>`
}

/** Sous-titre / chapô serif italique. */
export function subhead(text: string): string {
  if (!text) return ''
  return `<p style="margin:0 0 6px;font-family:${SERIF};font-style:italic;font-size:18px;line-height:1.5;color:${C.muted};">${esc(text)}</p>`
}

/** Paragraphe d'introduction (légèrement plus grand). */
export function lead(text: string): string {
  if (!text) return ''
  return `<p style="margin:0 0 18px;font-family:${SANS};font-size:16px;line-height:1.8;color:${C.body};">${nl2br(text)}</p>`
}

/** Paragraphe de corps. */
export function paragraph(text: string): string {
  if (!text) return ''
  return `<p style="margin:0 0 18px;font-family:${SANS};font-size:15px;line-height:1.78;color:${C.body};">${nl2br(text)}</p>`
}

/** Filet fin pleine largeur. */
export function rule(): string {
  return `<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="border-top:1px solid ${C.line};font-size:0;line-height:0;height:1px;">&nbsp;</td></tr></table>`
}

/** Séparateur décoratif centré (filet — losange — filet). */
export function ornament(): string {
  return `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:8px 0;"><tr>
    <td style="border-top:1px solid ${C.line};font-size:0;line-height:0;">&nbsp;</td>
    <td width="30" style="padding:0 12px;text-align:center;font-family:${SERIF};font-size:12px;line-height:1;color:${C.sage};">&#10022;</td>
    <td style="border-top:1px solid ${C.line};font-size:0;line-height:0;">&nbsp;</td>
  </tr></table>`
}

/** Espace vertical. */
export function spacer(h = 24): string {
  return `<div style="height:${h}px;line-height:${h}px;font-size:0;">&nbsp;</div>`
}

/** Sous-titre de section : court filet sauge + label en petites capitales. */
export function sectionTitle(text: string): string {
  if (!text) return ''
  return `<table role="presentation" cellpadding="0" cellspacing="0" style="margin:28px 0 12px;"><tr><td style="width:36px;border-top:2px solid ${C.sage};font-size:0;line-height:0;height:2px;">&nbsp;</td></tr></table>
  <p style="margin:0 0 12px;font-family:${SANS};font-size:13px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:${C.ink};">${esc(text)}</p>`
}

/**
 * Liste à puces. Une ligne = un item.
 * Si la ligne commence déjà par un emoji/symbole, il sert de puce ; sinon on
 * ajoute un petit carré sauge.
 */
export function featureLines(text: string): string {
  const lines = text.split('\n').map((s) => s.trim()).filter(Boolean)
  if (!lines.length) return ''
  const rows = lines
    .map((line) => {
      const ownMarker = !/^[A-Za-z0-9À-ÖØ-öø-ÿ]/.test(line)
      if (ownMarker) {
        return `<tr><td style="padding:7px 0;font-family:${SANS};font-size:15px;line-height:1.65;color:${C.body};">${nl2br(line)}</td></tr>`
      }
      return `<tr>
        <td width="20" valign="top" style="padding:8px 0 7px;font-family:${SANS};font-size:13px;line-height:1.5;color:${C.sage};">&#9642;</td>
        <td style="padding:7px 0;font-family:${SANS};font-size:15px;line-height:1.65;color:${C.body};">${nl2br(line)}</td>
      </tr>`
    })
    .join('')
  return `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:2px 0 14px;">${rows}</table>`
}

/** Bouton plein, sauge profond (CTA principal), centré. */
export function button(label: string, url: string): string {
  if (!label || !url) return ''
  return `<table role="presentation" cellpadding="0" cellspacing="0" align="center" style="margin:10px auto;"><tr><td style="background:${C.sageDeep};">
    <a href="${esc(url)}" target="_blank" style="display:inline-block;padding:15px 34px;font-family:${SANS};font-size:12px;font-weight:600;letter-spacing:2.5px;text-transform:uppercase;color:#FBFAF6;text-decoration:none;">${esc(label)}</a>
  </td></tr></table>`
}

/** « Cartel » d'exposition : lignes label (sauge) / valeur (serif), centrées. */
export function cartel(items: { label: string; value: string }[]): string {
  const list = items.filter((i) => i.value)
  if (!list.length) return ''
  const rows = list
    .map((i, idx) => {
      const last = idx === list.length - 1
      return `<tr><td align="center" style="padding:14px 8px;${last ? '' : `border-bottom:1px solid ${C.line};`}">
        <div style="font-family:${SANS};font-size:10px;letter-spacing:3px;text-transform:uppercase;color:${C.sage};">${esc(i.label)}</div>
        <div style="margin-top:5px;font-family:${SERIF};font-size:17px;color:${C.ink};">${esc(i.value)}</div>
      </td></tr>`
    })
    .join('')
  return `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0;border-top:1px solid ${C.line};border-bottom:1px solid ${C.line};">${rows}</table>`
}

/** Encart code promo (fond sauge clair, bordure pointillée, code en grand). */
export function promoBox(label: string, code: string): string {
  if (!code) return ''
  return `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:8px 0 6px;"><tr><td align="center" style="background:${C.sageBg};border:1px dashed ${C.sage};padding:22px 16px;">
    ${label ? `<div style="margin:0 0 8px;font-family:${SANS};font-size:11px;letter-spacing:2px;text-transform:uppercase;color:${C.body};">${esc(label)}</div>` : ''}
    <div style="font-family:${SERIF};font-size:27px;letter-spacing:5px;color:${C.sageDeep};">${esc(code)}</div>
  </td></tr></table>`
}

/** Petite note centrée discrète. */
export function note(text: string): string {
  if (!text) return ''
  return `<p style="margin:14px 0 0;font-family:${SANS};font-size:12px;line-height:1.6;color:${C.muted};text-align:center;">${nl2br(text)}</p>`
}

/** Signature serif italique. */
export function signature(text: string): string {
  if (!text) return ''
  return `<p style="margin:18px 0 0;font-family:${SERIF};font-style:italic;font-size:16px;line-height:1.5;color:${C.ink};">${nl2br(text)}</p>`
}

interface ShellOpts {
  preheader?: string
  /** Nom affiché (masthead + pied de page). */
  brand?: string
  /** Monogramme du masthead (ex. « MVR »). Mettre '' pour n'afficher que le nom. */
  monogram?: string
  /** URL d'un logo image hébergé : remplace le monogramme typographique. */
  logoUrl?: string
  /** Couleur de fond d'une « plaque » derrière le logo (utile pour un logo clair/blanc). */
  logoBg?: string
  /** Couleur d'accent (liseré haut de carte). */
  accent?: Accent
  /** Adresse postale (pied de page). '' pour masquer. */
  address?: string
  /** Réseaux sociaux, texte libre (pied de page). '' pour masquer. */
  socials?: string
  /** Texte du lien de gestion des préférences. */
  preferences?: string
}

/** Squelette complet de l'email MVR. */
export function emailShellMvr(body: string, opts: ShellOpts = {}): string {
  const brand = opts.brand || 'Musée de la Vie Romantique'
  const monogram = opts.monogram ?? 'MVR'
  const accent = accentColor(opts.accent || 'mauve')
  const address = opts.address ?? '16 rue Chaptal, 75009 Paris'
  const socials = opts.socials ?? 'Facebook&nbsp;·&nbsp;Instagram&nbsp;·&nbsp;X'
  const preferences = opts.preferences ?? 'Mettre à jour mes préférences'

  let mark: string
  let showWordmark = true
  if (opts.logoUrl) {
    const w = opts.logoBg ? 130 : 160
    const img = `<img src="${esc(opts.logoUrl)}" width="${w}" alt="${esc(brand)}" style="display:block;margin:0 auto;border:0;width:${w}px;max-width:${w}px;height:auto;" />`
    mark = opts.logoBg
      ? `<table role="presentation" cellpadding="0" cellspacing="0" align="center" style="margin:0 auto;"><tr><td style="background:${opts.logoBg};padding:18px 22px;border-radius:10px;">${img}</td></tr></table>`
      : img
  } else if (monogram) {
    mark = `<div style="font-family:${SERIF};font-size:30px;letter-spacing:8px;color:${C.ink};line-height:1;">${esc(monogram)}</div>`
  } else {
    mark = `<div style="font-family:${SERIF};font-size:22px;letter-spacing:2px;color:${C.ink};">${esc(brand)}</div>`
    showWordmark = false
  }
  const wordmark =
    showWordmark && brand
      ? `<div style="margin-top:11px;font-family:${SANS};font-size:10px;letter-spacing:4px;text-transform:uppercase;color:${C.muted};">${esc(brand)}</div>`
      : ''
  const masthead = mark + wordmark

  const footer = [
    `<div style="font-family:${SERIF};font-size:13px;color:${C.ink};">${esc(brand)}</div>`,
    address ? `<div style="margin-top:4px;">${esc(address)}</div>` : '',
    socials ? `<div style="margin-top:8px;">${socials}</div>` : '',
    `<div style="margin-top:12px;">
      <a href="#" style="color:${C.muted};text-decoration:underline;">Se désabonner</a>
      &nbsp;·&nbsp;
      <a href="#" style="color:${C.muted};text-decoration:underline;">${esc(preferences)}</a>
    </div>`,
  ]
    .filter(Boolean)
    .join('')

  return `<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<meta name="x-apple-disable-message-reformatting" />
<title>${esc(brand)}</title>
</head>
<body style="margin:0;padding:0;background:${C.canvas};">
${opts.preheader ? `<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;opacity:0;color:transparent;">${esc(opts.preheader)}</div>` : ''}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${C.canvas};">
  <tr>
    <td align="center" style="padding:40px 14px;">

      <!-- Masthead / logo -->
      <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
        <tr><td align="center" style="padding:0 0 22px;">${masthead}</td></tr>
      </table>

      <!-- Corps -->
      <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:${C.paper};border:1px solid ${C.line};border-top:3px solid ${accent};">
        <tr><td style="padding:46px 48px 44px;">
          ${body}
        </td></tr>
      </table>

      <!-- Pied de page -->
      <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
        <tr><td style="padding:24px 8px 0;text-align:center;font-family:${SANS};font-size:11px;line-height:1.7;color:${C.muted};">
          ${footer}
        </td></tr>
      </table>

    </td>
  </tr>
</table>
</body>
</html>`
}
