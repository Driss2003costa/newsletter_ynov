# -*- coding: utf-8 -*-
"""Organigramme par pôles — noir et blanc, épuré."""
import html

WHITE = "#FFFFFF"
BLACK = "#111111"
GREEN = "#2E7D32"   # carte d'Estelle, pour se repérer
SANS  = "Arial, 'Helvetica Neue', Helvetica, 'Liberation Sans', sans-serif"

elems, xs, ys = [], [], []
def track(x, y): xs.append(x); ys.append(y)

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

def box(cx, top, w, name, role, dark=False, bg=None):
    h = 84
    left = cx - w/2
    track(left, top); track(left + w, top + h)
    fill = bg if bg else (BLACK if dark else WHITE)
    tcol = WHITE if (dark or bg) else BLACK
    elems.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w}" height="{h}" rx="2" '
                 f'fill="{fill}" stroke="{BLACK}" stroke-width="1.4"/>')
    elems.append(f'<text x="{cx:.1f}" y="{top+32:.1f}" text-anchor="middle" '
                 f'font-family="{SANS}" font-size="15.5" font-weight="700" fill="{tcol}">'
                 f'{html.escape(name)}</text>')
    for i, ln in enumerate(wrap(role, int(w / 6.6))):
        elems.append(f'<text x="{cx:.1f}" y="{top+52+i*16:.1f}" text-anchor="middle" '
                     f'font-family="{SANS}" font-size="11" fill="{tcol}" '
                     f'opacity="{0.85 if dark else 0.7}">{html.escape(ln)}</text>')
    return dict(cx=cx, bottom=top + h)

def line(x1, y1, x2, y2):
    track(x1, y1); track(x2, y2)
    elems.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" '
                 f'stroke="{BLACK}" stroke-width="1.3" fill="none"/>')

def frame(cx, top, w, h, label):
    left = cx - w/2
    track(left, top); track(left + w, top + h)
    elems.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w}" height="{h}" rx="10" '
                 f'fill="none" stroke="{BLACK}" stroke-width="1" stroke-dasharray="6 4"/>')
    elems.append(f'<text x="{cx:.1f}" y="{top+28:.1f}" text-anchor="middle" '
                 f'font-family="{SANS}" font-size="13" font-weight="700" letter-spacing="2" '
                 f'fill="{BLACK}">{html.escape(label)}</text>')

# ---------- géométrie
DW, RW, TW = 248, 230, 196
dig, com, ate = 330, 810, 1290
Ftop, FW, FH = 258, 450, 270

# pôle direction (encadré comme les autres)
frame(810, 40, 640, 158, "PÔLE DIRECTION")
box(675, 84, DW, "Alexandra Cefai", "Créatrice de la marque", dark=True)
box(945, 84, DW, "Damien Grauvogel", "Designer produit et co-créateur", dark=True)

# bus vers les pôles (depuis le bas du cadre direction)
line(810, 198, 810, 228)
line(dig, 228, ate, 228)
for c in (dig, com, ate): line(c, 228, c, Ftop)

def tbox(cx, top, member):
    name, role = member
    box(cx, top, TW, name, role, bg=(GREEN if name == "Estelle Casterot" else None))

def pole(cx, label, resp, team):
    frame(cx, Ftop, FW, FH, label)
    r = box(cx, Ftop + 44, RW, resp[0], resp[1])
    bot = r['bottom']
    if len(team) == 2:
        c1, c2 = cx - 105, cx + 105
        line(cx, bot, cx, bot + 28)
        line(c1, bot + 28, c2, bot + 28)
        line(c1, bot + 28, c1, bot + 40); line(c2, bot + 28, c2, bot + 40)
        tbox(c1, bot + 40, team[0]); tbox(c2, bot + 40, team[1])
    else:
        line(cx, bot, cx, bot + 40)
        tbox(cx, bot + 40, team[0])

pole(dig, "PÔLE DIGITAL",
     ("Camille Abela", "Responsable e-commerce"),
     [("Estelle Casterot", "Alternante cheffe de projet e-commerce")])
pole(com, "PÔLE COMMERCIAL",
     ("Marie Homasson", "Manageuse commerciale"),
     [("Ruben Sagot", "Alternant commercial"),
      ("Lucas Mouren", "Alternant gestion entreprise")])
pole(ate, "PÔLE ATELIER",
     ("Sarah Moussaoui", "Responsable commande B2C et SAV"),
     [("Camille Noël", "Peintre"),
      ("Jennifer Lienert", "Peintre et commande")])

# ---------- viewBox
PAD = 36
minx, maxx = min(xs) - PAD, max(xs) + PAD
miny, maxy = min(ys) - PAD, max(ys) + PAD
Wt, Ht = maxx - minx, maxy - miny
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt:.0f}" height="{Ht:.0f}" '
       f'viewBox="{minx:.0f} {miny:.0f} {Wt:.0f} {Ht:.0f}">'
       f'<rect x="{minx:.0f}" y="{miny:.0f}" width="{Wt:.0f}" height="{Ht:.0f}" fill="{WHITE}"/>'
       + "".join(elems) + '</svg>')
open("organigramme_poles.svg", "w", encoding="utf-8").write(svg)
open("organigramme_poles.html", "w", encoding="utf-8").write(
    f'<!doctype html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0}}</style></head><body>{svg}</body></html>')
print(f"SVG {Wt:.0f}x{Ht:.0f}")
