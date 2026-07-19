# -*- coding: utf-8 -*-
"""Organigramme J'ai vu la Vierge — noir et blanc, épuré, sans texte autour."""
import html

WHITE = "#FFFFFF"
BLACK = "#111111"
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

def box(cx, top, w, name, role, dark=False):
    h = 84
    left = cx - w/2
    track(left, top); track(left + w, top + h)
    fill   = BLACK if dark else WHITE
    stroke = BLACK
    tname  = WHITE if dark else BLACK
    trole  = WHITE if dark else BLACK
    elems.append(f'<rect x="{left:.1f}" y="{top:.1f}" width="{w}" height="{h}" rx="2" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="1.4"/>')
    elems.append(f'<text x="{cx:.1f}" y="{top+32:.1f}" text-anchor="middle" '
                 f'font-family="{SANS}" font-size="16" font-weight="700" fill="{tname}">'
                 f'{html.escape(name)}</text>')
    maxc = int(w / 6.6)
    for i, ln in enumerate(wrap(role, maxc)):
        elems.append(f'<text x="{cx:.1f}" y="{top+53+i*16:.1f}" text-anchor="middle" '
                     f'font-family="{SANS}" font-size="11.5" fill="{trole}" '
                     f'opacity="{0.85 if dark else 0.7}">{html.escape(ln)}</text>')
    return dict(cx=cx, top=top, w=w, bottom=top + h)

def line(x1, y1, x2, y2):
    track(x1, y1); track(x2, y2)
    elems.append(f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" '
                 f'stroke="{BLACK}" stroke-width="1.3" fill="none"/>')

# ---------- construction
W1, W2 = 248, 216
colA, colB, colC = 320, 800, 1280

# direction (boîtes noires)
box(665, 60, W1, "Alexandra Cefai", "Créatrice de la marque", dark=True)
box(935, 60, W1, "Damien Grauvogel", "Designer produit et co-créateur", dark=True)
line(665, 144, 665, 166); line(935, 144, 935, 166); line(665, 166, 935, 166)
line(800, 166, 800, 200)

# bus vers responsables
line(colA, 200, colC, 200)
for cx in (colA, colB, colC): line(cx, 200, cx, 242)

mMarie = box(colA, 242, W1, "Marie Homasson", "Manageuse commerciale")
mSarah = box(colB, 242, W1, "Sarah Moussaoui", "Responsable commande B2C et SAV")
mCam   = box(colC, 242, W1, "Camille Abela", "Responsable e-commerce")

def two(mgr, r1, r2):
    cx, bot = mgr['cx'], mgr['bottom']
    c1, c2 = cx - 114, cx + 114
    line(cx, bot, cx, bot + 30)
    line(c1, bot + 30, c2, bot + 30)
    line(c1, bot + 30, c1, bot + 42); line(c2, bot + 30, c2, bot + 42)
    box(c1, bot + 42, W2, *r1); box(c2, bot + 42, W2, *r2)

def one(mgr, r):
    cx, bot = mgr['cx'], mgr['bottom']
    line(cx, bot, cx, bot + 42)
    box(cx, bot + 42, W2, *r)

two(mMarie, ("Ruben Sagot", "Alternant commercial"),
            ("Lucas Mouren", "Alternant gestion entreprise"))
two(mSarah, ("Camille Noël", "Peintre"),
            ("Jennifer Lienert", "Responsable commande (plâtre)"))
one(mCam, ("Estelle Casterot", "Alternante cheffe de projet e-commerce"))

# ---------- viewBox serré
PAD = 36
minx, maxx = min(xs) - PAD, max(xs) + PAD
miny, maxy = min(ys) - PAD, max(ys) + PAD
Wt, Ht = maxx - minx, maxy - miny
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{Wt:.0f}" height="{Ht:.0f}" '
       f'viewBox="{minx:.0f} {miny:.0f} {Wt:.0f} {Ht:.0f}">'
       f'<rect x="{minx:.0f}" y="{miny:.0f}" width="{Wt:.0f}" height="{Ht:.0f}" fill="{WHITE}"/>'
       + "".join(elems) + '</svg>')
open("organigramme.svg", "w", encoding="utf-8").write(svg)
open("organigramme.html", "w", encoding="utf-8").write(
    f'<!doctype html><html><head><meta charset="utf-8"><style>*{{margin:0;padding:0}}</style></head><body>{svg}</body></html>')
print(f"SVG {Wt:.0f}x{Ht:.0f}")
