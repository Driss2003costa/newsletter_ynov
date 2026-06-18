import { NavLink, Outlet } from 'react-router-dom'
import { LayoutDashboard, PenLine, GalleryVerticalEnd, Settings as SettingsIcon } from 'lucide-react'
import { cn } from '../lib/cn'

const nav = [
  { to: '/', label: 'Tableau de bord', icon: LayoutDashboard, end: true },
  { to: '/composer', label: 'Composer', icon: PenLine, end: false },
  { to: '/templates', label: 'Templates', icon: GalleryVerticalEnd, end: false },
  { to: '/parametres', label: 'Paramètres', icon: SettingsIcon, end: false },
]

export default function Layout() {
  return (
    <div className="min-h-screen flex">
      {/* Sidebar — cartel de galerie */}
      <aside className="w-64 shrink-0 border-r border-line bg-paper/70 hidden md:flex flex-col">
        <div className="px-7 py-8 border-b border-line">
          <p className="eyebrow mb-1">Studio d'envoi</p>
          <h1 className="font-serif text-2xl leading-tight">
            Newsletter
            <br />
            <span className="text-accent">Ynov</span>
          </h1>
        </div>
        <nav className="flex-1 px-3 py-6 space-y-1">
          {nav.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-4 py-2.5 text-sm transition-colors',
                  isActive ? 'bg-ink text-paper' : 'text-muted hover:text-ink hover:bg-canvas',
                )
              }
            >
              <Icon size={16} strokeWidth={1.75} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="px-7 py-6 border-t border-line">
          <p className="text-[11px] leading-relaxed text-muted">
            Salle d'envoi · Ynov Campus
            <br />
            Édition {new Date().getFullYear()}
          </p>
        </div>
      </aside>

      {/* Contenu */}
      <main className="flex-1 min-w-0">
        {/* Barre mobile */}
        <div className="md:hidden flex items-center gap-4 overflow-x-auto border-b border-line bg-paper px-4 py-3">
          {nav.map(({ to, label, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              className={({ isActive }) =>
                cn('text-xs whitespace-nowrap', isActive ? 'text-accent font-medium' : 'text-muted')
              }
            >
              {label}
            </NavLink>
          ))}
        </div>
        <Outlet />
      </main>
    </div>
  )
}
