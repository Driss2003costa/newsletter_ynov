import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Send, Monitor, Smartphone, CheckCircle2, AlertCircle, FlaskConical, Loader2 } from 'lucide-react'
import { templates, getTemplate, defaultVars } from '../templates'
import { useStore } from '../store/useStore'
import { sendEmail } from '../lib/api'
import type { SendStatus } from '../types'
import EmailPreview from '../components/EmailPreview'
import { cn } from '../lib/cn'

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

/** Découpe une saisie libre en adresses (virgule, point-virgule, espace, retour ligne). */
function parseRecipients(raw: string): string[] {
  return Array.from(new Set(raw.split(/[\s,;]+/).map((s) => s.trim()).filter(Boolean)))
}

interface Feedback {
  status: SendStatus
  message: string
}

export default function Composer() {
  const [params] = useSearchParams()
  const settings = useStore((s) => s.settings)
  const addRecord = useStore((s) => s.addRecord)

  const [selectedId, setSelectedId] = useState(() => {
    const q = params.get('template')
    return getTemplate(q ?? undefined)?.id ?? templates[0].id
  })
  const template = getTemplate(selectedId)!

  const [vars, setVars] = useState<Record<string, string>>(() => defaultVars(template))
  const [subject, setSubject] = useState(template.defaultSubject)
  const [toRaw, setToRaw] = useState('')
  const [device, setDevice] = useState<'desktop' | 'mobile'>('desktop')
  const [sending, setSending] = useState(false)
  const [feedback, setFeedback] = useState<Feedback | null>(null)

  // Changement de template → réinitialise variables + objet.
  function selectTemplate(id: string) {
    const t = getTemplate(id)
    if (!t) return
    setSelectedId(id)
    setVars(defaultVars(t))
    setSubject(t.defaultSubject)
    setFeedback(null)
  }

  // Pré-sélection via ?template= (au cas où le param change après montage).
  useEffect(() => {
    const q = params.get('template')
    if (q && q !== selectedId && getTemplate(q)) selectTemplate(q)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params])

  const html = useMemo(() => template.render(vars), [template, vars])
  const recipients = useMemo(() => parseRecipients(toRaw), [toRaw])
  const invalid = recipients.filter((e) => !EMAIL_RE.test(e))
  const canSend = recipients.length > 0 && invalid.length === 0 && subject.trim().length > 0 && !sending

  async function handleSend() {
    if (!canSend) return
    setSending(true)
    setFeedback(null)
    const result = await sendEmail({
      to: recipients,
      subject: subject.trim(),
      html,
      fromName: settings.fromName,
      fromEmail: settings.fromEmail,
      replyTo: settings.replyTo || undefined,
    })

    const status: SendStatus = !result.ok ? 'error' : result.demo ? 'demo' : 'sent'
    addRecord({
      id: crypto.randomUUID(),
      templateId: template.id,
      templateName: template.name,
      to: recipients,
      subject: subject.trim(),
      status,
      message: result.message,
      timestamp: Date.now(),
    })

    setFeedback({
      status,
      message:
        status === 'sent'
          ? `Email envoyé à ${recipients.length} destinataire${recipients.length > 1 ? 's' : ''}.`
          : status === 'demo'
            ? result.message || 'Mode démo : aucun email réellement envoyé.'
            : result.message || "Échec de l'envoi.",
    })
    setSending(false)
  }

  return (
    <div className="px-6 md:px-10 py-12 max-w-7xl mx-auto">
      <header className="mb-8">
        <p className="eyebrow mb-3">Composition</p>
        <h1 className="font-serif text-4xl md:text-5xl leading-tight">Composer un envoi</h1>
      </header>

      <div className="grid lg:grid-cols-[minmax(0,420px)_1fr] gap-px bg-line border border-line">
        {/* ---- Colonne formulaire ---- */}
        <div className="bg-paper p-6 md:p-8 space-y-7">
          {/* Template */}
          <div>
            <label className="field-label">Template</label>
            <div className="grid grid-cols-1 gap-px bg-line border border-line">
              {templates.map((t) => (
                <button
                  key={t.id}
                  onClick={() => selectTemplate(t.id)}
                  className={cn(
                    'text-left px-4 py-3 transition-colors',
                    t.id === selectedId ? 'bg-ink text-paper' : 'bg-paper hover:bg-canvas',
                  )}
                >
                  <span className="block text-sm">{t.name}</span>
                  <span className={cn('block text-xs', t.id === selectedId ? 'text-paper/60' : 'text-muted')}>
                    {t.category}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Destinataires */}
          <div>
            <label className="field-label">Destinataire(s)</label>
            <textarea
              value={toRaw}
              onChange={(e) => setToRaw(e.target.value)}
              rows={2}
              placeholder="prenom@exemple.com, autre@exemple.com"
              className="field resize-y"
            />
            <p className="mt-1.5 text-xs text-muted">
              {recipients.length} adresse{recipients.length > 1 ? 's' : ''}
              {invalid.length > 0 && <span className="text-accent"> · invalide : {invalid.join(', ')}</span>}
            </p>
          </div>

          {/* Objet */}
          <div>
            <label className="field-label">Objet</label>
            <input value={subject} onChange={(e) => setSubject(e.target.value)} className="field" />
          </div>

          <hr className="hairline" />

          {/* Variables du template */}
          <div className="space-y-5">
            <p className="eyebrow">Contenu</p>
            {template.fields.map((f) => (
              <div key={f.key}>
                <label className="field-label">{f.label}</label>
                {f.type === 'textarea' ? (
                  <textarea
                    value={vars[f.key] ?? ''}
                    onChange={(e) => setVars((v) => ({ ...v, [f.key]: e.target.value }))}
                    rows={4}
                    className="field resize-y"
                  />
                ) : (
                  <input
                    type={f.type === 'url' ? 'url' : 'text'}
                    value={vars[f.key] ?? ''}
                    onChange={(e) => setVars((v) => ({ ...v, [f.key]: e.target.value }))}
                    className="field"
                  />
                )}
                {f.help && <p className="mt-1 text-xs text-muted">{f.help}</p>}
              </div>
            ))}
          </div>

          <hr className="hairline" />

          {/* Expéditeur + envoi */}
          <div>
            <p className="text-xs text-muted mb-4">
              Expéditeur : <span className="text-ink">{settings.fromName}</span> &lt;{settings.fromEmail}&gt;
            </p>
            <button onClick={handleSend} disabled={!canSend} className="btn-ink w-full">
              {sending ? <Loader2 size={16} className="animate-spin" /> : <Send size={16} />}
              {sending ? 'Envoi…' : 'Envoyer'}
            </button>

            {feedback && (
              <div
                className={cn(
                  'mt-4 flex items-start gap-2 px-4 py-3 text-sm border',
                  feedback.status === 'sent' && 'border-success/40 bg-success/5 text-ink',
                  feedback.status === 'demo' && 'border-gold/40 bg-gold/5 text-ink',
                  feedback.status === 'error' && 'border-accent/40 bg-accent-50 text-ink',
                )}
              >
                {feedback.status === 'sent' && <CheckCircle2 size={16} className="mt-0.5 text-success shrink-0" />}
                {feedback.status === 'demo' && <FlaskConical size={16} className="mt-0.5 text-gold shrink-0" />}
                {feedback.status === 'error' && <AlertCircle size={16} className="mt-0.5 text-accent shrink-0" />}
                <span>{feedback.message}</span>
              </div>
            )}
          </div>
        </div>

        {/* ---- Colonne aperçu ---- */}
        <div className="bg-canvas p-6 md:p-8">
          <div className="flex items-center justify-between mb-5">
            <p className="eyebrow">Aperçu</p>
            <div className="flex gap-px border border-line">
              <button
                onClick={() => setDevice('desktop')}
                className={cn('p-2', device === 'desktop' ? 'bg-ink text-paper' : 'bg-paper text-muted')}
                title="Bureau"
              >
                <Monitor size={15} />
              </button>
              <button
                onClick={() => setDevice('mobile')}
                className={cn('p-2', device === 'mobile' ? 'bg-ink text-paper' : 'bg-paper text-muted')}
                title="Mobile"
              >
                <Smartphone size={15} />
              </button>
            </div>
          </div>
          <EmailPreview html={html} device={device} />
        </div>
      </div>
    </div>
  )
}
