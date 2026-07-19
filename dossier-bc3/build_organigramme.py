# -*- coding: utf-8 -*-
"""Génère l'organigramme de J'ai vu la Vierge en SVG (palette musée)."""
import html

# -------- palette « musée »
BG      = "#F4EEE2"
BOX     = "#FFFFFF"
INK     = "#26221E"
MUTED   = "#6E655A"
LINE    = "#4A443C"
OXBLOOD = "#7A1F1F"
DIR_FILL= "#FCF7F5"

SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"

elems = []          # fragments SVG
xs, ys = [], []     # pour la bounding box

def track(x, y):
    xs.append(x); ys.append(y)

def wrap(text, maxc):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= maxc:
            cur = (cur + " " + w).strip()
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines[:2]

def box(cx, top, w, name, role, direction=False):
    h = 86
    left = cx - w/2
    track(left, top); track(left + w, top + h)
    stroke = OXBLOOD if direction else INK
    sw = 1.8 if direction else 1.3
    fill = DIR_FILL if direction else BOX
    elems.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w}" height="{h}" rx="7" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    # nom
    elems.append(f'<text x="{cx:.1f}" y="{top+32:.1f}" text-anchor="middle" '
                 f'font-family="{SERIF}" font-size="16.5" font-weight="bold" fill="{INK}">'
                 f'{html.escape(name)}</text>')
    # rôle (jusqu'à 2 lignes)
    maxc = int(w / 7.2)
    for i, ln in enumerate(wrap(role, maxc)):
        elems.append(f'<text x="{cx:.1f}" y="{top+54+i*17:.1f}" text-anchor="middle" '
                     f'font-family="{SERIF}" font-size="12" fill="{MUTED}">{html.escape(ln)}</text>')
    return dict(cx=cx, top=top, w=w, h=h, bottom=top+h)

def line(x1, y1, x2, y2):
    track(x1, y1); track(x2, y2)
    elems.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" '
                 f'stroke="{LINE}" stroke-width="1.4" fill="none"/>')

def label(cx, y, text):
    track(cx, y)
    elems.append(f'<text x="{cx:.1f}" y="{y:.1f}" text-anchor="middle" '
                 f'font-family="{SERIF}" font-size="12" letter-spacing="3" '
                 f'fill="{OXBLOOD}">{html.escape(text)}</text>')

# ============================ construction
W1, W2 = 250, 216
colA, colB, colC = 320, 800, 1280   # Marie, Sarah, Camille Abela

# Niveau 0 : direction
fa = box(665, 110, W1, "Alexandra Cefai", "Créatrice de la marque", direction=True)
fd = box(935, 110, W1, "Damien Grauvogel", "Designer produit et co-créateur", direction=True)

# jonction des deux fondateurs
line(665, 196, 665, 216)
line(935, 196, 935, 216)
line(665, 216, 935, 216)
line(800, 216, 800, 250)

# bus vers les managers
line(colA, 250, colC, 250)
for cx in (colA, colB, colC):
    line(cx, 250, cx, 292)

# Niveau 1 : responsables
mMarie  = box(colA, 292, W1, "Marie Homasson", "Manageuse commerciale")
mSarah  = box(colB, 292, W1, "Sarah Moussaoui", "Responsable commande B2C et SAV")
mCam    = box(colC, 292, W1, "Camille Abela", "Responsable e-commerce")

# Niveau 2
def two_reports(mgr, r1, r2):
    cx, bot = mgr['cx'], mgr['bottom']
    c1, c2 = cx - 114, cx + 114
    line(cx, bot, cx, bot + 32)
    line(c1, bot + 32, c2, bot + 32)
    line(c1, bot + 32, c1, bot + 44)
    line(c2, bot + 32, c2, bot + 44)
    box(c1, bot + 44, W2, r1[0], r1[1])
    box(c2, bot + 44, W2, r2[0], r2[1])

def one_report(mgr, r):
    cx, bot = mgr['cx'], mgr['bottom']
    line(cx, bot, cx, bot + 44)
    box(cx, bot + 44, W2, r[0], r[1])

two_reports(mMarie,
            ("Ruben Sagot", "Alternant commercial"),
            ("Lucas Mouren", "Alternant gestion entreprise"))
two_reports(mSarah,
            ("Camille Noël", "Peintre"),
            ("Jennifer Lienert", "Responsable commande (plâtre)"))
one_report(mCam, ("Estelle Casterot", "Alternante cheffe de projet e-commerce"))

# ============================ bounding box + titre + légende
PAD = 70
minx, maxx = min(xs) - PAD, max(xs) + PAD
miny, maxy = min(ys) - PAD, max(ys) + PAD
cxmid = (minx + maxx) / 2

title = (f'<text x="{cxmid:.1f}" y="{miny+34:.1f}" text-anchor="middle" '
         f'font-family="{SERIF}" font-size="26" font-weight="bold" fill="{OXBLOOD}">'
         f'J\'ai vu la Vierge</text>'
         f'<text x="{cxmid:.1f}" y="{miny+60:.1f}" text-anchor="middle" '
         f'font-family="{SERIF}" font-size="14" fill="{INK}">Organigramme de l\'entreprise</text>')
caption = (f'<text x="{cxmid:.1f}" y="{maxy-24:.1f}" text-anchor="middle" '
           f'font-family="{SERIF}" font-size="11" font-style="italic" fill="{MUTED}">'
           f'Figure 1 : Organigramme de J\'ai vu la Vierge et positionnement de l\'alternante</text>')
# on réserve la place du titre/légende dans la bbox
miny -= 34
maxy += 6

Wt, Ht = maxx - minx, maxy - miny
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt:.0f}" height="{Ht:.0f}" '
       f'viewBox="{minx:.0f} {miny:.0f} {Wt:.0f} {Ht:.0f}">'
       f'<rect x="{minx:.0f}" y="{miny:.0f}" width="{Wt:.0f}" height="{Ht:.0f}" fill="{BG}"/>'
       + title + "".join(elems) + caption + '</svg>')

open("organigramme.svg", "w", encoding="utf-8").write(svg)
htmlpage = f'<!doctype html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0}}</style></head><body>{svg}</body></html>'
open("organigramme.html", "w", encoding="utf-8").write(htmlpage)
print(f"SVG {Wt:.0f}x{Ht:.0f} généré.")
