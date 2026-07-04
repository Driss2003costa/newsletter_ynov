# -*- coding: utf-8 -*-
"""Generateur d'ornements SVG (line-art dore + botanique wisteria) pour le deck."""
import math, os

OUT = os.path.dirname(os.path.abspath(__file__)) + "/orn"
os.makedirs(OUT, exist_ok=True)

GOLD   = "#C9A227"
GOLD_L = "#E4C97E"
GOLD_D = "#A07C1F"
WIST_D = "#7E63A0"
WIST   = "#9B7FB8"
WIST_L = "#C9B8DF"
WIST_P = "#D8CCE4"
SAGE   = "#9DAE86"
SAGE_D = "#7C8C68"
BORD   = "#7A1F2B"
BORD_D = "#5E1621"
INK    = "#3A3630"
IVORY  = "#F5EFE2"


def save(name, w, h, body, extra=""):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">{extra}{body}</svg>'
    open(f"{OUT}/{name}.svg", "w").write(svg)


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def hx(c):
    return "#%02X%02X%02X" % c


def hex2rgb(s):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


# ---------------------------------------------------------------- WISTERIA SPRIG
def _floret(fx, fy, rr, c_top, c_bot, edge, op):
    """Un floret de glycine : petale en goutte, plus clair vers le bas."""
    return (
        f'<path d="M{fx:.1f} {fy-rr:.1f} '
        f'C {fx+rr*1.05:.1f} {fy-rr*0.6:.1f}, {fx+rr*0.9:.1f} {fy+rr*0.9:.1f}, {fx:.1f} {fy+rr*1.15:.1f} '
        f'C {fx-rr*0.9:.1f} {fy+rr*0.9:.1f}, {fx-rr*1.05:.1f} {fy-rr*0.6:.1f}, {fx:.1f} {fy-rr:.1f} Z" '
        f'fill="{c_bot}" opacity="{op:.2f}"/>'
        f'<ellipse cx="{fx:.1f}" cy="{fy-rr*0.25:.1f}" rx="{rr*0.62:.1f}" ry="{rr*0.5:.1f}" fill="{c_top}" opacity="{op*0.9:.2f}"/>'
        f'<ellipse cx="{fx-rr*0.24:.1f}" cy="{fy-rr*0.32:.1f}" rx="{rr*0.16:.1f}" ry="{rr*0.2:.1f}" fill="{IVORY}" opacity="0.5"/>')


def wisteria(name="wisteria", W=360, H=700, flip=False, soft=False):
    """Grappe de glycine tombante, delicate et effilee (raceme)."""
    import random
    random.seed(7)
    parts = []
    if not soft:
        # tige souple + 3 feuilles fines en haut
        parts.append(f'<path d="M{W*0.52:.0f} 6 C {W*0.42:.0f} {H*0.10:.0f}, {W*0.58:.0f} {H*0.18:.0f}, {W*0.50:.0f} {H*0.26:.0f}" '
                     f'fill="none" stroke="{SAGE_D}" stroke-width="3" stroke-linecap="round" opacity="0.6"/>')
        for (lx, ly, rot, sc) in [(0.34,0.06,-40,0.9),(0.66,0.09,34,0.8),(0.46,0.15,-14,0.7)]:
            cx, cy = W*lx, H*ly
            parts.append(f'<g transform="translate({cx:.0f},{cy:.0f}) rotate({rot}) scale({sc})">'
                         f'<path d="M0 0 C 20 -12, 44 -8, 56 3 C 44 14, 20 16, 0 3 Z" fill="{SAGE}" opacity="0.45"/>'
                         f'<path d="M2 1 L 52 3" stroke="{SAGE_D}" stroke-width="1.4" opacity="0.4"/></g>')
    # raceme : cluster effile, plus dense en haut, tail wispy
    top_y, bot_y = H*0.10, H*0.99
    rows = 40
    for r in range(rows):
        t = r / (rows - 1)
        y = top_y + (bot_y - top_y) * t
        # profil du raceme : renflement haut, longue pointe
        env = math.sin(math.pi * min(t*1.15, 1)) ** 0.7
        spread = (W*0.32) * env * (1 - 0.25*t)
        n = max(1, int(round(4.2 * env * (1 - 0.3*t))))
        if t > 0.8:
            n = 1 if r % 2 else 2
        base = t
        c_bot = hx(lerp(hex2rgb(WIST_L), hex2rgb(WIST_P), min(1, base*1.1)))
        c_top = hx(lerp(hex2rgb(WIST), hex2rgb(WIST_L), base))
        if soft:
            c_bot = c_top = WIST_L
        rr = (16 - 9*t) * (0.9 + 0.2*math.sin(r))
        for k in range(n):
            fx = W*0.5 + (spread * (((k+0.5)/n)*2 - 1)) * (0.85 + 0.15*math.sin(r+k))
            fx += random.uniform(-4, 4)
            yy = y + random.uniform(-3, 3)
            op = 0.5 if soft else random.uniform(0.72, 0.95)
            parts.append(_floret(fx, yy, rr, c_top, c_bot, WIST_D, op))
    body = "".join(parts)
    if soft:
        body = f'<g opacity="0.5">{body}</g>'
    if flip:
        body = f'<g transform="scale(-1,1) translate({-W},0)">{body}</g>'
    save(name, W, H, body)


# ---------------------------------------------------------------- CORNER FILIGREE
def filigree(name="filigree", S=300):
    """Fleuron d'angle : volute Regency doree, coin superieur gauche."""
    g = GOLD
    p = []
    # cadre d'angle en L, double filet
    p.append(f'<path d="M18 150 L18 26 Q18 18 26 18 L150 18" fill="none" stroke="{g}" stroke-width="3.2" stroke-linecap="round"/>')
    p.append(f'<path d="M28 150 L28 34 Q28 28 34 28 L150 28" fill="none" stroke="{GOLD_L}" stroke-width="1.4" stroke-linecap="round"/>')
    # volute principale
    p.append(f'<path d="M28 34 C 78 40, 104 66, 96 104 C 90 132, 60 138, 52 116 '
             f'C 47 100, 62 90, 74 98 C 82 103, 80 116, 70 116" '
             f'fill="none" stroke="{g}" stroke-width="2.6" stroke-linecap="round"/>')
    # petite volute miroir horizontale
    p.append(f'<path d="M34 28 C 40 78, 66 104, 104 96 C 132 90, 138 60, 116 52 '
             f'C 100 47, 90 62, 98 74 C 103 82, 116 80, 116 70" '
             f'fill="none" stroke="{g}" stroke-width="2.6" stroke-linecap="round"/>')
    # feuilles / bourgeons dores
    for (cx, cy, rot) in [(120,120,45),(150,58,10),(58,150,80)]:
        p.append(f'<g transform="translate({cx},{cy}) rotate({rot})">'
                 f'<path d="M0 0 C 10 -8, 26 -6, 34 2 C 26 10, 10 8, 0 0 Z" fill="{g}" opacity="0.9"/></g>')
    # rosette d'angle
    p.append(f'<circle cx="23" cy="23" r="7" fill="{g}"/><circle cx="23" cy="23" r="3" fill="{GOLD_L}"/>')
    save(name, S, S, "".join(p))


# ---------------------------------------------------------------- WAX SEAL
def wax_seal(name="seal", S=260, mono="MVR", color=BORD, dark=BORD_D):
    cx = cy = S/2
    R = S*0.42
    # bord festonne (scallops)
    scal = []
    teeth = 26
    for i in range(teeth):
        a = 2*math.pi*i/teeth
        rr = R*1.06
        x = cx + rr*math.cos(a); y = cy + rr*math.sin(a)
        scal.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R*0.075:.1f}" fill="{color}"/>')
    p = []
    p.append(f'<defs><radialGradient id="wg" cx="38%" cy="34%" r="75%">'
             f'<stop offset="0%" stop-color="{hx(lerp(hex2rgb(color),(255,255,255),0.28))}"/>'
             f'<stop offset="62%" stop-color="{color}"/>'
             f'<stop offset="100%" stop-color="{dark}"/></radialGradient></defs>')
    p += scal
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R:.1f}" fill="url(#wg)"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.82:.1f}" fill="none" stroke="{dark}" stroke-width="2" opacity="0.6"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{R*0.9:.1f}" fill="none" stroke="{hx(lerp(hex2rgb(color),(255,255,255),0.2))}" stroke-width="1" opacity="0.5"/>')
    # petite couronne de laurier interne
    for s in (-1, 1):
        p.append(f'<path d="M{cx} {cy+R*0.5:.1f} Q {cx+s*R*0.42:.1f} {cy+R*0.15:.1f} {cx+s*R*0.30:.1f} {cy-R*0.4:.1f}" '
                 f'fill="none" stroke="{hx(lerp(hex2rgb(color),(255,255,255),0.35))}" stroke-width="1.6" opacity="0.7"/>')
    # monogramme
    p.append(f'<text x="{cx}" y="{cy+S*0.055:.0f}" text-anchor="middle" '
             f'font-family="Playfair Display, Georgia, serif" font-weight="700" '
             f'font-size="{S*0.24:.0f}" fill="{hx(lerp(hex2rgb(color),(255,255,255),0.42))}" '
             f'letter-spacing="1">{mono}</text>')
    save(name, S, S, "".join(p))


# ---------------------------------------------------------------- FLORAL DIVIDER
def divider(name="divider", W=520, H=70):
    cx, cy = W/2, H/2
    g = GOLD
    p = []
    # ligne fine
    p.append(f'<line x1="30" y1="{cy}" x2="{cx-46:.0f}" y2="{cy}" stroke="{g}" stroke-width="1.4"/>')
    p.append(f'<line x1="{cx+46:.0f}" y1="{cy}" x2="{W-30}" y2="{cy}" stroke="{g}" stroke-width="1.4"/>')
    # volutes symetriques
    for s in (-1, 1):
        bx = cx + s*30
        p.append(f'<path d="M{bx:.0f} {cy} C {bx+s*24:.0f} {cy-16:.0f}, {bx+s*44:.0f} {cy-6:.0f}, {bx+s*40:.0f} {cy+6:.0f} '
                 f'C {bx+s*37:.0f} {cy+14:.0f}, {bx+s*26:.0f} {cy+10:.0f}, {bx+s*28:.0f} {cy+2:.0f}" '
                 f'fill="none" stroke="{g}" stroke-width="1.8" stroke-linecap="round"/>')
        p.append(f'<path d="M{bx:.0f} {cy} q {s*20:.0f} 14 {s*40:.0f} 8" fill="none" stroke="{SAGE}" stroke-width="1.6" opacity="0.7"/>')
    # rosette centrale
    for i in range(6):
        a = math.pi/3*i
        x = cx + 11*math.cos(a); y = cy + 11*math.sin(a)
        p.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="6.5" ry="3.4" fill="{g}" transform="rotate({math.degrees(a):.0f} {x:.1f} {y:.1f})" opacity="0.95"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="5.5" fill="{GOLD_L}"/><circle cx="{cx}" cy="{cy}" r="2.6" fill="{GOLD_D}"/>')
    save(name, W, H, "".join(p))


# ---------------------------------------------------------------- ROSETTE (bullet)
def rosette(name="rosette", S=48):
    cx = cy = S/2
    g = GOLD
    p = []
    for i in range(6):
        a = math.pi/3*i
        x = cx + S*0.22*math.cos(a); y = cy + S*0.22*math.sin(a)
        p.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{S*0.16:.1f}" ry="{S*0.085:.1f}" fill="{g}" '
                 f'transform="rotate({math.degrees(a):.0f} {x:.1f} {y:.1f})"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{S*0.12:.1f}" fill="{GOLD_L}"/>')
    p.append(f'<circle cx="{cx}" cy="{cy}" r="{S*0.055:.1f}" fill="{GOLD_D}"/>')
    save(name, S, S, "".join(p))


# ---------------------------------------------------------------- HERALDIC BEE
def bee(name="bee", W=120, H=90):
    cx, cy = W*0.5, H*0.56
    p = []
    # ailes
    for s in (-1, 1):
        p.append(f'<ellipse cx="{cx+s*20:.0f}" cy="{cy-18:.0f}" rx="20" ry="12" fill="{GOLD_L}" opacity="0.55" '
                 f'transform="rotate({s*25} {cx+s*20:.0f} {cy-18:.0f})"/>')
        p.append(f'<ellipse cx="{cx+s*20:.0f}" cy="{cy-18:.0f}" rx="20" ry="12" fill="none" stroke="{GOLD}" stroke-width="1.2" '
                 f'transform="rotate({s*25} {cx+s*20:.0f} {cy-18:.0f})" opacity="0.7"/>')
    # corps
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="16" ry="22" fill="{GOLD}"/>')
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="16" ry="22" fill="none" stroke="{GOLD_D}" stroke-width="1.4"/>')
    # rayures
    for dy in (-8, 2, 12):
        p.append(f'<line x1="{cx-14:.0f}" y1="{cy+dy}" x2="{cx+14:.0f}" y2="{cy+dy}" stroke="{GOLD_D}" stroke-width="2.4" opacity="0.85"/>')
    # tete
    p.append(f'<circle cx="{cx}" cy="{cy-24:.0f}" r="7" fill="{GOLD_D}"/>')
    save(name, W, H, "".join(p))


wisteria("wisteria")
wisteria("wisteria_r", flip=True)
wisteria("wisteria_soft", soft=True)
filigree("filigree")
wax_seal("seal_mvr", mono="MVR")
wax_seal("seal_lw", mono="LW")
divider("divider")
rosette("rosette")
bee("bee")
print("SVG generes dans", OUT)
print(os.listdir(OUT))
