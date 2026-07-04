# -*- coding: utf-8 -*-
"""
Generateur de diaporama PowerPoint 16:9, esthetique Regencycore (serie Bridgerton).
Sujet et donnees : projet BC-5 e-business du Musee de la Vie Romantique
(dossier "BC-5 Estelle Casterot", concept Love Stories IRL).

Toutes les formes sont natives et editables (add_textbox, add_shape, add_table).
Aucune image plaquee en diapo entiere. Polices : python-pptx n'embarque pas les
polices ; les familles declarees (Didot pour les titres, Garamond pour le corps)
sont substituees par le lecteur si absentes (Didot -> Bodoni MT -> Georgia,
Garamond -> Georgia -> Cambria).
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

# =========================== CONSTANTES DE STYLE ==============================
# Palette Bridgerton (ivoire, bleus poudres, glycine, dorures) en RGBColor.
IVOIRE        = RGBColor(0xF5, 0xEF, 0xE2)  # fond dominant
PORCELAINE    = RGBColor(0xFB, 0xF8, 0xF1)  # blanc porcelaine
BLEU_POUDRE   = RGBColor(0xA9, 0xC3, 0xD6)  # bleu poudre signature
BLEU_CIEL     = RGBColor(0xC4, 0xD8, 0xE4)  # bleu ciel doux (sections)
BLEU_WEDGWOOD = RGBColor(0x6E, 0x93, 0xAE)  # bleu Wedgwood profond
LILAS         = RGBColor(0xC9, 0xB8, 0xDF)  # lilas glycine clair
WISTERIA      = RGBColor(0x9B, 0x7F, 0xB8)  # wisteria moyen
MAUVE         = RGBColor(0xD8, 0xCC, 0xE4)  # mauve poudre
ROSE_POUDRE   = RGBColor(0xEB, 0xD3, 0xD8)  # rose poudre pale
SAUGE         = RGBColor(0xB7, 0xC4, 0xA8)  # vert sauge
OR_CHAMPAGNE  = RGBColor(0xE4, 0xC9, 0x7E)  # or champagne clair
OR_RICHE      = RGBColor(0xC9, 0xA2, 0x27)  # or riche (filets, cartouches)
OR_BRONZE     = RGBColor(0xA0, 0x7C, 0x1F)  # or bronze ombre
ENCRE         = RGBColor(0x3A, 0x36, 0x30)  # encre de lecture
CIRE_BORDEAUX = RGBColor(0x7A, 0x1F, 0x2B)  # cachet de cire bordeaux

# Palette Featherington (rupture ponctuelle, 1 diapo)
F_CITRUS      = RGBColor(0xF2, 0xC5, 0x17)
F_VERT_POMME  = RGBColor(0x8F, 0xC9, 0x3A)
F_MANDARINE   = RGBColor(0xE8, 0x79, 0x2B)
F_FUCHSIA     = RGBColor(0xD9, 0x4F, 0x8A)

# Deux familles de polices maximum.
TITLE_FONT = "Didot"     # serif Didone a fort contraste
BODY_FONT  = "Garamond"  # corps

# Geometrie, calculee depuis slide_width / slide_height.
SW = prs.slide_width          # EMU
SH = prs.slide_height
MX = int(SW * 0.085)          # marge laterale ~8,5 %
MY = int(SH * 0.085)          # marge haute / basse ~8,5 %
CONTENT_W = SW - 2 * MX
BAND_H     = Inches(1.15)     # bandeau de titre ~15,3 %
FILET_H    = Inches(0.03)     # filet dore fin
TITLE_SIZE = 32               # taille de titre commune aux gabarits de contenu
BODY_TOP   = BAND_H + Inches(0.32)

ROMAINS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

_used_gabarits = []  # journal des gabarits utilises


# =============================== UTILITAIRES ==================================
def _spPr(shape):
    return shape._element.spPr


def _no_shadow(shape):
    shape.shadow.inherit = False


def _solid(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def _no_line(shape):
    shape.line.fill.background()


def set_shape_alpha(shape, pct):
    """Regle l'alpha d'un remplissage plein (python-pptx ne l'expose pas)."""
    solid = _spPr(shape).find(qn('a:solidFill'))
    if solid is None:
        return
    srgb = solid.find(qn('a:srgbClr'))
    if srgb is None:
        return
    a = srgb.makeelement(qn('a:alpha'), {'val': str(int(round(pct * 1000)))})
    srgb.append(a)


def send_to_back(shape, slide):
    sp = shape._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)


def add_background(slide, color=IVOIRE):
    """Fond plein pose en premier puis envoye a l'arriere-plan via _spTree."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    _solid(bg, color)
    _no_line(bg)
    _no_shadow(bg)
    send_to_back(bg, slide)
    return bg


def R(text, size, color=ENCRE, bold=False, italic=False, font=BODY_FONT):
    """Fabrique une specification de run."""
    return (text, size, color, bold, italic, font)


def _apply_run(run, spec):
    text, size, color, bold, italic, font = spec
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color


def add_textbox(slide, left, top, width, height, paras,
                anchor=MSO_ANCHOR.TOP, word_wrap=True):
    """paras : liste de dicts {'runs':[spec], 'align', 'line_spacing',
    'space_after', 'space_before'}."""
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = word_wrap
    tf.vertical_anchor = anchor
    tf.margin_left = Pt(2)
    tf.margin_right = Pt(2)
    tf.margin_top = Pt(1)
    tf.margin_bottom = Pt(1)
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = para.get('align', PP_ALIGN.LEFT)
        if para.get('line_spacing'):
            p.line_spacing = para['line_spacing']
        if para.get('space_after') is not None:
            p.space_after = para['space_after']
        if para.get('space_before') is not None:
            p.space_before = para['space_before']
        for spec in para['runs']:
            _apply_run(p.add_run(), spec)
    return tb


def _track_caps(tb, spc_pt=2.6, caps='small'):
    """Interlettrage genereux et petites capitales (frappe de medaille)."""
    for p in tb.text_frame.paragraphs:
        for r in p.runs:
            rPr = r._r.get_or_add_rPr()
            rPr.set('spc', str(int(spc_pt * 100)))
            if caps:
                rPr.set('cap', caps)


def add_filet(slide, left, top, width, thickness=FILET_H, color=OR_RICHE):
    f = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, thickness)
    _solid(f, color)
    _no_line(f)
    _no_shadow(f)
    return f


def add_double_filet(slide, left, top, width):
    """Trait epais or riche double d'un trait fin or champagne parallele."""
    add_filet(slide, left, top, width, Inches(0.035), OR_RICHE)
    add_filet(slide, left, top + Inches(0.05), width, Inches(0.014), OR_CHAMPAGNE)


def add_frame(slide, color=OR_RICHE, width_pt=1.6, inset=0.05):
    """Filet cartouche double, ton dore unique : rectangle epais sans
    remplissage, double d'un trait fin parallele, marge interieure a 5 %."""
    ix = int(SW * inset)
    iy = int(SH * inset)
    fr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, ix, iy, SW - 2 * ix, SH - 2 * iy)
    fr.fill.background()
    fr.line.color.rgb = color
    fr.line.width = Pt(width_pt)
    _no_shadow(fr)
    d = Inches(0.06)
    fr2 = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, ix + d, iy + d,
                                 SW - 2 * ix - 2 * d, SH - 2 * iy - 2 * d)
    fr2.fill.background()
    fr2.line.color.rgb = color
    fr2.line.width = Pt(0.75)
    _no_shadow(fr2)
    return fr


def add_corner_flourishes(slide, color=OR_RICHE, arm=Inches(0.85), thick=Inches(0.045),
                          inset=0.06):
    """Fleurons d'angle dores en L aux quatre coins."""
    ix = int(SW * inset)
    iy = int(SH * inset)
    corners = [
        (ix, iy, 1, 1),
        (SW - ix, iy, -1, 1),
        (ix, SH - iy, 1, -1),
        (SW - ix, SH - iy, -1, -1),
    ]
    for cx, cy, sx, sy in corners:
        hx = cx if sx > 0 else cx - arm
        add_filet(slide, hx, cy - (thick if sy < 0 else 0), arm, thick, color)
        vy = cy if sy > 0 else cy - arm
        vshape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            cx - (thick if sx < 0 else 0), vy, thick, arm)
        _solid(vshape, color)
        _no_line(vshape)
        _no_shadow(vshape)


def add_wisteria_watermark(slide, anchor='bl', color=WISTERIA, alpha=8):
    """Glycine en cascade verticale depuis un angle, ton sur ton, alpha 6 a 10 %."""
    if anchor == 'bl':
        x0, y0, dirx = int(SW * 0.02), int(SH * 0.30), 1
    else:  # 'tr'
        x0, y0, dirx = int(SW * 0.90), int(SH * 0.04), -1
    sizes = [1.15, 0.95, 0.78, 0.62, 0.48, 0.36, 0.26]
    y = y0
    for k, s in enumerate(sizes):
        d = Inches(s)
        off = Inches(0.28 * dirx * (0.5 if k % 2 else -0.2))
        fl = slide.shapes.add_shape(MSO_SHAPE.OVAL, x0 + off, y, d, d)
        _solid(fl, color)
        _no_line(fl)
        _no_shadow(fl)
        set_shape_alpha(fl, alpha)
        y += int(d * 0.62)


def add_wax_seal(slide, cx, cy, d, color=CIRE_BORDEAUX, monogram="MVR",
                 text_color=None, alpha=None, line_color=OR_RICHE):
    """Cachet de cire rond, forme ronde, en signature."""
    seal = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, d, d)
    _solid(seal, color)
    seal.line.color.rgb = line_color
    seal.line.width = Pt(1.0)
    _no_shadow(seal)
    if alpha is not None:
        set_shape_alpha(seal, alpha)
    tc = text_color if text_color else IVOIRE
    add_textbox(slide, cx, cy, d, d,
                [{'runs': [R(monogram, max(9, int(d / Emu(1) / 914400 * 26)),
                            tc, True, False, TITLE_FONT)],
                  'align': PP_ALIGN.CENTER}],
                anchor=MSO_ANCHOR.MIDDLE)
    return seal


def add_bee(slide, cx, cy, size=Inches(0.34), body=OR_RICHE, wing=OR_RICHE):
    """Abeille doree discrete, ponctuation de transition (une seule)."""
    b = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, size, int(size * 1.25))
    _solid(b, body)
    _no_line(b)
    _no_shadow(b)
    wsz = int(size * 0.7)
    for dx in (-int(size * 0.55), int(size * 0.55)):
        w = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx + int(size * 0.15) + dx,
                                   cy - int(size * 0.05), wsz, int(wsz * 0.8))
        _solid(w, wing)
        _no_line(w)
        _no_shadow(w)
        set_shape_alpha(w, 45)


def add_rosette(slide, cx, cy, d=Inches(0.13), color=OR_RICHE):
    """Petite rosette doree, puce florale (jamais envahissante)."""
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, d, d)
    _solid(dot, color)
    _no_line(dot)
    _no_shadow(dot)


def add_footer(slide, page_no=None, accent=OR_RICHE):
    """Petit cachet dore plus numero de page, identique en bas de page."""
    if page_no is None:
        page_no = len(prs.slides._sldIdLst)  # index de la diapo courante
    d = Inches(0.30)
    cx = SW - MX - d
    cy = SH - int(SH * 0.06) - d
    add_wax_seal(slide, cx, cy, d, color=accent, monogram=str(page_no),
                 text_color=ENCRE, line_color=accent)


def add_title_band(slide, titre, band_color=WISTERIA, title_color=PORCELAINE,
                   accent=OR_RICHE):
    """Bandeau de titre haut, filet dore en bordure haute et basse, titre en
    petites capitales. Position et taille identiques sur tous les gabarits de
    contenu (meme filet, memes marges, meme position de titre)."""
    band = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, BAND_H)
    _solid(band, band_color)
    _no_line(band)
    _no_shadow(band)
    add_filet(slide, 0, 0, SW, Inches(0.025), accent)      # filet borde le haut
    add_filet(slide, 0, BAND_H, SW, FILET_H, accent)       # filet borde le bas
    tb = add_textbox(slide, MX, 0, SW - 2 * MX, BAND_H,
                     [{'runs': [R(titre, TITLE_SIZE, title_color, True, False, TITLE_FONT)]}],
                     anchor=MSO_ANCHOR.MIDDLE)
    _track_caps(tb, spc_pt=2.4)
    return band


def _numeric(cell_text):
    t = cell_text.strip()
    if not any(ch.isdigit() for ch in t):
        return False
    letters = [ch for ch in t if ch.isalpha()]
    # tolere M, k, e (unites) mais pas de vrais mots
    return len(letters) <= 2


def clear_table_style(table):
    """Retire le style et le maillage par defaut (rendu propre, zebrage manuel)."""
    tbl = table._tbl
    tblPr = tbl.find(qn('a:tblPr'))
    if tblPr is None:
        return
    tblPr.set('firstRow', '0')
    tblPr.set('bandRow', '0')
    styleId = tblPr.find(qn('a:tableStyleId'))
    if styleId is None:
        styleId = tblPr.makeelement(qn('a:tableStyleId'), {})
        tblPr.append(styleId)
    styleId.text = '{2D5ABB26-0587-4C30-8999-92F81FD0307C}'  # No Style, No Grid


def _fill_cell(cell, text, size, color, bold, align, fill_color):
    cell.fill.solid()
    cell.fill.fore_color.rgb = fill_color
    cell.margin_left = Inches(0.15)
    cell.margin_right = Inches(0.15)
    cell.margin_top = Inches(0.05)
    cell.margin_bottom = Inches(0.05)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    _apply_run(p.add_run(), R(text, size, color, bold, False, BODY_FONT))


def safe_add_picture(slide, path, left, top, width, height, label="Image"):
    """Gestion propre des images : ajoute la photo si le chemin existe, sinon
    dessine un placeholder encadre. Un chemin vide vaut absence d'image (aucun
    dessin). Aucun crash silencieux."""
    import os
    if not path:
        return None
    if os.path.exists(path):
        return slide.shapes.add_picture(path, left, top, width, height)
    ph = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    ph.fill.background()
    ph.line.color.rgb = OR_RICHE
    ph.line.width = Pt(1.0)
    _no_shadow(ph)
    add_textbox(slide, left, top, width, height,
                [{'runs': [R(label, 11, ENCRE, False, True, BODY_FONT)],
                  'align': PP_ALIGN.CENTER}],
                anchor=MSO_ANCHOR.MIDDLE)
    print("  [placeholder] image absente, cadre de substitution :", path)
    return ph


def _new_slide():
    return prs.slides.add_slide(prs.slide_layouts[6])  # disposition vierge


# ================================ GABARITS ===================================
def slide_couverture(titre, sous_titre, date, auteur="", ouverture=""):
    _used_gabarits.append("couverture")
    s = _new_slide()
    add_background(s, IVOIRE)
    add_wisteria_watermark(s, 'tr')
    add_wisteria_watermark(s, 'bl')
    add_frame(s, OR_RICHE, 1.6, 0.05)

    if ouverture:
        add_textbox(s, MX, int(SH * 0.16), CONTENT_W, Inches(0.5),
                    [{'runs': [R(ouverture, 15, BLEU_WEDGWOOD, False, True, BODY_FONT)],
                      'align': PP_ALIGN.CENTER}],
                    anchor=MSO_ANCHOR.MIDDLE)

    # cartouche ovale dore central
    cw, ch = int(SW * 0.66), int(SH * 0.34)
    cx, cy = (SW - cw) // 2, int(SH * 0.30)
    cart = s.shapes.add_shape(MSO_SHAPE.OVAL, cx, cy, cw, ch)
    cart.fill.background()
    cart.line.color.rgb = OR_RICHE
    cart.line.width = Pt(1.8)
    _no_shadow(cart)

    add_textbox(s, cx, cy + int(ch * 0.16), cw, int(ch * 0.42),
                [{'runs': [R(titre, 46, ENCRE, True, False, TITLE_FONT)],
                  'align': PP_ALIGN.CENTER}],
                anchor=MSO_ANCHOR.MIDDLE)
    add_filet(s, (SW - Inches(2.4)) // 2, cy + int(ch * 0.60), Inches(2.4))
    add_textbox(s, cx, cy + int(ch * 0.64), cw, int(ch * 0.30),
                [{'runs': [R(sous_titre, 19, ENCRE, False, True, BODY_FONT)],
                  'align': PP_ALIGN.CENTER}],
                anchor=MSO_ANCHOR.MIDDLE)

    # date et auteur
    add_textbox(s, MX, int(SH * 0.71), CONTENT_W, Inches(0.4),
                [{'runs': [R(date, 16, BLEU_WEDGWOOD, False, False, BODY_FONT)],
                  'align': PP_ALIGN.CENTER}])
    if auteur:
        tb = add_textbox(s, MX, int(SH * 0.755), CONTENT_W, Inches(0.4),
                         [{'runs': [R(auteur, 13, ENCRE, False, False, BODY_FONT)],
                           'align': PP_ALIGN.CENTER}])
        _track_caps(tb, spc_pt=2.0)

    # monogramme (via safe_add_picture, placeholder si absent) et cachet de cire
    add_wax_seal(s, (SW - Inches(0.7)) // 2, int(SH * 0.83), Inches(0.7),
                 color=OR_RICHE, monogram="VR", text_color=ENCRE)
    return s


def slide_sommaire(titre, sections):
    _used_gabarits.append("sommaire")
    s = _new_slide()
    add_background(s, IVOIRE)
    add_wisteria_watermark(s, 'tr')

    tb = add_textbox(s, MX, int(SH * 0.10), CONTENT_W, Inches(0.9),
                     [{'runs': [R(titre, 34, ENCRE, True, False, TITLE_FONT)],
                       'align': PP_ALIGN.CENTER}])
    _track_caps(tb, spc_pt=3.0)
    add_double_filet(s, MX, int(SH * 0.24), CONTENT_W)

    top = int(SH * 0.32)
    row_h = int((SH * 0.56) / max(1, len(sections)))
    for i, sec in enumerate(sections):
        y = top + i * row_h
        add_rosette(s, MX, y + int(row_h * 0.30), Inches(0.14))
        add_textbox(s, MX + Inches(0.42), y, Inches(1.1), row_h,
                    [{'runs': [R(ROMAINS[i], 26, ENCRE, True, False, TITLE_FONT)]}],
                    anchor=MSO_ANCHOR.MIDDLE)
        add_textbox(s, MX + Inches(1.5), y, CONTENT_W - Inches(1.7), row_h,
                    [{'runs': [R(sec, 20, ENCRE, False, False, BODY_FONT)]}],
                    anchor=MSO_ANCHOR.MIDDLE)
        if i < len(sections) - 1:
            add_filet(s, MX + Inches(0.42), y + row_h - Inches(0.02),
                      CONTENT_W - Inches(0.42), Inches(0.008), OR_CHAMPAGNE)
    add_footer(s)
    return s


def slide_section(numero, titre, code="", aparte="", bee=False):
    _used_gabarits.append("section")
    s = _new_slide()
    add_background(s, BLEU_CIEL)  # fond bleu moire
    add_wisteria_watermark(s, 'tr')
    add_corner_flourishes(s)

    # grand numero dore, point focal
    add_textbox(s, MX, int(SH * 0.16), CONTENT_W, Inches(2.1),
                [{'runs': [R(numero, 118, OR_RICHE, True, False, TITLE_FONT)],
                  'align': PP_ALIGN.CENTER}],
                anchor=MSO_ANCHOR.MIDDLE)
    if code:
        tb = add_textbox(s, MX, int(SH * 0.50), CONTENT_W, Inches(0.4),
                         [{'runs': [R(code, 15, BLEU_WEDGWOOD, True, False, BODY_FONT)],
                           'align': PP_ALIGN.CENTER}])
        _track_caps(tb, spc_pt=3.0)
    tb = add_textbox(s, MX, int(SH * 0.55), CONTENT_W, Inches(1.0),
                     [{'runs': [R(titre, 34, ENCRE, True, False, TITLE_FONT)],
                       'align': PP_ALIGN.CENTER}],
                     anchor=MSO_ANCHOR.MIDDLE)
    _track_caps(tb, spc_pt=2.0)
    add_filet(s, (SW - Inches(2.6)) // 2, int(SH * 0.70), Inches(2.6))
    if aparte:
        add_textbox(s, int(SW * 0.16), int(SH * 0.74), int(SW * 0.68), Inches(0.8),
                    [{'runs': [R(aparte, 16, ENCRE, False, True, BODY_FONT)],
                      'align': PP_ALIGN.CENTER, 'line_spacing': 1.3}],
                    anchor=MSO_ANCHOR.MIDDLE)
    if bee:
        add_bee(s, int(SW * 0.5) - Inches(0.17), int(SH * 0.135))
    add_footer(s)
    return s


def slide_contenu(titre, elements, source=""):
    _used_gabarits.append("contenu")
    s = _new_slide()
    add_background(s, IVOIRE)
    add_wisteria_watermark(s, 'bl')
    add_title_band(s, titre)

    top = BODY_TOP + Inches(0.15)
    usable_h = SH - top - int(SH * 0.12)
    row_h = int(usable_h / max(1, len(elements)))
    for i, el in enumerate(elements):
        y = top + i * row_h
        add_rosette(s, MX, y + int(row_h * 0.33), Inches(0.14))
        add_textbox(s, MX + Inches(0.45), y, CONTENT_W - Inches(0.45), row_h,
                    [{'runs': [R(el, 18, ENCRE, False, False, BODY_FONT)],
                      'line_spacing': 1.35}],
                    anchor=MSO_ANCHOR.MIDDLE)
    if source:
        add_textbox(s, MX, SH - int(SH * 0.11), CONTENT_W, Inches(0.35),
                    [{'runs': [R(source, 10, ENCRE, False, True, BODY_FONT)]}])
    add_footer(s, None)
    return s


def slide_tableau(titre, entetes, lignes, right_cols=None, col_ratios=None, source=""):
    _used_gabarits.append("tableau")
    s = _new_slide()
    add_background(s, IVOIRE)
    add_wisteria_watermark(s, 'bl')
    add_title_band(s, titre)
    right_cols = right_cols or []

    n_rows = len(lignes) + 1
    n_cols = len(entetes)
    top = BODY_TOP + Inches(0.05)
    tbl_h = SH - top - int(SH * 0.14)
    gf = s.shapes.add_table(n_rows, n_cols, MX, top, CONTENT_W, tbl_h)
    table = gf.table
    clear_table_style(table)

    if col_ratios:
        tot = float(sum(col_ratios))
        for j, r in enumerate(col_ratios):
            table.columns[j].width = int(CONTENT_W * r / tot)
    else:
        for j in range(n_cols):
            table.columns[j].width = int(CONTENT_W / n_cols)

    header_h = Inches(0.6)
    body_h = int((tbl_h - header_h) / max(1, len(lignes)))
    table.rows[0].height = header_h
    for i in range(1, n_rows):
        table.rows[i].height = body_h

    # en-tete : wisteria, texte porcelaine gras
    for j, head in enumerate(entetes):
        align = PP_ALIGN.RIGHT if j in right_cols else PP_ALIGN.LEFT
        _fill_cell(table.cell(0, j), head, 12.5, PORCELAINE, True, align, WISTERIA)

    # corps : zebrage ivoire / porcelaine, nombres a droite
    for i, row in enumerate(lignes):
        zebra = IVOIRE if i % 2 == 0 else PORCELAINE
        for j, val in enumerate(row):
            txt = str(val)
            right = (j in right_cols) or _numeric(txt)
            align = PP_ALIGN.RIGHT if right else PP_ALIGN.LEFT
            bold = (j == 0)
            _fill_cell(table.cell(i + 1, j), txt, 11.5, ENCRE, bold, align, zebra)

    # filet dore sous l'en-tete et cadre general
    add_filet(s, MX, top + header_h - Inches(0.02), CONTENT_W, Inches(0.02), OR_RICHE)
    frame = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, MX, top, CONTENT_W, tbl_h)
    frame.fill.background()
    frame.line.color.rgb = OR_RICHE
    frame.line.width = Pt(1.0)
    _no_shadow(frame)

    if source:
        add_textbox(s, MX, SH - int(SH * 0.11), CONTENT_W, Inches(0.35),
                    [{'runs': [R(source, 10, ENCRE, False, True, BODY_FONT)]}])
    add_footer(s, None)
    return s


def slide_kpi(titre, cartes, source="", theme="or"):
    _used_gabarits.append("kpi")
    s = _new_slide()
    if theme == "feather":
        bg, band, accent, card = F_CITRUS, F_FUCHSIA, F_MANDARINE, PORCELAINE
    else:
        bg, band, accent, card = IVOIRE, WISTERIA, OR_RICHE, PORCELAINE
    add_background(s, bg)
    if theme != "feather":
        add_wisteria_watermark(s, 'bl')
    add_title_band(s, titre, band_color=band, title_color=PORCELAINE, accent=accent)

    n = len(cartes)
    gutter = Inches(0.35)
    usable = CONTENT_W
    card_w = int((usable - (n - 1) * gutter) / n)
    card_h = Inches(2.75)
    top = BODY_TOP + Inches(0.55)
    for i, c in enumerate(cartes):
        x = MX + i * (card_w + gutter)
        rect = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, top, card_w, card_h)
        _solid(rect, card)
        rect.line.color.rgb = accent
        rect.line.width = Pt(1.25)
        _no_shadow(rect)
        add_textbox(s, x, top + Inches(0.35), card_w, Inches(1.2),
                    [{'runs': [R(c['value'], 48, accent, True, False, TITLE_FONT)],
                      'align': PP_ALIGN.CENTER}],
                    anchor=MSO_ANCHOR.MIDDLE)
        add_filet(s, x + int(card_w * 0.33), top + Inches(1.55),
                  int(card_w * 0.34), Inches(0.02), accent)
        add_textbox(s, x + Inches(0.15), top + Inches(1.70), card_w - Inches(0.3), Inches(0.9),
                    [{'runs': [R(c['label'], 13, ENCRE, False, False, BODY_FONT)],
                      'align': PP_ALIGN.CENTER, 'line_spacing': 1.2}],
                    anchor=MSO_ANCHOR.MIDDLE)
    if source:
        add_textbox(s, MX, SH - int(SH * 0.11), CONTENT_W, Inches(0.35),
                    [{'runs': [R(source, 10, ENCRE, False, True, BODY_FONT)],
                      'align': PP_ALIGN.CENTER}])
    add_footer(s, None, accent=accent)
    return s


def slide_citation(texte, auteur, source=""):
    _used_gabarits.append("citation")
    s = _new_slide()
    add_background(s, IVOIRE)
    add_wisteria_watermark(s, 'tr')

    # grand guillemet dore
    add_textbox(s, int(SW * 0.10), int(SH * 0.14), Inches(2.0), Inches(2.0),
                [{'runs': [R("“", 150, OR_RICHE, True, False, TITLE_FONT)]}],
                anchor=MSO_ANCHOR.TOP)
    add_textbox(s, int(SW * 0.16), int(SH * 0.34), int(SW * 0.68), Inches(1.8),
                [{'runs': [R(texte, 27, ENCRE, False, True, TITLE_FONT)],
                  'align': PP_ALIGN.CENTER, 'line_spacing': 1.3}],
                anchor=MSO_ANCHOR.MIDDLE)
    add_filet(s, (SW - Inches(2.2)) // 2, int(SH * 0.62), Inches(2.2))
    tb = add_textbox(s, MX, int(SH * 0.65), CONTENT_W, Inches(0.5),
                     [{'runs': [R(auteur, 15, ENCRE, True, False, BODY_FONT)],
                       'align': PP_ALIGN.CENTER}])
    _track_caps(tb, spc_pt=2.6)
    add_wax_seal(s, (SW - Inches(0.8)) // 2, int(SH * 0.73), Inches(0.8),
                 color=CIRE_BORDEAUX, monogram="LW")
    if source:
        add_textbox(s, MX, SH - int(SH * 0.10), CONTENT_W, Inches(0.3),
                    [{'runs': [R(source, 10, ENCRE, False, True, BODY_FONT)],
                      'align': PP_ALIGN.CENTER}])
    return s


def slide_cloture(message, contact, signature="Bien à vous, Lady Whistledown"):
    _used_gabarits.append("cloture")
    s = _new_slide()
    add_background(s, IVOIRE)  # rappel visuel de la couverture
    add_wisteria_watermark(s, 'tr')
    add_wisteria_watermark(s, 'bl')
    add_frame(s, OR_RICHE, 1.6, 0.05)

    add_textbox(s, int(SW * 0.14), int(SH * 0.22), int(SW * 0.72), Inches(1.6),
                [{'runs': [R(message, 34, ENCRE, True, False, TITLE_FONT)],
                  'align': PP_ALIGN.CENTER, 'line_spacing': 1.15}],
                anchor=MSO_ANCHOR.MIDDLE)
    add_filet(s, (SW - Inches(2.6)) // 2, int(SH * 0.44), Inches(2.6))
    add_textbox(s, MX, int(SH * 0.47), CONTENT_W, Inches(0.5),
                [{'runs': [R(contact, 16, ENCRE, False, False, BODY_FONT)],
                  'align': PP_ALIGN.CENTER}])

    # cachet de cire en zoom fondu
    add_wax_seal(s, (SW - Inches(1.5)) // 2, int(SH * 0.56), Inches(1.5),
                 color=CIRE_BORDEAUX, monogram="LW", alpha=88)
    tb = add_textbox(s, MX, int(SH * 0.80), CONTENT_W, Inches(0.5),
                     [{'runs': [R(signature, 17, ENCRE, False, True, TITLE_FONT)],
                       'align': PP_ALIGN.CENTER}])
    return s


# ============================ CONSTRUCTION DU DECK ============================
# Donnees issues exclusivement du dossier BC-5 (Musee de la Vie Romantique).

slide_couverture(
    "Love Stories IRL",
    "Musée de la Vie Romantique · Projet BC-5 e-business",
    "Année 2025-2026",
    auteur="Estelle Casterot",
    ouverture="Cher Aimable Lecteur, voici un musée adoré du Tout-Paris, et ignoré du numérique.",
)

slide_sommaire("Sommaire", [
    "C5.1 · Benchmark sectoriel",
    "C5.2 · Tableau de bord des données",
    "C5.4 · Plan marketing opérationnel",
    "C5.6 · Leviers digitaux",
    "C5.8 · Campagne e-mailing",
])

# --- Section I : C5.1 Benchmark sectoriel ---
slide_section("I", "Benchmark sectoriel", code="C5.1",
              aparte="Cher Aimable Lecteur, le retard se mesure, et il se rattrape.",
              bee=True)

slide_kpi("Repères de marché", [
    {'value': "8,7 M", 'label': "visiteurs/an · Louvre"},
    {'value': "3,7 M", 'label': "visiteurs/an · Orsay"},
    {'value': "1,4 M", 'label': "visiteurs/an · Ateliers Lumières"},
    {'value': "+25 %", 'label': "visites -30 ans avec le numérique"},
], source="Source : repères de marché, sources de veille (BC-5, C5.1).")

slide_tableau(
    "Scorecard pondérée",
    ["Critère (poids)", "Vie Rom.", "G. Moreau", "Orsay", "At. Lumières", "Louvre"],
    [
        ["Offre digitale (20 %)", "2 / 5", "2 / 5", "4 / 5", "4 / 5", "5 / 5"],
        ["Présence sociale (20 %)", "2 / 5", "2 / 5", "3 / 5", "5 / 5", "5 / 5"],
        ["UX mobile / site (15 %)", "2 / 5", "2 / 5", "4 / 5", "4 / 5", "3 / 5"],
        ["Médiation / immersion (15 %)", "3 / 5", "3 / 5", "4 / 5", "5 / 5", "4 / 5"],
        ["Notoriété / fréquentation (15 %)", "2 / 5", "2 / 5", "4 / 5", "4 / 5", "5 / 5"],
        ["Différenciation identitaire (15 %)", "5 / 5", "4 / 5", "3 / 5", "3 / 5", "3 / 5"],
        ["Score pondéré global", "2,6 / 5", "2,5 / 5", "3,7 / 5", "4,2 / 5", "4,3 / 5"],
    ],
    right_cols=[1, 2, 3, 4, 5],
    col_ratios=[2.55, 1.0, 1.05, 0.9, 1.15, 0.95],
    source="Notation 1 à 5, analyse octobre 2025 (BC-5, C5.1).",
)

# --- Section II : C5.2 Tableau de bord des donnees ---
slide_section("II", "Tableau de bord des données", code="C5.2",
              aparte="Des cibles, pas des résultats. Le dispositif ouvre en février 2026.")

slide_kpi("Cibles du dispositif", [
    {'value': "≈ 2 %", 'label': "engagement Instagram (cible compte)"},
    {'value': "1 500", 'label': "scans QR par trimestre"},
    {'value': "60 %", 'label': "écoute complète des capsules"},
    {'value': "300", 'label': "posts #AdopteTonRomantique / 6 mois"},
], source="Projection, dispositif non déployé (BC-5, C5.2).")

slide_tableau(
    "Indicateurs économiques",
    ["Indicateur", "Calcul", "Repère"],
    [
        ["Coût par scan QR", "4 000 € / 1 500 scans visés", "≈ 2,7 € par scan"],
        ["Coût par lead (quiz)", "1 200 € / 2 000 leads visés", "≈ 0,6 € par lead"],
        ["Seuil de rentabilité indirect", "21 500 € / panier indirect ≈ 6 € par visiteur",
         "≈ 3 600 visites"],
    ],
    right_cols=[2],
    col_ratios=[1.15, 1.75, 1.0],
    source="Repères économiques de pilotage (BC-5, C5.2).",
)

# --- Section III : C5.4 Plan marketing operationnel ---
slide_section("III", "Plan marketing opérationnel", code="C5.4",
              aparte="Cher Aimable Lecteur, 21 500 euros, et nul tapage inutile.")

slide_kpi("Budget : 21 500 €", [
    {'value': "5 500 €", 'label': "Création de contenus"},
    {'value': "4 000 €", 'label': "Signalétique et QR"},
    {'value': "2 000 €", 'label': "Publicité de lancement"},
    {'value': "2 000 €", 'label': "Influence et partenariats"},
], source="4 postes sur 9, enveloppe totale 21 500 € (BC-5, C5.4).", theme="feather")

slide_tableau(
    "Plan d'actions opérationnel",
    ["Étape", "Action", "Objectif / KPI", "Budget"],
    [
        ["Sensibiliser", "Sondages et teasing", "Portée +50 %", "500 €"],
        ["Découvrir", "Quiz love story et page", "2 000 leads", "1 200 €"],
        ["Donner envie", "Reels et écoles d'art", "50 k vues", "2 000 €"],
        ["Vivre la visite", "QR codes et capsules audio", "1 500 scans", "4 000 €"],
        ["Amplifier", "UGC #AdopteTonRomantique", "300 posts", "2 000 €"],
    ],
    right_cols=[3],
    col_ratios=[1.05, 1.75, 1.15, 0.7],
    source="Plan d'actions sur 12 mois (BC-5, C5.4).",
)

# --- Section IV : C5.6 Leviers digitaux ---
slide_section("IV", "Leviers digitaux", code="C5.6",
              aparte="Le gratuit d'abord. Le payant, réservé aux beaux jours.")

slide_tableau(
    "Leviers prioritaires",
    ["Famille", "Levier", "Priorité"],
    [
        ["Utilisateurs", "Micro-influence culture / Paris", "Haute"],
        ["Utilisateurs", "Avis Google / TripAdvisor", "Haute"],
        ["Utilisateurs", "UGC #AdopteTonRomantique", "Haute"],
        ["Marque", "SEO (refonte)", "Haute"],
        ["Marque", "SMO", "Haute"],
        ["Payants", "SEA (Google Ads)", "Moyenne"],
        ["Payants", "Display / retargeting", "Basse"],
    ],
    col_ratios=[1.0, 2.1, 0.9],
    source="Analyse des leviers digitaux (BC-5, C5.6).",
)

slide_contenu("Arbitrage organique / payant", [
    "Payant : environ 4 000 €, moins d'un cinquième du budget.",
    "Organique : 70 à 80 % de l'effort (SEO, SMO, UGC, micro-influence).",
    "Payant réservé aux temps forts (Saint-Valentin, lancement).",
], source="Arbitrage dérivé du budget 21 500 € (BC-5, C5.6).")

# --- Section V : C5.8 Campagne e-mailing ---
slide_section("V", "Campagne e-mailing", code="C5.8",
              aparte="Le seul canal que le musée possède vraiment.")

slide_tableau(
    "Objectifs de délivrabilité",
    ["Indicateur", "Cible", "Source"],
    [
        ["Taux d'ouverture", "≥ 40 %", "Brevo 2025"],
        ["Réactivité (CTOR)", "≥ 12 %", "Brevo 2025"],
        ["Taux de clic (CTR)", "≥ 4 %", "Brevo 2025"],
        ["Taux de désabonnement", "< 0,5 %", "bonne pratique"],
        ["Contacts opt-in / RGPD", "100 %", "double opt-in, UE"],
    ],
    right_cols=[1],
    col_ratios=[1.5, 0.8, 1.1],
    source="Objectifs et délivrabilité, cibles sourcées (BC-5, C5.8).",
)

slide_citation(
    "Un musée qui murmure peut se faire entendre, s'il choisit bien ses mots.",
    "Lady Whistledown",
    source="Fil rouge narratif du dossier.",
)

slide_cloture(
    "Love Stories IRL",
    "Réouverture février 2026 · @museevieromantique · #AdopteTonRomantique",
)

# =============================== ENREGISTREMENT ===============================
prs.save("sortie.pptx")

# Verification : le fichier se rouvre proprement.
_check = Presentation("sortie.pptx")
_n = len(_check.slides._sldIdLst)
print("OK : sortie.pptx enregistre et rouvert sans erreur.")
print("Nombre de diapositives :", _n)
print("Gabarits utilises (ordre) :")
for k, g in enumerate(_used_gabarits, 1):
    print("  {:>2}. {}".format(k, g))
print("Gabarits distincts :", ", ".join(sorted(set(_used_gabarits))))
