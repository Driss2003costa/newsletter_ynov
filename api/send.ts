/**
 * Vercel Serverless Function — POST /api/send
 *
 * Envoie un email via l'API Resend (https://resend.com).
 * Sans `RESEND_API_KEY`, la fonction répond en MODE DÉMO : rien n'est envoyé,
 * mais l'application reçoit une réponse de succès simulée pour tester le flux.
 *
 * Body attendu (JSON) :
 *   { to: string | string[], subject: string, html: string,
 *     fromName?: string, fromEmail?: string, replyTo?: string }
 */

type Req = {
  method?: string
  body?: unknown
}

type Res = {
  status: (code: number) => Res
  json: (data: unknown) => void
  setHeader: (name: string, value: string) => void
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

function asArray(v: unknown): string[] {
  if (Array.isArray(v)) return v.map(String)
  if (typeof v === 'string') return [v]
  return []
}

export default async function handler(req: Req, res: Res) {
  res.setHeader('Content-Type', 'application/json')

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Méthode non autorisée. Utilise POST.' })
  }

  let body: Record<string, unknown> = {}
  try {
    body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body as Record<string, unknown>) ?? {}
  } catch {
    return res.status(400).json({ error: 'Corps de requête JSON invalide.' })
  }

  const to = asArray(body.to).map((s) => s.trim()).filter(Boolean)
  const subject = typeof body.subject === 'string' ? body.subject : ''
  const html = typeof body.html === 'string' ? body.html : ''
  const fromName = typeof body.fromName === 'string' ? body.fromName : ''
  const fromEmailRaw = typeof body.fromEmail === 'string' ? body.fromEmail : ''
  const replyTo = typeof body.replyTo === 'string' ? body.replyTo : ''

  // Validation
  if (to.length === 0) return res.status(400).json({ error: 'Aucun destinataire fourni.' })
  const invalid = to.filter((e) => !EMAIL_RE.test(e))
  if (invalid.length) return res.status(400).json({ error: `Adresse(s) invalide(s) : ${invalid.join(', ')}` })
  if (!subject) return res.status(400).json({ error: "L'objet de l'email est requis." })
  if (!html) return res.status(400).json({ error: 'Le contenu HTML est vide.' })

  const apiKey = process.env.RESEND_API_KEY
  const fromEmail = fromEmailRaw || process.env.DEFAULT_FROM_EMAIL || 'onboarding@resend.dev'
  const fromLabel = fromName || process.env.DEFAULT_FROM_NAME || ''
  const from = fromLabel ? `${fromLabel} <${fromEmail}>` : fromEmail

  // --- Mode démo : pas de clé API ---
  if (!apiKey) {
    return res.status(200).json({
      demo: true,
      message:
        'Mode démo : aucun email réellement envoyé (RESEND_API_KEY non configurée). Le flux a été validé.',
      preview: { from, to, subject },
    })
  }

  // --- Envoi réel via Resend ---
  try {
    const payload: Record<string, unknown> = { from, to, subject, html }
    if (replyTo) payload.reply_to = replyTo

    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    })

    const data = await r.json().catch(() => ({}))

    if (!r.ok) {
      const message =
        (data && (data.message || (data.error && data.error.message))) || `Erreur Resend (${r.status})`
      return res.status(r.status).json({ error: message, details: data })
    }

    return res.status(200).json({ demo: false, id: data.id ?? null, to, subject })
  } catch (err) {
    return res.status(502).json({ error: `Échec de l'appel à Resend : ${(err as Error).message}` })
  }
}
