import type { EmailTemplate } from '../types'
import { vernissage } from './vernissage'
import { bienvenue } from './bienvenue'
import { programme } from './programme'

/** Registre des templates disponibles dans le studio. */
export const templates: EmailTemplate[] = [vernissage, bienvenue, programme]

export function getTemplate(id: string | undefined): EmailTemplate | undefined {
  return templates.find((t) => t.id === id)
}

/** Initialise les variables d'un template avec leurs valeurs par défaut. */
export function defaultVars(template: EmailTemplate): Record<string, string> {
  return Object.fromEntries(template.fields.map((f) => [f.key, f.default]))
}
