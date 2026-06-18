import type { EmailTemplate } from '../types'
import {
  emailShellMvr,
  eyebrow,
  headline,
  lead,
  paragraph,
  sectionTitle,
  featureLines,
  promoBox,
  button,
  note,
  rule,
  spacer,
  signature,
  LOGO_MVR,
} from './shellMvr'

/**
 * Immersion Experience — promo d'une expérience immersive (ton tutoiement,
 * dynamique). Même système visuel moderne, accent sauge, avec encart code promo.
 */
export const immersion: EmailTemplate = {
  id: 'immersion',
  name: 'Immersion Experience — Promo',
  description: 'Annonce dynamique avec offre limitée et code promo. Ton tutoiement, accent vert sauge.',
  category: 'Promotion',
  defaultSubject: '🚀 Une aventure immersive t’attend !',
  fields: [
    { key: 'eyebrow', label: 'Étiquette', type: 'text', default: 'Nouvelle expérience immersive' },
    { key: 'title', label: 'Titre', type: 'text', default: 'Une aventure immersive t’attend' },
    { key: 'greeting', label: 'Accroche', type: 'text', default: 'Salut,' },
    {
      key: 'intro',
      label: 'Introduction',
      type: 'textarea',
      default:
        "Et si tu sortais de l'ordinaire le temps d'une journée ?\n\nEntre défis interactifs, décors immersifs et missions à relever en équipe, notre nouvelle expérience a été pensée pour celles et ceux qui aiment l'action, le fun et les moments à partager.",
      help: 'Les sauts de ligne sont conservés.',
    },
    { key: 'programmeTitle', label: 'Titre « ce qui t’attend »', type: 'text', default: '🎯 Ce qui t’attend' },
    {
      key: 'programme',
      label: 'Points clés (une ligne = un item)',
      type: 'textarea',
      default:
        'Des univers immersifs à explorer\nDes défis collaboratifs et interactifs\nUne expérience à vivre entre amis\nDes souvenirs mémorables à partager',
    },
    { key: 'offerTitle', label: 'Titre de l’offre', type: 'text', default: '🔥 Offre exclusive' },
    {
      key: 'offerText',
      label: 'Texte de l’offre',
      type: 'textarea',
      default: 'Réserve ta place avant le 30 juin et profite de 15 % de réduction avec le code :',
    },
    { key: 'promoCode', label: 'Code promo', type: 'text', default: 'IMMERSION15' },
    { key: 'ctaLabel', label: 'Bouton — texte', type: 'text', default: 'Je réserve ma place' },
    { key: 'ctaUrl', label: 'Bouton — lien', type: 'url', default: 'https://example.com/immersion' },
    { key: 'noteText', label: 'Note', type: 'text', default: 'Les places sont limitées pour garantir une expérience optimale.' },
    { key: 'signature', label: 'Signature', type: 'textarea', default: 'À très vite,\nL’équipe Immersion Experience' },
  ],
  render: (v) =>
    emailShellMvr(
      [
        eyebrow(v.eyebrow, 'sage'),
        headline(v.title),
        spacer(12),
        paragraph(v.greeting),
        lead(v.intro),
        sectionTitle(v.programmeTitle),
        featureLines(v.programme),
        sectionTitle(v.offerTitle),
        paragraph(v.offerText),
        promoBox('Code promo', v.promoCode),
        spacer(16),
        button(v.ctaLabel, v.ctaUrl),
        note(v.noteText),
        spacer(22),
        rule(),
        signature(v.signature),
      ].join('\n'),
      {
        preheader: `Réserve avant le 30 juin · -15% avec le code ${v.promoCode}`,
        brand: 'Musée de la Vie Romantique',
        accent: 'sage',
        logoUrl: LOGO_MVR,
        logoBg: '#2E2F29',
      },
    ),
}
