import type { EmailTemplate } from '../types'
import {
  emailShellMvr,
  eyebrow,
  headline,
  subhead,
  lead,
  paragraph,
  sectionTitle,
  featureLines,
  cartel,
  button,
  rule,
  spacer,
  signature,
} from './shellMvr'

/**
 * Saint-Valentin — Soirée au musée (invitation classique).
 * Cartel d'exposition (date/lieu/horaires), programme en liste, RSVP.
 */
export const stValentin: EmailTemplate = {
  id: 'st-valentin',
  name: 'Saint-Valentin — Soirée',
  description: "Invitation à la soirée du 14 février : programme, cartel date/lieu, réservation.",
  category: 'Invitation',
  defaultSubject: '❤️ Célébrez la Saint-Valentin au Musée de la Vie Romantique',
  fields: [
    { key: 'eyebrow', label: 'Étiquette', type: 'text', default: 'Invitation · Saint-Valentin' },
    { key: 'title', label: 'Titre', type: 'text', default: 'Une soirée romantique au cœur du romantisme parisien' },
    { key: 'subtitle', label: 'Sous-titre (italique)', type: 'text', default: "Une soirée d'exception pour célébrer l'amour." },
    {
      key: 'intro',
      label: 'Introduction',
      type: 'textarea',
      default:
        "À l'occasion de la Saint-Valentin, le Musée de la Vie Romantique vous invite à partager un moment unique dans un cadre empreint de poésie et d'élégance.\n\nLe temps d'une soirée exceptionnelle, découvrez les collections du musée sous un nouvel angle et laissez-vous séduire par l'atmosphère intimiste de cette demeure historique.",
      help: 'Les sauts de ligne sont conservés.',
    },
    { key: 'programmeTitle', label: 'Titre du programme', type: 'text', default: '🌹 Au programme' },
    {
      key: 'programme',
      label: 'Programme (une ligne = un item)',
      type: 'textarea',
      default:
        "Visite libre des collections permanentes\nParcours thématique autour de l'amour romantique\nAnimation musicale en ambiance feutrée\nSurprises réservées aux couples et aux visiteurs",
    },
    { key: 'date', label: 'Date', type: 'text', default: '14 février' },
    { key: 'place', label: 'Lieu', type: 'text', default: 'Musée de la Vie Romantique, Paris' },
    { key: 'hours', label: 'Horaires', type: 'text', default: '19h00 – 22h00' },
    { key: 'ctaLabel', label: 'Bouton — texte', type: 'text', default: 'Je réserve ma place' },
    { key: 'ctaUrl', label: 'Bouton — lien', type: 'url', default: 'https://example.com/saint-valentin' },
    {
      key: 'closing',
      label: 'Conclusion',
      type: 'textarea',
      default:
        "Partagez cette expérience avec la personne de votre choix et célébrez l'amour dans l'un des lieux les plus romantiques de Paris.\n\nAu plaisir de vous accueillir,",
    },
    { key: 'signature', label: 'Signature', type: 'text', default: "L'équipe du Musée de la Vie Romantique" },
  ],
  render: (v) =>
    emailShellMvr(
      [
        eyebrow(v.eyebrow, 'mauve'),
        headline(v.title),
        subhead(v.subtitle),
        spacer(16),
        lead(v.intro),
        sectionTitle(v.programmeTitle),
        featureLines(v.programme),
        spacer(4),
        cartel([
          { label: 'Date', value: v.date },
          { label: 'Lieu', value: v.place },
          { label: 'Horaires', value: v.hours },
        ]),
        spacer(20),
        button(v.ctaLabel, v.ctaUrl),
        spacer(22),
        rule(),
        spacer(18),
        paragraph(v.closing),
        signature(v.signature),
      ].join('\n'),
      {
        preheader: `${v.date} · ${v.hours} · Musée de la Vie Romantique`,
        accent: 'mauve',
      },
    ),
}
