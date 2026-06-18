import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ArrowUpRight, X } from 'lucide-react'
import { templates, defaultVars } from '../templates'
import EmailPreview from '../components/EmailPreview'
import type { EmailTemplate } from '../types'

export default function Templates() {
  const [preview, setPreview] = useState<EmailTemplate | null>(null)

  return (
    <div className="max-w-5xl mx-auto px-6 md:px-10 py-12">
      <header className="mb-10">
        <p className="eyebrow mb-3">Collection</p>
        <h1 className="font-serif text-4xl md:text-5xl leading-tight mb-3">Templates</h1>
        <p className="text-muted max-w-xl leading-relaxed">
          {templates.length} modèles dans le style « musée ». Chaque modèle est éditable au moment de
          composer : titres, textes, dates, boutons.
        </p>
      </header>

      <div className="grid sm:grid-cols-2 gap-px bg-line border border-line">
        {templates.map((t) => (
          <article key={t.id} className="bg-paper p-7 flex flex-col">
            <div className="flex items-start justify-between gap-4 mb-3">
              <div>
                <p className="eyebrow mb-2">{t.category}</p>
                <h2 className="font-serif text-2xl leading-tight">{t.name}</h2>
              </div>
              <span className="text-muted font-serif text-lg">{t.id === 'vernissage' ? '01' : t.id === 'bienvenue' ? '02' : '03'}</span>
            </div>
            <p className="text-sm text-muted leading-relaxed flex-1 mb-5">{t.description}</p>
            <hr className="hairline mb-4" />
            <div className="flex items-center gap-4">
              <button onClick={() => setPreview(t)} className="text-sm text-ink underline underline-offset-4 hover:text-accent">
                Aperçu
              </button>
              <Link to={`/composer?template=${t.id}`} className="ml-auto btn-outline !py-2 !px-4 text-xs">
                Composer <ArrowUpRight size={14} />
              </Link>
            </div>
          </article>
        ))}
      </div>

      {/* Modale d'aperçu */}
      {preview && (
        <div
          className="fixed inset-0 z-50 bg-ink/40 flex items-start justify-center overflow-y-auto p-4 md:p-10"
          onClick={() => setPreview(null)}
        >
          <div className="bg-canvas border border-line w-full max-w-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between px-6 py-4 border-b border-line">
              <div>
                <p className="eyebrow">{preview.category}</p>
                <h3 className="font-serif text-xl">{preview.name}</h3>
              </div>
              <button onClick={() => setPreview(null)} className="text-muted hover:text-ink">
                <X size={20} />
              </button>
            </div>
            <div className="p-4">
              <EmailPreview html={preview.render(defaultVars(preview))} />
            </div>
            <div className="px-6 py-4 border-t border-line flex justify-end">
              <Link to={`/composer?template=${preview.id}`} className="btn-ink">
                Utiliser ce template <ArrowUpRight size={16} />
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
