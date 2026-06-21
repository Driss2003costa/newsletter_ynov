import type { EmailTemplate } from '../types'
import {
  emailShellMvr,
  eyebrow,
  headline,
  lead,
  paragraph,
  sectionTitle,
  featureLines,
  cartel,
  button,
  ornament,
  spacer,
  signature,
  LOGO_MVR,
} from './shellMvr'

/**
 * Saint-Valentin — Expérience immersive (application-guide « Les Échos du Romantisme »).
 * Séparateurs décoratifs, section « app » avec fonctionnalités, cartel, RSVP.
 */
export const stValentinImmersif: EmailTemplate = {
  id: 'st-valentin-immersif',
  name: 'Saint-Valentin — Expérience immersive',
  description: "Soirée immersive du 14 février avec l'application-guide : fonctionnalités, parcours interactif, réservation.",
  category: 'Invitation',
  defaultSubject: '❤️ Vivez une Saint-Valentin immersive au Musée de la Vie Romantique',
  fields: [
    { key: 'eyebrow', label: 'Étiquette', type: 'text', default: 'Saint-Valentin · Expérience immersive' },
    { key: 'title', label: 'Titre', type: 'text', default: "Une soirée où l'amour prend vie" },
    {
      key: 'intro',
      label: 'Introduction',
      type: 'textarea',
      default:
        "Le 14 février, plongez dans une expérience inédite au Musée de la Vie Romantique grâce à notre nouvelle application-guide immersive.\n\nParcourez les salons du musée, écoutez les confidences des grandes figures du romantisme et découvrez les plus belles histoires d'amour du XIXᵉ siècle à travers un parcours interactif conçu spécialement pour la Saint-Valentin.",
      help: 'Les sauts de ligne sont conservés.',
    },
    { key: 'appTitle', label: 'Titre de la section app', type: 'text', default: '📱 Découvrez « Les Échos du Romantisme »' },
    { key: 'appIntro', label: 'Intro de la section app', type: 'text', default: "Grâce à l'application gratuite du musée :" },
    {
      key: 'features',
      label: 'Fonctionnalités (une ligne = un item)',
      type: 'textarea',
      default:
        "🎧 Écoutez des récits audio immersifs inspirés des œuvres et des artistes.\n✨ Explorez des contenus en réalité augmentée en pointant votre smartphone vers certaines œuvres.\n❤️ Participez au parcours « Duo Romantique » et répondez à des questions qui révéleront vos affinités artistiques et sentimentales.\n📜 Débloquez des lettres d'amour historiques et des anecdotes exclusives au fil de votre visite.\n📸 Repartez avec un souvenir numérique personnalisé à partager avec votre moitié.",
    },
    { key: 'date', label: 'Date', type: 'text', default: '14 février' },
    { key: 'hours', label: 'Horaires', type: 'text', default: '19h00 – 22h00' },
    { key: 'place', label: 'Lieu', type: 'text', default: 'Musée de la Vie Romantique, Paris' },
    { key: 'ctaLabel', label: 'Bouton — texte', type: 'text', default: 'Je réserve ma soirée' },
    { key: 'ctaUrl', label: 'Bouton — lien', type: 'url', default: 'https://example.com/saint-valentin-immersif' },
    {
      key: 'closing',
      label: 'Conclusion',
      type: 'textarea',
      default:
        "Laissez-vous guider dans un voyage entre art, émotion et poésie pour célébrer l'amour dans l'un des lieux les plus romantiques de Paris.\n\nNous avons hâte de vous accueillir.",
    },
    { key: 'signature', label: 'Signature', type: 'text', default: "L'équipe du Musée de la Vie Romantique" },
  ],
  render: (v) =>
    emailShellMvr(
      [
        eyebrow(v.eyebrow, 'mauve'),
        headline(v.title),
        ornament(),
        lead(v.intro),
        sectionTitle(v.appTitle),
        paragraph(v.appIntro),
        featureLines(v.features),
        ornament(),
        cartel([
          { label: 'Date', value: v.date },
          { label: 'Horaires', value: v.hours },
          { label: 'Lieu', value: v.place },
        ]),
        spacer(20),
        button(v.ctaLabel, v.ctaUrl),
        spacer(22),
        ornament(),
        spacer(4),
        paragraph(v.closing),
        signature(v.signature),
      ].join('\n'),
      {
        preheader: `Une Saint-Valentin immersive · ${v.date}, ${v.hours}`,
        accent: 'mauve',
        logoUrl: LOGO_MVR,
        logoBg: '#7D8E8A',
      },
    ),
}
