import { useState } from 'react'
import { Trash2, Info } from 'lucide-react'
import { useStore } from '../store/useStore'

export default function Settings() {
  const settings = useStore((s) => s.settings)
  const setSettings = useStore((s) => s.setSettings)
  const history = useStore((s) => s.history)
  const clearHistory = useStore((s) => s.clearHistory)
  const [saved, setSaved] = useState(false)

  function update(key: keyof typeof settings, value: string) {
    setSettings({ [key]: value })
    setSaved(true)
    setTimeout(() => setSaved(false), 1500)
  }

  return (
    <div className="max-w-2xl mx-auto px-6 md:px-10 py-12">
      <header className="mb-10">
        <p className="eyebrow mb-3">Configuration</p>
        <h1 className="font-serif text-4xl md:text-5xl leading-tight">Paramètres</h1>
      </header>

      {/* Expéditeur */}
      <section className="card p-7 mb-8">
        <h2 className="font-serif text-2xl mb-1">Expéditeur</h2>
        <p className="text-sm text-muted mb-6">Identité affichée dans les emails envoyés.</p>
        <div className="space-y-5">
          <div>
            <label className="field-label">Nom affiché</label>
            <input className="field" value={settings.fromName} onChange={(e) => update('fromName', e.target.value)} />
          </div>
          <div>
            <label className="field-label">Adresse d'envoi</label>
            <input
              className="field"
              type="email"
              value={settings.fromEmail}
              onChange={(e) => update('fromEmail', e.target.value)}
            />
            <p className="mt-1 text-xs text-muted">
              Le domaine doit être vérifié dans Resend. Pour tester : <code>onboarding@resend.dev</code>.
            </p>
          </div>
          <div>
            <label className="field-label">Répondre à (optionnel)</label>
            <input
              className="field"
              type="email"
              value={settings.replyTo}
              onChange={(e) => update('replyTo', e.target.value)}
              placeholder="contact@exemple.com"
            />
          </div>
        </div>
        {saved && <p className="mt-4 text-xs text-success">Enregistré.</p>}
      </section>

      {/* Statut envoi */}
      <section className="card p-7 mb-8">
        <h2 className="font-serif text-2xl mb-4">Envoi des emails</h2>
        <div className="flex items-start gap-3 text-sm text-muted leading-relaxed">
          <Info size={16} className="mt-0.5 shrink-0 text-accent" />
          <div>
            <p className="mb-2">
              L'envoi réel passe par la fonction <code>/api/send</code> (Resend). Elle ne fonctionne que
              déployée sur Vercel ou via <code>vercel dev</code>.
            </p>
            <p>
              Définis <code>RESEND_API_KEY</code> dans les variables d'environnement Vercel pour activer
              l'envoi réel. Sans cette clé — ou en <code>npm run dev</code> — l'app reste en{' '}
              <span className="text-ink">mode démo</span> : aperçu et journal fonctionnent, aucun email ne part.
            </p>
          </div>
        </div>
      </section>

      {/* Journal */}
      <section className="card p-7">
        <h2 className="font-serif text-2xl mb-1">Journal d'envoi</h2>
        <p className="text-sm text-muted mb-6">{history.length} entrée(s) stockée(s) localement (navigateur).</p>
        <button
          onClick={() => {
            if (confirm("Effacer tout le journal d'envoi ?")) clearHistory()
          }}
          disabled={history.length === 0}
          className="btn-outline text-sm"
        >
          <Trash2 size={15} /> Vider le journal
        </button>
      </section>
    </div>
  )
}
