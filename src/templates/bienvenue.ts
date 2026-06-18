import type { EmailTemplate } from '../types'
import { emailShell, eyebrow, headline, subhead, paragraph, rule, spacer, button } from './shell'

/** Email de bienvenue — accueil sobre, une seule action. */
export const bienvenue: EmailTemplate = {
  id: 'bienvenue',
  name: 'Bienvenue',
  description: 'Accueil épuré pour une nouvelle inscription : message + une action.',
  category: 'Bienvenue',
  defaultSubject: 'Bienvenue à Ynov',
  fields: [
    { key: 'eyebrow', label: 'Étiquette', type: 'text', default: 'Bienvenue' },
    { key: 'title', label: 'Titre', type: 'text', default: 'Ravis de te compter parmi nous' },
    { key: 'subtitle', label: 'Sous-titre (italique)', type: 'text', default: 'Ton aventure commence ici.' },
    {
      key: 'body',
      label: 'Texte',
      type: 'textarea',
      default:
        "Bonjour,\n\nTon inscription est confirmée. Tu trouveras dans ton espace toutes les ressources, le calendrier et les contacts utiles pour bien démarrer.\n\nN'hésite pas à répondre à cet email si tu as la moindre question — nous sommes là pour t'accompagner.",
    },
    { key: 'ctaLabel', label: 'Bouton — texte', type: 'text', default: 'Accéder à mon espace' },
    { key: 'ctaUrl', label: 'Bouton — lien', type: 'url', default: 'https://example.com/espace' },
    { key: 'signature', label: 'Signature', type: 'text', default: "L'équipe Ynov" },
  ],
  render: (v) =>
    emailShell(
      [
        eyebrow(v.eyebrow),
        headline(v.title),
        subhead(v.subtitle),
        spacer(18),
        paragraph(v.body),
        spacer(8),
        button(v.ctaLabel, v.ctaUrl),
        spacer(28),
        rule(),
        spacer(16),
        `<p style="margin:0;font-family:Georgia,serif;font-style:italic;font-size:15px;color:#6B6258;">${v.signature || ''}</p>`,
      ].join('\n'),
      { preheader: v.subtitle || v.title, brand: 'Newsletter Ynov' },
    ),
}
