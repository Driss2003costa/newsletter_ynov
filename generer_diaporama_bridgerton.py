# -*- coding: utf-8 -*-
"""
Diaporama PowerPoint 16:9, esthetique Regencycore (serie Bridgerton).
Sujet et donnees : projet BC-5 e-business du Musee de la Vie Romantique
(dossier "BC-5 Estelle Casterot", concept Love Stories IRL).

Le design est concu en px sur une grille 1280x720 puis porte a l'identique
en EMU (1 px = 9525 EMU) et en points (1 pt = 0,75 px), ce qui reproduit
fidelement la maquette validee.

Formes natives et editables (add_textbox, add_shape, add_table, add_picture).
Les ornements (glycine, cachets de cire, fleurons, rosettes, abeille) sont de
petites images vectorielles PNG a fond transparent, jamais une image plaquee en
diapo entiere. Les deux polices (Playfair Display, EB Garamond) sont EMBARQUEES
dans le fichier .pptx ; des TTF sont fournis dans assets/fonts si substitution.
"""

# --- En-tete impose -----------------------------------------------------------
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
# ------------------------------------------------------------------------------

import os, zipfile, shutil, copy

BASE = os.path.dirname(os.path.abspath(__file__))
ORN  = os.path.join(BASE, "assets", "ornaments")
FONTDIR = os.path.join(BASE, "assets", "fonts")

# =========================== CONSTANTES DE STYLE ==============================
# Palette Bridgerton (ivoire, bleus poudres, glycine, dorures).
IVOIRE        = RGBColor(0xF5, 0xEF, 0xE2)
PORCELAINE    = RGBColor(0xFB, 0xF8, 0xF1)
BLEU_POUDRE   = RGBColor(0xA9, 0xC3, 0xD6)
BLEU_CIEL     = RGBColor(0xC4, 0xD8, 0xE4)
BLEU_WEDGWOOD = RGBColor(0x6E, 0x93, 0xAE)
LILAS         = RGBColor(0xC9, 0xB8, 0xDF)
WISTERIA      = RGBColor(0x9B, 0x7F, 0xB8)
MAUVE         = RGBColor(0xD8, 0xCC, 0xE4)
ROSE_POUDRE   = RGBColor(0xEB, 0xD3, 0xD8)
SAUGE         = RGBColor(0x9D, 0xAE, 0x86)
OR_CHAMPAGNE  = RGBColor(0xE4, 0xC9, 0x7E)
OR_RICHE      = RGBColor(0xC9, 0xA2, 0x27)
OR_BRONZE     = RGBColor(0xA0, 0x7C, 0x1F)
ENCRE         = RGBColor(0x3A, 0x36, 0x30)
ENCRE_DOUCE   = RGBColor(0x6B, 0x62, 0x5A)
CIRE_BORDEAUX = RGBColor(0x7A, 0x1F, 0x2B)
# Palette Featherington (rupture ponctuelle, 1 diapo)
F_CITRUS      = RGBColor(0xF2, 0xC5, 0x17)
F_VERT_POMME  = RGBColor(0x8F, 0xC9, 0x3A)
F_MANDARINE   = RGBColor(0xE8, 0x79, 0x2B)
F_FUCHSIA     = RGBColor(0xD9, 0x4F, 0x8A)

# Deux familles de polices maximum (embarquees dans le pptx).
TITLE_FONT = "Playfair Display"   # serif Didone a fort contraste (titres, chiffres)
BODY_FONT  = "EB Garamond"        # corps

# Grille de conception : 1280 x 720 px.
EMU_PER_PX = 9525
PT_PER_PX  = 0.75

def PXX(px):   # coordonnee / dimension horizontale (EMU)
    return Emu(int(round(px * EMU_PER_PX)))
PXY = PXX      # meme facteur en vertical (7,5 in = 720 px exactement)
def PT(px):
    return Pt(px * PT_PER_PX)

SW_PX, SH_PX = 1280, 720
MX_PX = 90     # marge laterale
ROMAINS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

# tailles natives des ornements (pour conserver le ratio)
NATIVE = {
    'wisteria': (360, 700), 'wisteria_r': (360, 700), 'wisteria_soft': (360, 700),
    'seal_mvr': (260, 260), 'seal_lw': (260, 260), 'filigree': (300, 300),
    'rosette': (48, 48), 'bee': (120, 90), 'divider': (520, 70),
}

_used_gabarits = []
_page = 0


# =============================== UTILITAIRES ==================================
def _no_shadow(shape):
    shape.shadow.inherit = False

def send_to_back(shape, slide):
    sp = shape._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)

def rect(slide, x, y, w, h, fill=None, line=None, line_pt=1.0, back=False):
    """Rectangle natif. fill/line en RGBColor ; None = transparent."""
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PXX(x), PXY(y), PXX(w), PXY(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_pt)
    _no_shadow(shp)
    if back:
        send_to_back(shp, slide)
    return shp

def add_background(slide, color=IVOIRE):
    return rect(slide, 0, 0, SW_PX, SH_PX, fill=color, back=True)

def hrule(slide, x, y, w, color=OR_RICHE, thick_emu_pt=1.0):
    """Filet horizontal fin (epaisseur en points)."""
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PXX(x), PXY(y), PXX(w), Pt(thick_emu_pt))
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    shp.line.fill.background(); _no_shadow(shp)
    return shp

def vrule(slide, x, y, h, color=OR_RICHE, thick_emu_pt=1.0):
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, PXX(x), PXY(y), Pt(thick_emu_pt), PXY(h))
    shp.fill.solid(); shp.fill.fore_color.rgb = color
    shp.line.fill.background(); _no_shadow(shp)
    return shp

def R(text, size_px, color=ENCRE, bold=False, italic=False, font=BODY_FONT,
      track=None, upper=False):
    return dict(text=text.upper() if upper else text, size=size_px, color=color,
                bold=bold, italic=italic, font=font, track=track)

def add_text(slide, x, y, w, h, paras, anchor=MSO_ANCHOR.TOP):
    """paras : liste de dicts {'runs':[R...], 'align', 'line', 'before', 'after'}."""
    tb = slide.shapes.add_textbox(PXX(x), PXY(y), PXX(w), PXY(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0
    tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = para.get('align', PP_ALIGN.LEFT)
        if para.get('line'):
            p.line_spacing = para['line']
        if para.get('before') is not None:
            p.space_before = Pt(para['before'])
        if para.get('after') is not None:
            p.space_after = Pt(para['after'])
        for spec in para['runs']:
            run = p.add_run()
            run.text = spec['text']
            f = run.font
            f.name = spec['font']; f.size = PT(spec['size'])
            f.bold = spec['bold']; f.italic = spec['italic']
            f.color.rgb = spec['color']
            if spec.get('track'):
                run._r.get_or_add_rPr().set('spc', str(int(spec['track'] * 100)))
    return tb

def set_pic_alpha(pic, pct):
    blip = pic._element.find(qn('p:blipFill')).find(qn('a:blip'))
    blip.append(blip.makeelement(qn('a:alphaModFix'), {'amt': str(int(pct * 1000))}))

def pic(slide, name, x, y, w=None, h=None, opacity=None, flip=False, rot=None):
    nw, nh = NATIVE[name]
    if w is None and h is not None:
        w = h * nw / nh
    if h is None and w is not None:
        h = w * nh / nw
    p = slide.shapes.add_picture(os.path.join(ORN, name + ".png"),
                                 PXX(x), PXY(y), PXX(w), PXY(h))
    if opacity is not None:
        set_pic_alpha(p, opacity)
    if flip:
        p._element.spPr.xfrm.set('flipH', '1')
    if rot is not None:
        p.rotation = rot
    _no_shadow(p)
    return p

def safe_pic(slide, name, x, y, w=None, h=None, **kw):
    """add_picture si l'ornement existe, sinon place un discret marqueur (aucun crash)."""
    path = os.path.join(ORN, name + ".png")
    if os.path.exists(path):
        return pic(slide, name, x, y, w, h, **kw)
    nw, nh = NATIVE.get(name, (100, 100))
    if w is None and h is not None: w = h * nw / nh
    if h is None and w is not None: h = w * nh / nw
    ph = rect(slide, x, y, w or 60, h or 60, fill=None, line=OR_RICHE, line_pt=0.75)
    print("  [ornement absent] marqueur :", path)
    return ph

def _new_slide():
    global _page
    _page += 1
    return prs.slides.add_slide(prs.slide_layouts[6])

def divider_rule(slide, cx, y, total_w, mark="rosette", mark_px=22):
    """Filet dore centre avec un petit ornement au milieu."""
    half = (total_w - mark_px - 28) / 2
    hrule(slide, cx - total_w/2, y + mark_px/2, half)
    hrule(slide, cx + mark_px/2 + 14, y + mark_px/2, half)
    if mark == "bee":
        safe_pic(slide, "bee", cx - 20, y - 3, w=40)
    else:
        safe_pic(slide, "rosette", cx - mark_px/2, y, w=mark_px)

def eyebrow_title(slide, eyebrow, title, x=MX_PX, y=92, w=1100, accent=OR_BRONZE):
    add_text(slide, x, y, w, 22,
             [{'runs': [R(eyebrow, 15, accent, True, False, BODY_FONT, track=4, upper=True)]}])
    add_text(slide, x, y + 24, w, 60,
             [{'runs': [R(title, 46, ENCRE, True, False, TITLE_FONT)]}])
    safe_pic(slide, "rosette", x, y + 96, w=22)
    hrule(slide, x + 34, y + 101, w - 34, OR_RICHE)

def footer(slide, running="Musee de la Vie Romantique"):
    add_text(slide, MX_PX, 686, 500, 18,
             [{'runs': [R(running, 12.5, ENCRE_DOUCE, False, True, BODY_FONT, track=1)]}])
    add_text(slide, SW_PX - MX_PX - 200, 686, 200, 18,
             [{'runs': [R(str(_page).rjust(2), 12.5, OR_BRONZE, False, False, BODY_FONT, track=2)]}],
             )  # numero a droite
    tb = slide.shapes[-1]; tb.text_frame.paragraphs[0].alignment = PP_ALIGN.RIGHT


# ================================ GABARITS ===================================
def slide_couverture(titre_a, titre_b, eyebrow, sous_titre, ouverture, auteur_date):
    _used_gabarits.append("couverture")
    s = _new_slide()
    add_background(s, IVOIRE)
    rect(s, 44, 44, SW_PX-88, SH_PX-88, fill=None, line=OR_RICHE, line_pt=1.5)
    rect(s, 52, 52, SW_PX-104, SH_PX-104, fill=None, line=OR_CHAMPAGNE, line_pt=0.75)
    pic(s, "wisteria",   44, 44, h=360, opacity=90)
    pic(s, "wisteria_r", SW_PX-44-185, 44, h=360, opacity=90)
    cx = SW_PX/2
    add_text(s, 140, 232, SW_PX-280, 22,
             [{'runs': [R(eyebrow, 16, OR_BRONZE, True, False, BODY_FONT, track=4, upper=True)],
               'align': PP_ALIGN.CENTER}])
    add_text(s, 140, 258, SW_PX-280, 110,
             [{'runs': [R(titre_a + " ", 92, ENCRE, True, False, TITLE_FONT),
                        R(titre_b, 92, ENCRE, True, True, TITLE_FONT)],
               'align': PP_ALIGN.CENTER}])
    divider_rule(s, cx, 386, 420)
    add_text(s, 140, 424, SW_PX-280, 34,
             [{'runs': [R(sous_titre, 21, BLEU_WEDGWOOD, False, True, BODY_FONT)],
               'align': PP_ALIGN.CENTER}])
    add_text(s, 140, 470, SW_PX-280, 30,
             [{'runs': [R(ouverture, 18, ENCRE_DOUCE, False, True, BODY_FONT)],
               'align': PP_ALIGN.CENTER}])
    safe_pic(s, "seal_mvr", cx-48, 560, w=96)
    add_text(s, 0, 662, SW_PX, 22,
             [{'runs': [R(auteur_date, 14, ENCRE_DOUCE, False, False, BODY_FONT, track=2, upper=True)],
               'align': PP_ALIGN.CENTER}])
    return s


def slide_sommaire(titre, entries):
    _used_gabarits.append("sommaire")
    s = _new_slide()
    add_background(s, IVOIRE)
    pic(s, "wisteria_soft", SW_PX-30-154, -120, h=300, opacity=40)
    add_text(s, 0, 74, SW_PX, 52,
             [{'runs': [R(titre, 44, ENCRE, True, False, TITLE_FONT)], 'align': PP_ALIGN.CENTER}])
    divider_rule(s, SW_PX/2, 132, 300)
    top, row_h = 196, 92
    lx, rx = 150, SW_PX-150
    for i, (num, code, title) in enumerate(entries):
        y = top + i*row_h
        if i:
            hrule(s, lx, y, rx-lx, OR_CHAMPAGNE, 0.75)
        add_text(s, lx, y+18, 88, 56,
                 [{'runs': [R(num, 40, OR_RICHE, True, False, TITLE_FONT)], 'align': PP_ALIGN.CENTER}],
                 anchor=MSO_ANCHOR.MIDDLE)
        add_text(s, lx+112, y+22, rx-lx-160, 20,
                 [{'runs': [R(code, 12.5, OR_BRONZE, True, False, BODY_FONT, track=3, upper=True)]}])
        add_text(s, lx+112, y+40, rx-lx-160, 32,
                 [{'runs': [R(title, 26, ENCRE, True, False, TITLE_FONT)]}])
        safe_pic(s, "rosette", rx-18, y+row_h/2-9, w=18)
    footer(s)
    return s


def slide_section(num, code, titre, aparte):
    _used_gabarits.append("section")
    s = _new_slide()
    add_background(s, BLEU_CIEL)
    pic(s, "wisteria_r", SW_PX-40-232, 0, h=440, opacity=85)
    pic(s, "wisteria", 30, SH_PX-120-185, h=360, opacity=50)
    safe_pic(s, "filigree", 40, 40, w=120)
    safe_pic(s, "filigree", SW_PX-40-120, SH_PX-40-120, w=120, rot=180)
    add_text(s, 0, 150, SW_PX, 200,
             [{'runs': [R(num, 200, OR_RICHE, True, False, TITLE_FONT)], 'align': PP_ALIGN.CENTER}])
    add_text(s, 0, 372, SW_PX, 22,
             [{'runs': [R(code, 16, BLEU_WEDGWOOD, True, False, BODY_FONT, track=3, upper=True)],
               'align': PP_ALIGN.CENTER}])
    add_text(s, 0, 398, SW_PX, 66,
             [{'runs': [R(titre, 56, ENCRE, True, False, TITLE_FONT)], 'align': PP_ALIGN.CENTER}])
    divider_rule(s, SW_PX/2, 486, 360)
    add_text(s, 200, 520, SW_PX-400, 40,
             [{'runs': [R(aparte, 20, ENCRE_DOUCE, False, True, BODY_FONT)],
               'align': PP_ALIGN.CENTER, 'line': 1.3}])
    return s


def slide_contenu(eyebrow, titre, elements, source):
    _used_gabarits.append("contenu")
    s = _new_slide()
    add_background(s, IVOIRE)
    pic(s, "wisteria_soft", SW_PX-160, SH_PX-160-185, h=340, opacity=45)
    eyebrow_title(s, eyebrow, titre)
    y = 320
    for el in elements:
        safe_pic(s, "rosette", 112, y+6, w=22)
        add_text(s, 146, y, SW_PX-146-120, 60,
                 [{'runs': [R(el, 24, ENCRE, False, False, BODY_FONT)], 'line': 1.4}])
        y += 78
    add_text(s, MX_PX, 664, 900, 20,
             [{'runs': [R(source, 13, ENCRE_DOUCE, False, True, BODY_FONT)]}])
    footer(s)
    return s


def slide_tableau(eyebrow, titre, headers, rows, right_cols, ratios, source):
    _used_gabarits.append("tableau")
    s = _new_slide()
    add_background(s, IVOIRE)
    eyebrow_title(s, eyebrow, titre)
    n_cols, n_rows = len(headers), len(rows) + 1
    left, top, width = MX_PX, 262, SW_PX - 2*MX_PX
    header_h, body_h = 40, 34
    hrule(s, left, top-2, width, OR_RICHE, 2.0)   # filet dore au-dessus
    gf = s.shapes.add_table(n_rows, n_cols, PXX(left), PXY(top), PXX(width),
                            PXY(header_h + body_h*len(rows)))
    table = gf.table
    # retirer le style par defaut
    tblPr = table._tbl.find(qn('a:tblPr'))
    tblPr.set('firstRow', '0'); tblPr.set('bandRow', '0')
    sid = tblPr.find(qn('a:tableStyleId'))
    if sid is None:
        sid = tblPr.makeelement(qn('a:tableStyleId'), {}); tblPr.append(sid)
    sid.text = '{2D5ABB26-0587-4C30-8999-92F81FD0307C}'
    tot = float(sum(ratios))
    for j, rt in enumerate(ratios):
        table.columns[j].width = PXX(width * rt / tot)
    table.rows[0].height = PXY(header_h)
    for i in range(1, n_rows):
        table.rows[i].height = PXY(body_h)

    def fill_cell(cell, txt, size, color, bold, align, bg):
        cell.fill.solid(); cell.fill.fore_color.rgb = bg
        cell.margin_left = PXX(18); cell.margin_right = PXX(18)
        cell.margin_top = PXX(4); cell.margin_bottom = PXX(4)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]; p.alignment = align
        r = p.add_run(); r.text = txt
        r.font.name = BODY_FONT; r.font.size = PT(size)
        r.font.bold = bold; r.font.color.rgb = color
        if not bold:
            r._r.get_or_add_rPr().set('spc', "0")

    for j, head in enumerate(headers):
        al = PP_ALIGN.RIGHT if j in right_cols else PP_ALIGN.LEFT
        c = table.cell(0, j)
        fill_cell(c, head.upper(), 13, OR_BRONZE, True, al, PORCELAINE)
        c.text_frame.paragraphs[0].runs[0]._r.get_or_add_rPr().set('spc', "200")
    for i, row in enumerate(rows):
        bg = IVOIRE if i % 2 == 0 else PORCELAINE
        last = (i == len(rows) - 1)
        for j, val in enumerate(row):
            al = PP_ALIGN.RIGHT if j in right_cols else PP_ALIGN.LEFT
            bold = last or (j == 0)
            fill_cell(table.cell(i+1, j), str(val), 15.5, ENCRE, bold, al, bg)
    hrule(s, left, top + header_h, width, OR_RICHE, 1.2)          # filet sous l'en-tete
    hrule(s, left, top + header_h + body_h*len(rows), width, OR_RICHE, 1.0)  # filet bas
    add_text(s, MX_PX, 664, 900, 20,
             [{'runs': [R(source, 13, ENCRE_DOUCE, False, True, BODY_FONT)]}])
    footer(s)
    return s


def slide_kpi(eyebrow, titre, cartes, source, theme="or"):
    _used_gabarits.append("kpi")
    s = _new_slide()
    if theme == "feather":
        bg, acc, num = F_CITRUS, F_MANDARINE, F_FUCHSIA
    else:
        bg, acc, num = IVOIRE, OR_RICHE, OR_RICHE
    add_background(s, bg)
    if theme != "feather":
        pic(s, "wisteria_soft", SW_PX-10-185, SH_PX-160-170, h=340, opacity=45)
    eyebrow_title(s, eyebrow, titre, accent=(OR_BRONZE if theme != "feather" else F_MANDARINE))
    # panneau
    px0, py0, pw, ph = MX_PX, 300, SW_PX-2*MX_PX, 216
    rect(s, px0, py0, pw, ph, fill=PORCELAINE, line=acc, line_pt=1.0)
    n = len(cartes)
    col_w = pw / n
    for i, c in enumerate(cartes):
        cx = px0 + i*col_w
        if i:
            vrule(s, cx, py0+30, ph-60, acc, 1.0)
        add_text(s, cx, py0+42, col_w, 70,
                 [{'runs': [R(c['value'], 60, num, True, False, TITLE_FONT)], 'align': PP_ALIGN.CENTER}],
                 anchor=MSO_ANCHOR.MIDDLE)
        hrule(s, cx+col_w/2-20, py0+122, 40, acc, 1.0)
        add_text(s, cx+16, py0+138, col_w-32, 60,
                 [{'runs': [R(c['label'], 13, ENCRE, False, False, BODY_FONT, track=1)],
                   'align': PP_ALIGN.CENTER, 'line': 1.3}], anchor=MSO_ANCHOR.TOP)
    add_text(s, MX_PX, 636, 900, 20,
             [{'runs': [R(source, 13, ENCRE_DOUCE, False, True, BODY_FONT)]}])
    footer(s)
    return s


def slide_citation(texte, auteur, source=""):
    _used_gabarits.append("citation")
    s = _new_slide()
    add_background(s, IVOIRE)
    pic(s, "wisteria_soft", -40, -140, h=360, opacity=45, flip=True)
    pic(s, "wisteria_soft", SW_PX-40-185, SH_PX-160-190, h=360, opacity=45)
    add_text(s, 180, 132, SW_PX-360, 90,
             [{'runs': [R("“", 140, OR_RICHE, True, False, TITLE_FONT)], 'align': PP_ALIGN.CENTER}])
    add_text(s, 180, 240, SW_PX-360, 120,
             [{'runs': [R(texte, 40, ENCRE, False, True, TITLE_FONT)],
               'align': PP_ALIGN.CENTER, 'line': 1.35}])
    divider_rule(s, SW_PX/2, 402, 300, mark="bee", mark_px=40)
    add_text(s, 0, 452, SW_PX, 24,
             [{'runs': [R(auteur, 16, OR_BRONZE, True, False, BODY_FONT, track=3, upper=True)],
               'align': PP_ALIGN.CENTER}])
    safe_pic(s, "seal_lw", SW_PX/2-46, 556, w=92)
    if source:
        add_text(s, 0, 678, SW_PX, 18,
                 [{'runs': [R(source, 11, ENCRE_DOUCE, False, True, BODY_FONT)], 'align': PP_ALIGN.CENTER}])
    return s


def slide_cloture(titre, contact, signature):
    _used_gabarits.append("cloture")
    s = _new_slide()
    add_background(s, IVOIRE)
    rect(s, 44, 44, SW_PX-88, SH_PX-88, fill=None, line=OR_RICHE, line_pt=1.5)
    rect(s, 52, 52, SW_PX-104, SH_PX-104, fill=None, line=OR_CHAMPAGNE, line_pt=0.75)
    pic(s, "wisteria",   44, 44, h=320, opacity=85)
    pic(s, "wisteria_r", SW_PX-44-165, 44, h=320, opacity=85)
    add_text(s, 140, 250, SW_PX-280, 90,
             [{'runs': [R(titre, 72, ENCRE, True, False, TITLE_FONT)], 'align': PP_ALIGN.CENTER}])
    divider_rule(s, SW_PX/2, 356, 360)
    add_text(s, 140, 392, SW_PX-280, 30,
             [{'runs': [R(contact, 20, BLEU_WEDGWOOD, False, True, BODY_FONT)], 'align': PP_ALIGN.CENTER}])
    safe_pic(s, "seal_lw", SW_PX/2-55, 470, w=110)
    add_text(s, 0, 610, SW_PX, 30,
             [{'runs': [R(signature, 22, ENCRE, False, True, TITLE_FONT)], 'align': PP_ALIGN.CENTER}])
    return s


# ============================ CONSTRUCTION DU DECK ============================
# Donnees issues exclusivement du dossier BC-5 (Musee de la Vie Romantique).

slide_couverture(
    "Love Stories", "IRL",
    "Musee de la Vie Romantique · Paris 9e",
    "Projet BC-5 · Conception de l'experience client, option e-business",
    "Cher Aimable Lecteur, voici un musee adore du Tout-Paris, et ignore du numerique.",
    "Estelle Casterot · Annee 2025-2026",
)

slide_sommaire("Sommaire", [
    ("I", "C5.1", "Benchmark sectoriel"),
    ("II", "C5.2", "Tableau de bord des donnees"),
    ("III", "C5.4", "Plan marketing operationnel"),
    ("IV", "C5.6", "Leviers digitaux"),
    ("V", "C5.8", "Campagne e-mailing"),
])

# --- Section I : C5.1 ---
slide_section("I", "C5.1 · Analyse strategique", "Benchmark sectoriel",
              "Cher Aimable Lecteur, le retard se mesure, et il se rattrape.")
slide_kpi("C5.1 · Benchmark sectoriel", "Reperes de marche", [
    {'value': "8,7 M", 'label': "visiteurs / an\nLouvre"},
    {'value': "3,7 M", 'label': "visiteurs / an\nOrsay"},
    {'value': "1,4 M", 'label': "visiteurs / an\nAteliers Lumieres"},
    {'value': "+25 %", 'label': "visites -30 ans\navec le numerique"},
], "Source : reperes de marche, sources de veille (BC-5, C5.1).")
slide_tableau("C5.1 · Benchmark sectoriel", "Scorecard ponderee",
    ["Critere (poids)", "Vie Rom.", "G. Moreau", "Orsay", "At. Lumieres", "Louvre"],
    [["Offre digitale (20 %)", "2 / 5", "2 / 5", "4 / 5", "4 / 5", "5 / 5"],
     ["Presence sociale (20 %)", "2 / 5", "2 / 5", "3 / 5", "5 / 5", "5 / 5"],
     ["UX mobile / site (15 %)", "2 / 5", "2 / 5", "4 / 5", "4 / 5", "3 / 5"],
     ["Mediation / immersion (15 %)", "3 / 5", "3 / 5", "4 / 5", "5 / 5", "4 / 5"],
     ["Notoriete / frequentation (15 %)", "2 / 5", "2 / 5", "4 / 5", "4 / 5", "5 / 5"],
     ["Differenciation identitaire (15 %)", "5 / 5", "4 / 5", "3 / 5", "3 / 5", "3 / 5"],
     ["Score pondere global", "2,6 / 5", "2,5 / 5", "3,7 / 5", "4,2 / 5", "4,3 / 5"]],
    right_cols=[1, 2, 3, 4, 5], ratios=[2.4, 1, 1.05, 0.9, 1.15, 0.95],
    source="Notation 1 a 5, analyse octobre 2025 (BC-5, C5.1).")

# --- Section II : C5.2 ---
slide_section("II", "C5.2 · Pilotage", "Tableau de bord des donnees",
              "Des cibles, pas des resultats. Le dispositif ouvre en fevrier 2026.")
slide_kpi("C5.2 · Tableau de bord", "Cibles du dispositif", [
    {'value': "≈ 2 %", 'label': "engagement Instagram\n(cible compte)"},
    {'value': "1 500", 'label': "scans QR\npar trimestre"},
    {'value': "60 %", 'label': "ecoute complete\ndes capsules"},
    {'value': "300", 'label': "posts #AdopteTonRomantique\nsur 6 mois"},
], "Projection, dispositif non deploye (BC-5, C5.2).")
slide_tableau("C5.2 · Tableau de bord", "Indicateurs economiques",
    ["Indicateur", "Calcul", "Repere"],
    [["Cout par scan QR", "4 000 € / 1 500 scans vises", "≈ 2,7 € par scan"],
     ["Cout par lead (quiz)", "1 200 € / 2 000 leads vises", "≈ 0,6 € par lead"],
     ["Seuil de rentabilite indirect", "21 500 € / panier indirect ≈ 6 €", "≈ 3 600 visites"]],
    right_cols=[2], ratios=[1.15, 1.75, 1.0],
    source="Reperes economiques de pilotage (BC-5, C5.2).")

# --- Section III : C5.4 ---
slide_section("III", "C5.4 · Operationnel", "Plan marketing operationnel",
              "Cher Aimable Lecteur, 21 500 euros, et nul tapage inutile.")
slide_kpi("C5.4 · Plan marketing operationnel", "Budget : 21 500 €", [
    {'value': "5 500 €", 'label': "creation\nde contenus"},
    {'value': "4 000 €", 'label': "signaletique\net QR"},
    {'value': "2 000 €", 'label': "publicite\nde lancement"},
    {'value': "2 000 €", 'label': "influence\net partenariats"},
], "4 postes sur 9, enveloppe totale 21 500 € (BC-5, C5.4).", theme="feather")
slide_tableau("C5.4 · Plan marketing operationnel", "Plan d'actions operationnel",
    ["Etape", "Action", "Objectif / KPI", "Budget"],
    [["Sensibiliser", "Sondages et teasing", "Portee +50 %", "500 €"],
     ["Decouvrir", "Quiz love story et page", "2 000 leads", "1 200 €"],
     ["Donner envie", "Reels et ecoles d'art", "50 k vues", "2 000 €"],
     ["Vivre la visite", "QR codes et capsules audio", "1 500 scans", "4 000 €"],
     ["Amplifier", "UGC #AdopteTonRomantique", "300 posts", "2 000 €"]],
    right_cols=[3], ratios=[1.05, 1.75, 1.15, 0.7],
    source="Plan d'actions sur 12 mois (BC-5, C5.4).")

# --- Section IV : C5.6 ---
slide_section("IV", "C5.6 · Acquisition", "Leviers digitaux",
              "Le gratuit d'abord. Le payant, reserve aux beaux jours.")
slide_tableau("C5.6 · Leviers digitaux", "Leviers prioritaires",
    ["Famille", "Levier", "Priorite"],
    [["Utilisateurs", "Micro-influence culture / Paris", "Haute"],
     ["Utilisateurs", "Avis Google / TripAdvisor", "Haute"],
     ["Utilisateurs", "UGC #AdopteTonRomantique", "Haute"],
     ["Marque", "SEO (refonte)", "Haute"],
     ["Marque", "SMO", "Haute"],
     ["Payants", "SEA (Google Ads)", "Moyenne"],
     ["Payants", "Display / retargeting", "Basse"]],
    right_cols=[], ratios=[1.0, 2.1, 0.9],
    source="Analyse des leviers digitaux (BC-5, C5.6).")
slide_contenu("C5.6 · Leviers digitaux", "Arbitrage organique / payant", [
    "Payant : environ 4 000 €, moins d'un cinquieme du budget.",
    "Organique : 70 a 80 % de l'effort (SEO, SMO, UGC, micro-influence).",
    "Payant reserve aux temps forts (Saint-Valentin, lancement).",
], "Arbitrage derive du budget 21 500 € (BC-5, C5.6).")

# --- Section V : C5.8 ---
slide_section("V", "C5.8 · Fidelisation", "Campagne e-mailing",
              "Le seul canal que le musee possede vraiment.")
slide_tableau("C5.8 · Campagne e-mailing", "Objectifs de delivrabilite",
    ["Indicateur", "Cible", "Source"],
    [["Taux d'ouverture", "≥ 40 %", "Brevo 2025"],
     ["Reactivite (CTOR)", "≥ 12 %", "Brevo 2025"],
     ["Taux de clic (CTR)", "≥ 4 %", "Brevo 2025"],
     ["Taux de desabonnement", "< 0,5 %", "bonne pratique"],
     ["Contacts opt-in / RGPD", "100 %", "double opt-in, UE"]],
    right_cols=[1], ratios=[1.5, 0.8, 1.1],
    source="Objectifs et delivrabilite, cibles sourcees (BC-5, C5.8).")

slide_citation("Un musee qui murmure peut se faire entendre, s'il choisit bien ses mots.",
               "Lady Whistledown", "Fil rouge narratif du dossier.")

slide_cloture("Love Stories IRL",
              "Reouverture fevrier 2026 · @museevieromantique · #AdopteTonRomantique",
              "Bien a vous, Lady Whistledown")


# ============================ POLICES EMBARQUEES =============================
def embed_fonts(pptx_path, families):
    """Embarque des TTF dans le .pptx (embeddedFontLst OOXML). families = liste de
    dicts {typeface, regular, bold, italic, boldItalic} (chemins TTF ou None)."""
    P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    Rns = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    CT = 'http://schemas.openxmlformats.org/package/2006/content-types'
    REL = 'http://schemas.openxmlformats.org/package/2006/relationships'
    from lxml import etree
    tmp = pptx_path + ".tmp"
    zin = zipfile.ZipFile(pptx_path, 'r')
    names = zin.namelist()
    data = {n: zin.read(n) for n in names}
    zin.close()

    # 1) parties polices
    font_parts = []          # (partname, bytes)
    rels_add = []            # (rid, target)
    embfonts = []            # (typeface, {style: rid})
    idx = 0
    rid_n = 1000
    for fam in families:
        styles = {}
        for style in ('regular', 'bold', 'italic', 'boldItalic'):
            path = fam.get(style)
            if not path or not os.path.exists(path):
                continue
            idx += 1
            part = f"ppt/fonts/font{idx}.fntdata"
            font_parts.append((part, open(path, 'rb').read()))
            rid = f"rIdFont{rid_n}"; rid_n += 1
            rels_add.append((rid, f"fonts/font{idx}.fntdata"))
            styles[style] = rid
        if styles:
            embfonts.append((fam['typeface'], styles))

    # 2) [Content_Types].xml : default fntdata
    ct = etree.fromstring(data['[Content_Types].xml'])
    if not any(d.get('Extension') == 'fntdata' for d in ct.findall(f'{{{CT}}}Default')):
        d = etree.SubElement(ct, f'{{{CT}}}Default')
        d.set('Extension', 'fntdata'); d.set('ContentType', 'application/x-fontdata')
    data['[Content_Types].xml'] = etree.tostring(ct, xml_declaration=True, encoding='UTF-8', standalone=True)

    # 3) presentation.xml.rels
    relp = 'ppt/_rels/presentation.xml.rels'
    rels = etree.fromstring(data[relp])
    for rid, target in rels_add:
        r = etree.SubElement(rels, f'{{{REL}}}Relationship')
        r.set('Id', rid); r.set('Type', f'{Rns}/font'); r.set('Target', target)
    data[relp] = etree.tostring(rels, xml_declaration=True, encoding='UTF-8', standalone=True)

    # 4) presentation.xml : embedTrueTypeFonts + embeddedFontLst apres notesSz
    pres = etree.fromstring(data['ppt/presentation.xml'])
    pres.set('embedTrueTypeFonts', '1'); pres.set('saveSubsetFonts', '0')
    lst = etree.Element(f'{{{P}}}embeddedFontLst')
    for typeface, styles in embfonts:
        ef = etree.SubElement(lst, f'{{{P}}}embeddedFont')
        fo = etree.SubElement(ef, f'{{{P}}}font'); fo.set('typeface', typeface)
        for style in ('regular', 'bold', 'italic', 'boldItalic'):
            if style in styles:
                el = etree.SubElement(ef, f'{{{P}}}{style}')
                el.set(f'{{{Rns}}}id', styles[style])
    notesSz = pres.find(f'{{{P}}}notesSz')
    pres.insert(list(pres).index(notesSz) + 1, lst)
    data['ppt/presentation.xml'] = etree.tostring(pres, xml_declaration=True, encoding='UTF-8', standalone=True)

    # 5) reecrire le zip
    zout = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
    for n, b in data.items():
        zout.writestr(n, b)
    for part, b in font_parts:
        zout.writestr(part, b)
    zout.close()
    shutil.move(tmp, pptx_path)
    return len(font_parts)


# =============================== ENREGISTREMENT ===============================
prs.save("sortie.pptx")

_families = [
    {'typeface': TITLE_FONT,
     'regular': f"{FONTDIR}/PlayfairDisplay-Regular.ttf",
     'bold': f"{FONTDIR}/PlayfairDisplay-Bold.ttf",
     'italic': f"{FONTDIR}/PlayfairDisplay-Italic.ttf",
     'boldItalic': f"{FONTDIR}/PlayfairDisplay-BoldItalic.ttf"},
    {'typeface': BODY_FONT,
     'regular': f"{FONTDIR}/EBGaramond-Regular.ttf",
     'bold': f"{FONTDIR}/EBGaramond-Bold.ttf",
     'italic': f"{FONTDIR}/EBGaramond-Italic.ttf",
     'boldItalic': f"{FONTDIR}/EBGaramond-BoldItalic.ttf"},
]
_nf = 0
try:
    _nf = embed_fonts("sortie.pptx", _families)
except Exception as e:
    print("  [polices] embarquement ignore :", e)

# Verification : le fichier se rouvre proprement.
_check = Presentation("sortie.pptx")
_n = len(_check.slides._sldIdLst)
print("OK : sortie.pptx enregistre et rouvert sans erreur.")
print("Nombre de diapositives :", _n)
print("Polices embarquees (parties) :", _nf)
print("Gabarits utilises (ordre) :")
for k, g in enumerate(_used_gabarits, 1):
    print("  {:>2}. {}".format(k, g))
print("Gabarits distincts :", ", ".join(sorted(set(_used_gabarits))))
