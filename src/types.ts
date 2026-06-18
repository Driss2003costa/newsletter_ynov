/** Un champ éditable d'un template (variable de fusion). */
export interface TemplateField {
  key: string
  label: string
  type: 'text' | 'textarea' | 'url'
  default: string
  help?: string
}

/** Un template d'email prédéfini. */
export interface EmailTemplate {
  id: string
  name: string
  /** Description courte affichée dans la galerie. */
  description: string
  /** Catégorie / type d'envoi (ex. « Invitation », « Bienvenue »). */
  category: string
  /** Objet pré-rempli quand on choisit le template. */
  defaultSubject: string
  /** Variables éditables. */
  fields: TemplateField[]
  /** Rend le HTML complet de l'email à partir des variables. */
  render: (vars: Record<string, string>) => string
}

export type SendStatus = 'sent' | 'demo' | 'error'

/** Une entrée du journal d'envoi. */
export interface SendRecord {
  id: string
  templateId: string
  templateName: string
  to: string[]
  subject: string
  status: SendStatus
  message?: string
  timestamp: number
}

export interface Settings {
  fromName: string
  fromEmail: string
  replyTo: string
}
