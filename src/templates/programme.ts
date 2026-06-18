import type { EmailTemplate } from '../types'
import { emailShell, eyebrow, headline, subhead, paragraph, rule, spacer, button } from './shell'

/**
 * Newsletter « programme » — liste de rubriques façon catalogue d'exposition.
 * Trois temps numérotés, séparés par des filets.
 */
export const programme: EmailTemplate = {
  id: 'programme',
  name: 'Programme du mois',
  description: 'Newsletter en rubriques numérotées, façon catalogue. Idéal pour un récap mensuel.',
  category: 'Newsletter',
  defaultSubject: 'Le programme du mois',
  fields: [
    { key: 'eyebrow', label: 'Étiquette', type: 'text', default: 'Programme · Juillet' },
    { key: 'title', label: 'Titre', type: 'text', default: 'À ne pas manquer ce mois-ci' },
    { key: 'intro', label: 'Introduction', type: 'textarea', default: "Trois rendez-vous sélectionnés pour toi. Bonne lecture." },
    { key: 'item1Title', label: 'Rubrique 1 — titre', type: 'text', default: 'Atelier portfolio' },
    { key: 'item1Body', label: 'Rubrique 1 — texte', type: 'textarea', default: 'Construis un portfolio qui se remarque, avec un intervenant du secteur.' },
    { key: 'item2Title', label: 'Rubrique 2 — titre', type: 'text', default: 'Conférence design' },
    { key: 'item2Body', label: 'Rubrique 2 — texte', type: 'textarea', default: "Une heure pour comprendre les tendances de l'année et les méthodes qui durent." },
    { key: 'item3Title', label: 'Rubrique 3 — titre', type: 'text', default: 'Journée portes ouvertes' },
    { key: 'item3Body', label: 'Rubrique 3 — texte', type: 'textarea', default: 'Fais découvrir le campus à tes proches et rencontre les équipes.' },
    { key: 'ctaLabel', label: 'Bouton — texte', type: 'text', default: 'Voir tout le programme' },
    { key: 'ctaUrl', label: 'Bouton — lien', type: 'url', default: 'https://example.com/programme' },
  ],
  render: (v) => {
    const item = (n: string, title: string, body: string) =>
      title
        ? [
            `<p style="margin:0 0 4px;font-family:Helvetica,Arial,sans-serif;font-size:11px;letter-spacing:3px;color:#A9853E;">${n}</p>`,
            `<h2 style="margin:0 0 8px;font-family:Georgia,serif;font-weight:400;font-size:20px;color:#1B1714;">${title}</h2>`,
            paragraph(body),
          ].join('\n')
        : ''

    return emailShell(
      [
        eyebrow(v.eyebrow),
        headline(v.title),
        spacer(14),
        paragraph(v.intro),
        rule(),
        spacer(22),
        item('01', v.item1Title, v.item1Body),
        rule(),
        spacer(22),
        item('02', v.item2Title, v.item2Body),
        rule(),
        spacer(22),
        item('03', v.item3Title, v.item3Body),
        spacer(8),
        button(v.ctaLabel, v.ctaUrl),
      ].join('\n'),
      { preheader: v.intro || v.title, brand: 'Newsletter Ynov' },
    )
  },
}
