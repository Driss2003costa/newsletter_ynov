import type { EmailTemplate } from '../types'
import { emailShell, eyebrow, headline, subhead, paragraph, rule, spacer, button, metaRow, metaTable } from './shell'

/**
 * Invitation type « vernissage » — la pièce la plus à propos pour un design musée.
 * Cartel, filets, méta date/lieu, bouton sobre.
 */
export const vernissage: EmailTemplate = {
  id: 'vernissage',
  name: 'Invitation — Vernissage',
  description: "Carton d'invitation à un événement : étiquette, date/lieu en cartel, RSVP.",
  category: 'Invitation',
  defaultSubject: 'Invitation — Vernissage le 3 juillet',
  fields: [
    { key: 'eyebrow', label: 'Étiquette', type: 'text', default: 'Invitation' },
    { key: 'title', label: 'Titre', type: 'text', default: 'Vernissage des projets étudiants' },
    { key: 'subtitle', label: 'Sous-titre (italique)', type: 'text', default: 'Une soirée pour découvrir les travaux de la promotion.' },
    {
      key: 'body',
      label: 'Texte',
      type: 'textarea',
      default:
        "Nous avons le plaisir de t'inviter au vernissage de fin d'année. Les étudiants présenteront leurs réalisations dans une scénographie pensée comme une exposition. Un verre sera offert à l'ouverture.",
      help: 'Les sauts de ligne sont conservés.',
    },
    { key: 'date', label: 'Date', type: 'text', default: 'Jeudi 3 juillet, 18 h 30' },
    { key: 'place', label: 'Lieu', type: 'text', default: 'Ynov Campus — Hall principal' },
    { key: 'dress', label: 'Mention', type: 'text', default: 'Entrée libre sur inscription' },
    { key: 'ctaLabel', label: 'Bouton — texte', type: 'text', default: 'Je réserve ma place' },
    { key: 'ctaUrl', label: 'Bouton — lien', type: 'url', default: 'https://example.com/rsvp' },
  ],
  render: (v) =>
    emailShell(
      [
        eyebrow(v.eyebrow),
        headline(v.title),
        subhead(v.subtitle),
        spacer(18),
        paragraph(v.body),
        metaTable([metaRow('Date', v.date), metaRow('Lieu', v.place), metaRow('Accès', v.dress)].join('')),
        spacer(20),
        button(v.ctaLabel, v.ctaUrl),
      ].join('\n'),
      { preheader: v.subtitle || v.title, brand: 'Newsletter Ynov' },
    ),
}
