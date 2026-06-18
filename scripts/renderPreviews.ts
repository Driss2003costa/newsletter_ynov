/**
 * Génère un aperçu HTML de chaque template dans `previews/`.
 * Lancer avec :  npx vite-node scripts/renderPreviews.ts
 */
import { writeFileSync, mkdirSync } from 'node:fs'
import { templates, defaultVars } from '../src/templates/index'

mkdirSync('previews', { recursive: true })
for (const t of templates) {
  const html = t.render(defaultVars(t))
  writeFileSync(`previews/${t.id}.html`, html, 'utf8')
  console.log(`✓ previews/${t.id}.html  —  ${t.name}`)
}
