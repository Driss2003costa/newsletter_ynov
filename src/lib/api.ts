/** Réponse normalisée d'un envoi. */
export interface SendResult {
  ok: boolean
  demo: boolean
  /** true si le mode démo est dû à l'absence de backend (ex. `npm run dev`). */
  simulated?: boolean
  id?: string | null
  message?: string
}

export interface SendPayload {
  to: string[]
  subject: string
  html: string
  fromName?: string
  fromEmail?: string
  replyTo?: string
}

/**
 * Appelle la fonction serverless /api/send.
 *
 * En `npm run dev` (Vite seul, sans backend), la route /api/send n'existe pas :
 * Vite renvoie alors le index.html (HTML, pas du JSON). On le détecte et on
 * bascule en démo « simulée » pour que l'UI reste testable hors Vercel.
 */
export async function sendEmail(payload: SendPayload): Promise<SendResult> {
  let res: Response
  try {
    res = await fetch('/api/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })
  } catch (err) {
    return {
      ok: true,
      demo: true,
      simulated: true,
      message: `Mode démo local : backend injoignable (${(err as Error).message}). Aucun email envoyé.`,
    }
  }

  const contentType = res.headers.get('content-type') || ''
  if (!contentType.includes('application/json')) {
    // Pas de fonction serverless en face (Vite dev) — démo simulée.
    return {
      ok: true,
      demo: true,
      simulated: true,
      message: 'Mode démo local : exécute `vercel dev` ou déploie sur Vercel pour un envoi réel.',
    }
  }

  const data = (await res.json().catch(() => ({}))) as Record<string, unknown>

  if (!res.ok) {
    return { ok: false, demo: false, message: (data.error as string) || `Erreur ${res.status}` }
  }

  return {
    ok: true,
    demo: Boolean(data.demo),
    id: (data.id as string) ?? null,
    message: (data.message as string) || undefined,
  }
}
