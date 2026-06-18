import { cn } from '../lib/cn'

interface Props {
  html: string
  /** Largeur de simulation : bureau ou mobile. */
  device?: 'desktop' | 'mobile'
  className?: string
}

/**
 * Rend le HTML d'email dans un iframe isolé (sandbox) pour un aperçu fidèle,
 * sans que les styles de l'app ne fuitent dans l'email — et inversement.
 */
export default function EmailPreview({ html, device = 'desktop', className }: Props) {
  return (
    <div className={cn('flex justify-center', className)}>
      <iframe
        title="Aperçu de l'email"
        srcDoc={html}
        sandbox=""
        className={cn(
          'bg-white border border-line transition-all duration-200',
          device === 'mobile' ? 'w-[390px]' : 'w-full',
        )}
        style={{ height: '70vh', minHeight: 480 }}
      />
    </div>
  )
}
