import { Link } from 'react-router-dom'
import { ArrowUpRight, Mail, FlaskConical, AlertCircle } from 'lucide-react'
import { useStore } from '../store/useStore'
import { templates } from '../templates'

function StatusDot({ status }: { status: string }) {
  const color = status === 'sent' ? 'bg-success' : status === 'demo' ? 'bg-gold' : 'bg-accent'
  return <span className={`inline-block w-1.5 h-1.5 rounded-full ${color}`} />
}

export default function Dashboard() {
  const history = useStore((s) => s.history)
  const sent = history.filter((h) => h.status === 'sent').length
  const demo = history.filter((h) => h.status === 'demo').length
  const errors = history.filter((h) => h.status === 'error').length

  const stats = [
    { label: 'Templates', value: templates.length, icon: Mail },
    { label: 'Envois réels', value: sent, icon: ArrowUpRight },
    { label: 'Tests (démo)', value: demo, icon: FlaskConical },
    { label: 'Échecs', value: errors, icon: AlertCircle },
  ]

  return (
    <div className="max-w-5xl mx-auto px-6 md:px-10 py-12">
      <header className="mb-12">
        <p className="eyebrow mb-3">Salle d'envoi</p>
        <h1 className="font-serif text-4xl md:text-5xl leading-tight mb-4">Tableau de bord</h1>
        <p className="text-muted max-w-xl leading-relaxed">
          Compose un email à partir d'un template prédéfini, prévisualise-le comme une œuvre encadrée,
          puis envoie-le. Sans clé Resend, tout fonctionne en mode démo pour tester sereinement.
        </p>
        <div className="mt-6 flex flex-wrap gap-3">
          <Link to="/composer" className="btn-ink">
            Composer un envoi <ArrowUpRight size={16} />
          </Link>
          <Link to="/templates" className="btn-outline">
            Parcourir les templates
          </Link>
        </div>
      </header>

      {/* Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-px bg-line border border-line mb-12">
        {stats.map(({ label, value, icon: Icon }) => (
          <div key={label} className="bg-paper p-6">
            <div className="flex items-center justify-between mb-6 text-muted">
              <span className="eyebrow">{label}</span>
              <Icon size={15} strokeWidth={1.5} />
            </div>
            <p className="font-serif text-4xl">{value}</p>
          </div>
        ))}
      </div>

      {/* Journal */}
      <section>
        <div className="flex items-baseline justify-between mb-4">
          <h2 className="font-serif text-2xl">Journal d'envoi</h2>
          <span className="eyebrow">{history.length} entrée{history.length > 1 ? 's' : ''}</span>
        </div>
        <hr className="hairline mb-2" />
        {history.length === 0 ? (
          <div className="card p-10 text-center text-muted">
            <p>Aucun envoi pour l'instant.</p>
            <Link to="/composer" className="text-accent underline underline-offset-4 mt-2 inline-block">
              Composer le premier
            </Link>
          </div>
        ) : (
          <ul className="divide-y divide-line border-x border-b border-line">
            {history.slice(0, 12).map((h) => (
              <li key={h.id} className="bg-paper px-5 py-4 flex items-center gap-4">
                <StatusDot status={h.status} />
                <div className="min-w-0 flex-1">
                  <p className="text-sm truncate">{h.subject}</p>
                  <p className="text-xs text-muted truncate">
                    {h.templateName} · {h.to.join(', ')}
                  </p>
                </div>
                <span className="eyebrow shrink-0">
                  {new Date(h.timestamp).toLocaleDateString('fr-FR', { day: '2-digit', month: 'short' })}
                </span>
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  )
}
