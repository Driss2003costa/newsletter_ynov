# -*- coding: utf-8 -*-
"""
Dossier BC3 (Retour d'expérience) d'Estelle CASTEROT, structuré selon le
cahier des charges EEMI. Zones surlignées en jaune = à compléter/vérifier.
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

JUST = WD_ALIGN_PARAGRAPH.JUSTIFY
CENTER = WD_ALIGN_PARAGRAPH.CENTER
doc = Document()

# ---------------- styles (exigences EEMI : Calibri 12, interligne simple, 6pt avant / 0 après)
st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(12)
st.paragraph_format.space_before = Pt(6); st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing = 1.0
for lvl, sz in [('Heading 1', 18), ('Heading 2', 15), ('Heading 3', 13)]:
    s = doc.styles[lvl]
    s.font.name = 'Calibri'; s.font.size = Pt(sz)
    s.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

illustrations = []

# ---------------- helpers
def seg(paragraph, segments):
    for s in segments:
        text, kind = (s if isinstance(s, tuple) else (s, 'n'))
        r = paragraph.add_run(text)
        if kind == 'ph':
            r.font.highlight_color = WD_COLOR_INDEX.YELLOW; r.italic = True
        elif kind == 'b':
            r.bold = True

def para(*s):
    p = doc.add_paragraph(); p.alignment = JUST; seg(p, s); return p
def bullet(*s):
    p = doc.add_paragraph(style='List Bullet'); seg(p, s); return p
def h1(t): doc.add_heading(t, 1)
def h2(t): doc.add_heading(t, 2)
def h3(t): doc.add_heading(t, 3)
def gap(n=1):
    for _ in range(n): doc.add_paragraph()
def pb(): doc.add_page_break()
def placeholder(t):
    p = doc.add_paragraph(); r = p.add_run('[À compléter : ' + t + ']')
    r.font.highlight_color = WD_COLOR_INDEX.YELLOW; r.italic = True; return p
def figure_placeholder(cap):
    illustrations.append(cap)
    p = doc.add_paragraph(); p.alignment = CENTER
    r = p.add_run('[ ' + cap + ' — visuel à insérer ]')
    r.font.highlight_color = WD_COLOR_INDEX.YELLOW; r.italic = True
    c = doc.add_paragraph(); c.alignment = CENTER
    cr = c.add_run(cap); cr.italic = True; cr.font.size = Pt(9)
def add_table(cap, headers, rows):
    illustrations.append(cap)
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]; cell.text = ''
        r = cell.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(10)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ''; p = cells[i].paragraphs[0]
            text, kind = (v if isinstance(v, tuple) else (v, 'n'))
            r = p.add_run(text); r.font.size = Pt(10)
            if kind == 'ph':
                r.font.highlight_color = WD_COLOR_INDEX.YELLOW; r.italic = True
    c = doc.add_paragraph(); c.alignment = CENTER
    cr = c.add_run(cap); cr.italic = True; cr.font.size = Pt(9)
    doc.add_paragraph()

# ---------------- mise en page EEMI (marges + en-tête + pied de page hors page de garde)
sec = doc.sections[0]
sec.left_margin = Cm(2.5); sec.right_margin = Cm(2.5)
sec.top_margin = Cm(2.0); sec.bottom_margin = Cm(2.0)
sec.different_first_page_header_footer = True

hp = sec.header.paragraphs[0]; hp.alignment = CENTER
r = hp.add_run('[ Logo entreprise ]        Estelle Casterot        [ Logo EEMI ]')
r.font.size = Pt(9); r.font.highlight_color = WD_COLOR_INDEX.YELLOW

fp = sec.footer.paragraphs[0]
tabs = fp.paragraph_format.tab_stops
tabs.add_tab_stop(Cm(8), WD_TAB_ALIGNMENT.CENTER)
tabs.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT)
fp.add_run('Année 2025 / 2026\tEstelle Casterot\t')
pr = fp.add_run();
for tag, t in [('begin', None), ('instrText', 'PAGE'), ('end', None)]:
    e = OxmlElement('w:fldChar') if tag != 'instrText' else OxmlElement('w:instrText')
    if tag == 'instrText': e.set(qn('xml:space'), 'preserve'); e.text = t
    else: e.set(qn('w:fldCharType'), tag)
    pr._r.append(e)

# ================= PAGE DE GARDE
def C(text, size, bold=False, italic=False, hl=False):
    p = doc.add_paragraph(); p.alignment = CENTER
    r = p.add_run(text); r.font.size = Pt(size); r.bold = bold; r.italic = italic
    if hl: r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    return p

C('[ Logo J\'ai vu la Vierge ]          [ Logo EEMI ]', 12, hl=True)
gap(2)
C("Dossier de Retour d'Expérience sur activités professionnelles", 24, bold=True)
C("Épreuve certifiante du Bloc de Compétences 3 (BC3)", 13)
C("Titre Chef de projets digitaux", 12, italic=True)
gap(2)
C("Estelle CASTEROT", 18, bold=True)
gap(1)
C("Bachelor 3 Communication, Marketing et Événementiel", 12)
C("Promotion 2025 / 2026", 12)
gap(2)
for lab, val in [("Entreprise d'accueil", "J'ai vu la Vierge"),
                 ("Poste occupé", "Alternante Cheffe de Projet e-commerce"),
                 ("Créatrice de la marque", "Alexandra Cefai"),
                 ("Tutrice en entreprise", "Camille Abela, Responsable de Projet e-commerce")]:
    p = doc.add_paragraph(); p.alignment = CENTER
    a = p.add_run(lab + " : "); a.bold = True; a.font.size = Pt(12)
    b = p.add_run(val); b.font.size = Pt(12)
C("Campus [Ynov Aix-en-Provence / EEMI, à confirmer selon l'établissement]", 11, italic=True, hl=True)
pb()

# ================= SOMMAIRE
h1('Sommaire')
para("Pour générer la pagination, sélectionnez tout le document puis appuyez sur F9, "
     "ou faites un clic droit sur le sommaire et choisissez « Mettre à jour les champs ».")
p = doc.add_paragraph(); run = p.add_run()
f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
ins = OxmlElement('w:instrText'); ins.set(qn('xml:space'), 'preserve'); ins.text = 'TOC \\o "1-3" \\h \\z \\u'
f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'separate')
tt = OxmlElement('w:t'); tt.text = "Le sommaire s'affichera ici après mise à jour (F9)."
f3 = OxmlElement('w:fldChar'); f3.set(qn('w:fldCharType'), 'end')
for e in (f1, ins, f2, tt, f3): run._r.append(e)
pb()

# ================= FICHE DE CONFIDENTIALITÉ
h1('Fiche de confidentialité')
para("Retour d'expérience en entreprise", ("", 'n'))
h3("Étudiante ou alternante")
for lab, val in [("Nom", "CASTEROT"), ("Prénom", "Estelle"),
                 ("Classe", "Bachelor 3 Communication, Marketing et Événementiel"),
                 ("Entreprise", "J'ai vu la Vierge")]:
    p = doc.add_paragraph(); a = p.add_run(lab + " : "); a.bold = True; p.add_run(val)
h3("Tutrice ou maître d'apprentissage")
for lab, val in [("Nom", "ABELA"), ("Prénom", "Camille"),
                 ("Fonction", "Responsable de Projet e-commerce")]:
    p = doc.add_paragraph(); a = p.add_run(lab + " : "); a.bold = True; p.add_run(val)
h3("Exigences au regard du présent dossier")
for txt in [
    "l'entreprise autorise son accès à l'équipe pédagogique, aux évaluateurs et aux apprenants, sans restriction de temps ;",
    "l'entreprise autorise son accès à l'équipe pédagogique et aux évaluateurs, sans restriction de temps ;",
    "l'entreprise limite son accès à l'équipe pédagogique et aux évaluateurs, jusqu'à la tenue du jury de diplomation."]:
    p = doc.add_paragraph(); p.add_run("☐  " + txt)
gap(1)
para("Signature et cachet de l'entreprise :")
pb()

# ================= REMERCIEMENTS
h1('Remerciements')
para("Avant d'entrer dans le vif de ce retour d'expérience, je souhaite adresser mes remerciements à "
     "toutes les personnes qui ont rendu cette alternance aussi riche.")
para("Je remercie tout particulièrement Camille Abela, ma tutrice et Responsable de Projet e-commerce, "
     "pour sa confiance, sa disponibilité et l'accompagnement qu'elle m'a offert tout au long de l'année. "
     "Ses briefs, ses retours et nos points hebdomadaires m'ont permis de progresser semaine après semaine "
     "et de gagner en autonomie sur un métier que je découvrais.")
para("Je remercie également Alexandra Cefai, créatrice de la marque J'ai vu la Vierge, ainsi que "
     "l'ensemble de l'équipe, qui m'ont accueillie avec bienveillance et m'ont fait confiance sur des sujets "
     "à forte visibilité.")
para("Mes remerciements vont enfin à l'équipe pédagogique et à mon référent de formation, qui m'ont donné "
     "les repères méthodologiques nécessaires pour mener à bien mes missions et pour prendre le recul attendu "
     "dans ce dossier.")
pb()

# ================= INTRODUCTION
h1('Introduction')
para("J'ai réalisé mon alternance de troisième année de Bachelor Communication, Marketing et Événementiel "
     "au sein de la marque J'ai vu la Vierge, selon un rythme de deux semaines en entreprise pour une semaine "
     "à l'école. J'y ai occupé le poste de Cheffe de Projet e-commerce, au sein du pôle digital, sous la "
     "responsabilité de ma tutrice Camille Abela, Responsable de Projet e-commerce. Mes missions couvraient "
     "l'animation des réseaux sociaux, la production de contenus, la rédaction des fiches produits, l'emailing "
     "et le reporting des performances.")
para("J'ai choisi cette alternance parce qu'elle correspondait précisément à mon projet professionnel. Je "
     "souhaitais apprendre à piloter des projets digitaux de bout en bout et découvrir le e-commerce, un "
     "univers que je connaissais peu et qui me semblait porteur. Rejoindre une marque à l'identité aussi "
     "singulière que J'ai vu la Vierge représentait un défi stimulant, à la croisée de la communication, du "
     "marketing et de l'événementiel, les trois dimensions de ma formation. Cette expérience s'inscrit "
     "pleinement dans mon ambition de poursuivre en mastère puis de devenir cheffe de projet.")
para("La marque J'ai vu la Vierge réinvente la statuette de la Vierge Marie en objet de décoration "
     "contemporain, à la rencontre de l'iconographie religieuse, de l'artisanat et de la culture pop. Ce "
     "positionnement fait à la fois sa force et sa principale difficulté de communication, car il faut réussir "
     "à proposer un objet à forte charge symbolique à un public large sans jamais trahir son identité. De ce "
     "constat est née la problématique qui guide ce dossier.")
p = doc.add_paragraph(); p.alignment = CENTER
r = p.add_run("Comment développer la visibilité et les performances e-commerce de J'ai vu la Vierge grâce à "
              "une stratégie de communication digitale cohérente, tout en préservant une image de marque "
              "singulière et sensible ?"); r.bold = True; r.italic = True
para("Pour y répondre, je présente d'abord l'entreprise, son organisation et son environnement technique. "
     "J'expose ensuite mon poste et mes missions, avant de consacrer un focus détaillé au projet central de "
     "mon alternance, la stratégie de communication digitale de la marque. Je termine par une synthèse et un "
     "bilan des compétences et des enseignements que cette expérience m'a apportés.")
pb()

# ================= 1. L'ENTREPRISE
h1("1. L'entreprise")

h2('1.1 La structure')
para("J'ai vu la Vierge est une marque de décoration qui revisite une figure très ancienne, la statuette de "
     "la Vierge Marie, pour en faire un objet contemporain, coloré et désirable. Là où l'objet religieux "
     "classique reste discret et traditionnel, la marque en fait une pièce de décoration assumée, à la fois "
     "spirituelle et pop, que l'on affiche chez soi comme un objet de style autant que de sens. Son ambition "
     "est de bousculer les codes de la décoration dévote.")
para("La société a été créée en 2018 par Alexandra Cefai, journaliste pendant vingt ans à La Provence, et "
     "son conjoint Damien Grauvogel, artiste et designer produit. Le couple tenait auparavant une galerie "
     "d'art au pied de Notre-Dame de la Garde, à Marseille. L'idée est née un lendemain de Fashion Week, en "
     "imaginant la Bonne Mère vêtue d'une robe rouge ou rose fluo, avec cette question amusée : pourquoi "
     "n'aurait-elle pas le droit de s'habiller comme elle le veut ? Le pari était lancé.")
para("L'aventure a d'abord été familiale. Alexandra s'occupait de la partie commerciale et démarchait les "
     "revendeurs de Marseille et des villages touristiques alentour, Damien assurait le design et la "
     "production, et la mère de Damien tenait le poste d'agent de conditionnement. Le concept marseillais a "
     "connu un succès rapide, notamment grâce à la participation au salon Maison et Objet, qui a ouvert la "
     "marque à l'international. Aujourd'hui, l'entreprise est installée dans le quartier de La Pomme, à "
     "Marseille.")
para("Sur le plan juridique, J'ai vu la Vierge est une PME au statut de SAS. Quelques chiffres clés "
     "résument son développement.")
bullet(("Création : ", 'b'), "2018, à Marseille.")
bullet(("Effectif : ", 'b'), "de 3 salariés à ses débuts à 9 aujourd'hui.")
bullet(("Distribution : ", 'b'), "plus de 400 revendeurs en France et des revendeurs à l'international, "
        "notamment à Tokyo, New York et Séoul.")
bullet(("Bascule vers le digital : ", 'b'), "pendant le confinement (de mars 2020 à mai 2021), les ventes "
        "du site e-commerce sont passées de 2 715,85 euros à 34 105,74 euros de chiffre d'affaires net d'une "
        "année sur l'autre, ce qui a confirmé l'importance stratégique du canal en ligne.")
para("La marque s'adresse à une clientèle majoritairement féminine, avec un cœur de cible situé entre trente "
     "et soixante ans, sensible à la décoration, à l'objet qui a du sens et au cadeau original. Pour orienter "
     "mes contenus, je me suis appuyée sur un persona type : une femme active et urbaine, attirée par les "
     "objets qui racontent une histoire, présente sur Instagram et attachée à l'authenticité d'une marque.")
placeholder("précisez si vous le souhaitez le panier moyen et la fourchette de prix des produits")
para("La distribution repose sur plusieurs canaux complémentaires : le site e-commerce propulsé par Shopify, "
     "une plateforme dédiée aux revendeurs sous Odoo, et un réseau de partenaires physiques prestigieux comme "
     "Le Printemps, le Mucem, Maison et Objet, Boboboom ou l'Olympique de Marseille, sans oublier des "
     "collaborations médiatiques telles que celle menée avec Karine Le Marchand.")
para("Sur son marché, la marque évolue face à des concurrents qui exploitent le même imaginaire, notamment "
     "Sapristi et Miraculeuse. Ce qui la distingue tient à deux atouts majeurs : une présence sur les réseaux "
     "sociaux nettement plus dynamique et un réseau de très bons commerçants et partenaires qui l'installent "
     "dans des lieux reconnus.")
para("Pour situer ce contexte, j'ai synthétisé l'environnement externe de la marque dans une grille PESTEL, "
     "puis l'ensemble de l'analyse dans une matrice SWOT.")
add_table("Tableau 1 : Analyse PESTEL de l'environnement de J'ai vu la Vierge",
    ["Facteur", "Ce que cela implique pour la marque"],
    [["Politique et réglementaire", "Contexte de laïcité et sensibilité autour des symboles religieux, qui "
      "peut freiner certains partenariats, comme je l'ai vécu avec l'Olympique de Marseille."],
     ["Économique", "Bonne dynamique du e-commerce et de la décoration, mais forte saisonnalité liée aux "
      "fêtes et aux temps forts commerciaux."],
     ["Socioculturel", "Goût marqué pour l'objet détourné, spirituel et pop, largement diffusé par les "
      "réseaux sociaux."],
     ["Technologique", "Poids des algorithmes, essor de la vidéo courte et montée de l'intelligence "
      "artificielle appliquée au ciblage, comme la solution Kiliba."],
     ["Écologique", "Attentes croissantes sur l'origine des produits et une fabrication responsable."],
     ["Légal", "Cadre du RGPD pour l'emailing, droit à l'image pour les shootings et obligations du "
      "e-commerce."]])
add_table("Tableau 2 : Matrice SWOT de J'ai vu la Vierge",
    ["Forces", "Faiblesses"],
    [["Identité forte et différenciante ; présence sociale dynamique ; réseau de partenaires prestigieux ; "
      "produit à fort pouvoir d'évocation.",
      "Dépendance à la portée organique ; image sensible ; notoriété encore de niche ; base clients à mieux "
      "exploiter."]])
add_table("Tableau 3 : SWOT, opportunités et menaces",
    ["Opportunités", "Menaces"],
    [["Essor de la vidéo courte ; engouement pour l'objet déco détourné ; collaborations médiatiques ; "
      "fidélisation par l'emailing.",
      "Concurrence de Sapristi et Miraculeuse ; volatilité des algorithmes ; sensibilité religieuse ; "
      "saisonnalité des ventes."]])

h2("1.2 L'organisation et les équipes")
para("J'ai vu la Vierge est une structure à taille humaine, aujourd'hui composée de neuf salariés, organisée "
     "autour de sa direction et de plusieurs pôles. Le management y est de proximité, dans un esprit encore "
     "familial hérité des débuts de la marque, ce qui favorise la réactivité et la circulation de "
     "l'information.")
para("L'organisation se répartit en quatre pôles : la direction, portée par Alexandra Cefai et Damien "
     "Grauvogel, le pôle digital auquel j'étais rattachée, le pôle commercial et le pôle atelier, où sont "
     "réalisées la peinture et la préparation des commandes. L'organigramme ci-dessous situe ma position au "
     "sein de cet ensemble.")
figure_placeholder("Figure 1 : Organigramme de J'ai vu la Vierge et positionnement de l'alternante")

h2("1.3 L'environnement technique")
para("Mon travail s'appuyait sur un ensemble d'outils numériques complémentaires, qui constituent "
     "l'environnement technique de la marque.")
bullet(("Shopify : ", 'b'), "gestion du site e-commerce, des fiches produits et des données de vente.")
bullet(("Odoo : ", 'b'), "gestion de la relation et des commandes avec les revendeurs professionnels.")
bullet(("Kiliba : ", 'b'), "solution d'emailing automatisé, pilotée par l'intelligence artificielle et "
        "intégrée à Shopify.")
bullet(("Trello : ", 'b'), "planification des tâches et suivi de l'avancement des contenus.")
bullet(("Les outils des plateformes sociales : ", 'b'), "Instagram, TikTok et Facebook, pour la "
        "programmation et le suivi des publications.")
bullet(("Un studio d'emailing sur mesure : ", 'b'), "développé pour les communications les plus premium, "
        "afin de garantir le respect de l'identité visuelle de la marque.")
placeholder("ajoutez vos outils de création de visuels, par exemple Canva ou la suite Adobe")
para("Sur le plan des relations externes, la marque interagit avec ses prestataires, avec ses clients "
     "particuliers via le site et les réseaux, et avec son important réseau de revendeurs et de partenaires "
     "physiques, dont j'assurais le relais sur les canaux digitaux.")
pb()

# ================= 2. LES MISSIONS ET PROJETS
h1('2. Les missions et projets')

h2('2.1 Présentation du poste et des missions')
para("En tant que Cheffe de Projet e-commerce au sein du pôle digital, j'occupais un rôle transversal, entre "
     "communication, création de contenu et commerce en ligne. Mes interlocuteurs hiérarchiques étaient ma "
     "tutrice Camille Abela, qui me briefait et validait mes contenus, et Alexandra Cefai, la créatrice, pour "
     "tout ce qui touchait à l'identité visuelle. Mes missions récurrentes étaient les suivantes.")
bullet(("Animation des réseaux sociaux : ", 'b'), "publication et programmation des posts, des stories et "
        "des vidéos sur Instagram, TikTok et Facebook, et animation de la communauté au quotidien.")
bullet(("Création de contenu vidéo : ", 'b'), "conception et réalisation de stories et de Reels vidéo pour "
        "les réseaux sociaux, un format que j'ai particulièrement investi pour sa forte portée.")
bullet(("Création de contenu visuel : ", 'b'), "participation aux shootings et préparation des visuels, "
        "déclinés pour chaque plateforme.")
bullet(("Gestion du site : ", 'b'), "mise à jour du site et rédaction des fiches produits.")
bullet(("Emailing : ", 'b'), "participation à la conception et à l'envoi des campagnes email.")
bullet(("Reporting : ", 'b'), "suivi hebdomadaire des performances et restitution des résultats.")
para("Notre collaboration reposait sur des rituels réguliers : un brief chaque lundi pour cadrer les "
     "priorités, un point hebdomadaire de suivi et un reporting transmis chaque lundi. Vers l'extérieur, je "
     "livrais mes contenus à la communauté par les publications, mais aussi par la relation directe avec les "
     "clients via le mail et la messagerie d'Instagram et de Facebook.")
para("Deux situations vécues résument bien mon quotidien. La première, plus délicate, a été un partenariat "
     "avec l'Olympique de Marseille, qui hésitait à s'associer à la marque de peur que l'univers religieux "
     "des statuettes paraisse trop connoté. Cette expérience m'a fait comprendre la sensibilité de l'image de "
     "la marque et l'importance de la manière de présenter les choses, en insistant sur la dimension "
     "culturelle et populaire de l'objet.")
para("La seconde a été une vraie réussite, la collaboration avec Karine Le Marchand. Concrètement, elle "
     "s'est construite autour d'un produit spécifique, un ex-voto baptisé « le cœur sur la main », créé dans "
     "le cadre d'un partenariat entre Karine Le Marchand et J'ai vu la Vierge. Le format de l'opération était "
     "simple mais redoutablement efficace, puisque Karine Le Marchand a présenté le produit à sa communauté "
     "à travers une story Instagram. Les retombées ont été immédiates et très concrètes, car cette seule "
     "prise de parole a généré plus de cinquante achats du produit. Cet exemple m'a montré à quel point une "
     "communication ciblée, portée par la bonne personne et au bon format, peut transformer une simple story "
     "en résultats commerciaux réels.")

h2('2.2 Focus projet : la stratégie de communication digitale')
para("Le projet central de mon alternance a été la stratégie de communication digitale de la marque. Il "
     "répond directement à sa stratégie d'entreprise, qui vise à transformer une forte notoriété sociale en "
     "ventes en ligne durables. J'y ai assumé un vrai niveau de responsabilité, de la proposition des "
     "contenus jusqu'à l'analyse de leurs performances.")

h3('2.2.1 Constat initial et problématique')
para("Au démarrage de mon alternance, la marque possédait déjà une belle communauté, mais très inégale d'un "
     "réseau à l'autre. Sur Instagram, de loin notre plateforme la plus forte, nous comptions environ 30 000 "
     "abonnés. Sur Facebook, la communauté était plus modeste, avec près de 3 000 abonnés. Sur TikTok, enfin, "
     "le compte n'en était qu'à ses tout débuts, avec seulement 28 abonnés, ce qui représentait autant une "
     "faiblesse qu'une vraie marge de progression. Côté emailing, la marque disposait déjà d'une base "
     "d'environ 1 200 contacts clients et envoyait régulièrement des newsletters, ce qui constituait un socle "
     "solide sur lequel m'appuyer, même si ce canal pouvait encore être mieux structuré et optimisé.")
para("Ce panorama révélait un déséquilibre. La marque était très visible par moments, mais cette visibilité "
     "reposait sur un canal fragile, les réseaux sociaux, et se convertissait mal en trafic et en ventes. La "
     "sensibilité de l'image ajoutait une contrainte, car il ne suffisait pas de communiquer plus, il fallait "
     "communiquer juste. De là découle la problématique du projet : comment développer la visibilité et les "
     "performances e-commerce de la marque grâce à une stratégie de communication digitale cohérente, tout en "
     "préservant une image singulière et sensible ?")

h3('2.2.2 Cibles et objectifs')
para("La cible principale correspond au persona décrit plus haut, cette femme de trente à soixante ans "
     "sensible à l'objet qui a du sens. À partir de là, la marque m'avait fixé des objectifs clairs, qui ont "
     "servi de boussole tout au long du projet.")
bullet("Développer la visibilité et la notoriété de la marque.")
bullet("Augmenter le trafic et les ventes sur le site e-commerce.")
bullet("Élargir l'audience sans diluer ni trahir l'identité de la marque.")
bullet("Renforcer la relation et la fidélité des clients existants.")

h3('2.2.3 Les scénarios et stratégies envisagés')
para("Pour atteindre ces objectifs, j'ai raisonné autour de trois scénarios possibles, que j'ai comparés "
     "avant de trancher.")
add_table("Tableau 4 : Comparaison des trois scénarios de stratégie",
    ["Critère", "A : Tout organique", "B : Emailing / CRM", "C : Stratégie mixte"],
    [["Coût", "Faible", "Moyen (abonnement)", "Maîtrisé"],
     ["Délai", "Court", "Moyen", "Progressif"],
     ["Cohérence avec l'image", "Très forte", "À surveiller", "Forte et maîtrisée"],
     ["Impact visibilité", "Fort", "Faible", "Fort"],
     ["Impact ventes", "Limité", "Fort", "Fort"]])
para("J'ai retenu le scénario C, la stratégie mixte, car c'est le seul qui répond à l'ensemble des objectifs "
     "à la fois : la visibilité par les réseaux, la conversion par l'emailing et la maîtrise de l'image par "
     "des temps forts soigneusement préparés. À l'intérieur de ce scénario, le levier emailing posait une "
     "question d'outil que j'ai instruite à part.")
add_table("Tableau 5 : Comparaison des solutions d'emailing envisagées",
    ["Solution", "Atouts", "Limites"],
    [["Kiliba", "Ciblage par intelligence artificielle selon le comportement des utilisateurs ; intégration "
      "directe à Shopify ; mise en place rapide.", "Personnalisation graphique limitée ; coût d'abonnement."],
     ["Shopify natif", "Intégré et simple ; peu coûteux.", "Design et fonctionnalités limités ; peu "
      "différenciant."],
     ["Outil sur mesure", "Contrôle total de l'identité visuelle ; adaptable aux temps forts ; gratuit à "
      "l'usage.", "Nécessite du développement et de la maintenance."]])
para("Le raisonnement a conduit à privilégier Kiliba pour la partie automatisée et ciblée, tout en "
     "développant un studio d'emailing sur mesure pour les communications premium où l'identité visuelle "
     "prime. Ce choix par les risques et par la cohérence avec les objectifs m'a permis de défendre la "
     "décision de manière argumentée.")

h3('2.2.4 Mise en œuvre : organisation, méthodes et planning')
para("Pour piloter cette stratégie, je me suis appuyée sur une organisation structurée. Mon outil central "
     "était Trello, sur lequel je planifiais toutes les tâches sous forme de tableau, dans une logique "
     "kanban, en suivant chaque contenu de l'idée jusqu'à la publication. Chaque création suivait un circuit "
     "de validation en deux temps, par la créatrice et par ma tutrice, ce qui garantissait la cohérence avec "
     "l'identité de la marque.")
para("Sur les réseaux, j'ai travaillé une ligne éditoriale fidèle au ton de la marque, en équilibrant "
     "plusieurs familles de contenus : les contenus produits, les coulisses, les temps forts et les formats "
     "spontanés inspirés des tendances. J'ai particulièrement investi la vidéo courte, avec les Reels et "
     "TikTok, car c'est le format qui offre la meilleure portée organique. Les actions se sont déployées "
     "progressivement sur l'année, selon le rétroplanning ci-dessous.")
add_table("Tableau 6 : Rétroplanning simplifié des actions sur l'année",
    ["Période", "Phase", "Actions principales"],
    [[("[à préciser]", 'ph'), "Prise en main", "Découverte de la marque, des outils et de la ligne "
      "éditoriale."],
     [("[à préciser]", 'ph'), "Montée en autonomie", "Animation régulière des réseaux, contenus et fiches "
      "produits, rituels de reporting."],
     [("[à préciser]", 'ph'), "Temps forts", "Préparation et relais des opérations, dont la collaboration "
      "Karine Le Marchand."],
     [("[à préciser]", 'ph'), "Emailing", "Mise en place des solutions d'emailing et des premiers modèles."],
     [("[à préciser]", 'ph'), "Optimisation", "Analyse des performances et ajustements."]])
figure_placeholder("Figure 2 : Diagramme de Gantt du projet sur l'année d'alternance")

h3('2.2.5 Les livrables')
para("Le principal livrable technique du projet est le studio d'emailing sur mesure. Cet outil repose sur "
     "une direction artistique sobre et élégante, de type musée, avec des modèles prêts à l'emploi comme une "
     "invitation de type vernissage, un email de bienvenue et un programme du mois. L'utilisateur choisit un "
     "modèle, renseigne les contenus, prévisualise le rendu comme une œuvre encadrée, puis envoie la "
     "campagne. Il garantit que chaque email respecte parfaitement l'univers de la marque. À cela s'ajoutent "
     "l'ensemble des contenus produits pour les réseaux et les fiches produits enrichies sur le site. Des "
     "captures figurent en annexe.")

h3('2.2.6 Les indicateurs de performance et les résultats')
para("Pour piloter la stratégie, j'ai suivi des indicateurs répartis sur tout le parcours client, de la "
     "notoriété jusqu'à la fidélisation, afin de comprendre où se situaient les points forts et les points "
     "de fuite.")
add_table("Tableau 7 : Les indicateurs de performance suivis",
    ["Objectif", "Indicateurs", "Outil de mesure"],
    [["Notoriété", "Abonnés, portée, impressions", "Meta Business Suite, TikTok Analytics"],
     ["Engagement", "Taux d'engagement, partages, enregistrements", "Outils natifs des plateformes"],
     ["Trafic", "Sessions, part du trafic social et email", "Shopify Analytics"],
     ["Conversion", "Taux de conversion, chiffre d'affaires, panier moyen", "Shopify"],
     ["Emailing", "Taux d'ouverture, taux de clic, désabonnement", "Kiliba, studio sur mesure"]])
para("Le tableau ci-dessous met en regard la situation de départ et les résultats obtenus. Les valeurs de "
     "départ sont connues, celles d'arrivée sont à compléter avec vos chiffres réels.")
add_table("Tableau 8 : Résultats avant et après la mise en œuvre",
    ["Indicateur", "Avant", "Après", "Objectif"],
    [["Abonnés Instagram", "environ 30 000", ("[à compléter]", 'ph'), ("[à compléter]", 'ph')],
     ["Abonnés Facebook", "environ 3 000", ("[à compléter]", 'ph'), ("[à compléter]", 'ph')],
     ["Abonnés TikTok", "28", ("[à compléter]", 'ph'), ("[à compléter]", 'ph')],
     ["Base de contacts email", "environ 1 200", ("[à compléter]", 'ph'), ("[à compléter]", 'ph')],
     ["Taux d'ouverture email", ("[à compléter]", 'ph'), ("[à compléter]", 'ph'), ("[à compléter]", 'ph')],
     ["Taux de conversion", ("[à compléter]", 'ph'), ("[à compléter]", 'ph'), ("[à compléter]", 'ph')]])
placeholder("commentez vos chiffres réels : quelles actions ont le mieux fonctionné et quels temps forts "
            "ont généré le plus de visibilité et de ventes")

h3('2.2.7 Difficultés, valeur ajoutée et axes d\'amélioration')
para("La principale difficulté a été la sensibilité de l'image de la marque, illustrée par l'hésitation de "
     "l'Olympique de Marseille, qui m'a appris à communiquer avec justesse. Une autre difficulté, plus "
     "quotidienne, a été d'apprendre à jongler entre des tâches très différentes dans une même journée, ce "
     "que j'ai structuré grâce à la planification et aux rituels de la semaine.")
placeholder("ajoutez si vous le souhaitez une ou deux autres difficultés concrètes rencontrées sur le projet")
para("Ma valeur ajoutée a été d'apporter à la marque une animation digitale régulière et cohérente, de "
     "contribuer à la réussite de temps forts comme la collaboration Karine Le Marchand, et de faire monter "
     "en puissance des canaux encore peu exploités comme TikTok et l'emailing. Les principaux axes "
     "d'amélioration que j'identifie sont de structurer plus tôt le levier de l'emailing et la collecte des "
     "données clients, et de mettre en place dès le départ un tableau de suivi des indicateurs plus complet "
     "pour mesurer l'impact de chaque action avec des preuves chiffrées.")
pb()

# ================= 3. CONCLUSION
h1('3. Conclusion')

h2('3.1 Synthèse')
para("Durant mon alternance chez J'ai vu la Vierge, j'ai piloté la stratégie de communication digitale d'une "
     "marque à l'identité forte et sensible. Partant d'une visibilité concentrée sur Instagram et d'une "
     "conversion insuffisante, j'ai animé au quotidien Instagram, TikTok et Facebook, produit les contenus et "
     "les fiches produits, participé à l'emailing et assuré le reporting des performances. J'ai comparé "
     "plusieurs scénarios avant de retenir une stratégie mixte, combinant l'animation des réseaux, l'emailing "
     "et les temps forts, et j'ai contribué à des opérations marquantes comme la collaboration avec Karine Le "
     "Marchand, qui a généré plus de cinquante ventes à partir d'une seule story. Cette lecture d'ensemble "
     "suffit à comprendre l'essentiel de ce que j'ai réalisé et des résultats obtenus.")

h2('3.2 Bilan')
para(("Quelles compétences ai-je développées ? ", 'b'),
     "J'ai appris à piloter un projet de communication digitale en planifiant et en coordonnant les tâches "
     "à l'aide de Trello et d'un circuit de validation. J'ai développé la capacité à animer des réseaux "
     "sociaux et à créer des contenus en produisant régulièrement des posts, des stories et des vidéos "
     "courtes adaptés à chaque plateforme. J'ai renforcé ma maîtrise de l'analyse de performance en suivant "
     "des indicateurs et en produisant un reporting hebdomadaire. J'ai enfin acquis des compétences "
     "e-commerce concrètes en utilisant Shopify pour le site et les fiches produits et Odoo pour les "
     "revendeurs.")
para(("Qu'ai-je appris en termes de savoir-être et de posture professionnelle ? ", 'b'),
     "J'ai surtout gagné en autonomie. Au début, lorsqu'il fallait répondre à des commentaires négatifs, je "
     "demandais systématiquement de l'aide ; avec le temps, j'ai appris à gérer ces messages seule, en "
     "gardant le bon ton et en protégeant l'image de la marque. Le reporting m'intimidait et je "
     "l'appréhendais chaque semaine, mais à force de le pratiquer, j'ai gagné en aisance pour exposer et "
     "défendre mon travail. J'ai aussi appris à décider seule quand la situation l'exigeait et à être force "
     "de proposition. Ce sont ces petits pas, répétés semaine après semaine, qui m'ont fait passer d'une "
     "posture d'exécutante à une posture de cheffe de projet.")
para(("Mon projet professionnel s'est-il conforté, a-t-il évolué ou est-il remis en question ? ", 'b'),
     "Cette expérience a nettement conforté mon projet. Elle m'a fait découvrir le e-commerce, un terrain que "
     "je ne connaissais pas et qui me passionne désormais, et elle m'a donné le goût et la confiance du "
     "pilotage de projet. À l'issue de mon Bachelor, je souhaite poursuivre en mastère afin d'approfondir mes "
     "compétences et, à terme, piloter des projets digitaux de plus grande ampleur.")
pb()

# ================= ANNEXES
h1('Annexes')
para("Les annexes rassemblent les éléments concrets qui appuient ce dossier. Insérez ci-dessous vos "
     "captures et documents réels.")
for a in [
    "Annexe 1 : organigramme détaillé de J'ai vu la Vierge.",
    "Annexe 2 : captures d'écran du studio d'emailing sur mesure.",
    "Annexe 3 : exemples de publications et de visuels réalisés pour les réseaux sociaux.",
    "Annexe 4 : capture du tableau Trello de suivi des tâches.",
    "Annexe 5 : exemple de reporting hebdomadaire.",
    "Annexe 6 : extraits de statistiques (réseaux sociaux, site, emailing).",
    "Annexe 7 : visuels de la collaboration avec Karine Le Marchand."]:
    p = doc.add_paragraph(); r = p.add_run(a); r.bold = True
    q = doc.add_paragraph(); rr = q.add_run('[ document ou capture à insérer ]')
    rr.font.highlight_color = WD_COLOR_INDEX.YELLOW; rr.italic = True

h2('Glossaire')
for term, desc in [
    ("Benchmark", "analyse comparative des pratiques des concurrents ou du marché."),
    ("Brief", "échange qui cadre les objectifs et les attentes d'une action."),
    ("CRM", "gestion de la relation client."),
    ("KPI", "indicateur clé de performance."),
    ("Kanban", "organisation visuelle des tâches par colonnes."),
    ("Persona", "portrait type d'un client cible."),
    ("Portée", "nombre de personnes uniques ayant vu un contenu."),
    ("Rétroplanning", "planning construit à rebours à partir de la date finale."),
    ("Taux de conversion", "part des visiteurs qui réalisent l'action attendue."),
    ("Taux d'ouverture", "part des destinataires qui ouvrent un email."),
    ("Template", "modèle prêt à l'emploi pour concevoir un email cohérent.")]:
    p = doc.add_paragraph(); r = p.add_run(term + " : "); r.bold = True; p.add_run(desc)

h2('Table des illustrations')
for item in illustrations:
    p = doc.add_paragraph(style='List Bullet'); p.add_run(item)

doc.core_properties.title = "Dossier BC3 EEMI - Estelle CASTEROT"
doc.core_properties.author = "Estelle CASTEROT"
out = "/home/user/newsletter_ynov/dossier-bc3/Dossier_BC3_EEMI_Estelle_CASTEROT.docx"
doc.save(out)
print("OK ->", out)
