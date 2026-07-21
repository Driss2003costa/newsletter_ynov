# -*- coding: utf-8 -*-
"""
Dossier BC3 (Retour d'expérience) d'Estelle CASTEROT.
Structure : cahier des charges EEMI + plan détaillé de l'Exemple 1 (table des matières).
Zones surlignées en jaune = à compléter / vérifier.
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

st = doc.styles['Normal']
st.font.name = 'Calibri'; st.font.size = Pt(12)
st.paragraph_format.space_before = Pt(6); st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing = 1.0
for lvl, sz in [('Heading 1', 18), ('Heading 2', 15), ('Heading 3', 13)]:
    s = doc.styles[lvl]
    s.font.name = 'Calibri'; s.font.size = Pt(sz)
    s.font.color.rgb = RGBColor(0x1a, 0x1a, 0x1a)

illustrations = []

def seg(paragraph, segments):
    for s in segments:
        text, kind = (s if isinstance(s, tuple) else (s, 'n'))
        r = paragraph.add_run(text)
        if kind == 'ph': r.font.highlight_color = WD_COLOR_INDEX.YELLOW; r.italic = True
        elif kind == 'b': r.bold = True
def para(*s):
    p = doc.add_paragraph(); p.alignment = JUST; seg(p, s); return p
def lead(title, *s):
    p = doc.add_paragraph(); p.alignment = JUST
    r = p.add_run(title + " "); r.bold = True; seg(p, s); return p
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
            if kind == 'ph': r.font.highlight_color = WD_COLOR_INDEX.YELLOW; r.italic = True
    c = doc.add_paragraph(); c.alignment = CENTER
    cr = c.add_run(cap); cr.italic = True; cr.font.size = Pt(9)
    doc.add_paragraph()

# ---------- mise en page EEMI
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
pr = fp.add_run()
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
C('[ Logo J\'ai vu la Vierge ]          [ Logo EEMI ]', 12, hl=True); gap(2)
C("Dossier de Retour d'Expérience sur activités professionnelles", 24, bold=True)
C("Épreuve certifiante du Bloc de Compétences 3 (BC3)", 13)
C("Titre Chef de projets digitaux", 12, italic=True); gap(2)
C("Estelle CASTEROT", 18, bold=True); gap(1)
C("Bachelor 3 Communication, Marketing et Événementiel", 12)
C("Promotion 2025 / 2026", 12); gap(2)
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
para("Pour générer la pagination, sélectionnez tout le document puis appuyez sur F9, ou faites un clic "
     "droit sur le sommaire et choisissez « Mettre à jour les champs ».")
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
para("Retour d'expérience en entreprise")
h3("Étudiante ou alternante")
for lab, val in [("Nom", "CASTEROT"), ("Prénom", "Estelle"),
                 ("Classe", "Bachelor 3 Communication, Marketing et Événementiel"),
                 ("Entreprise", "J'ai vu la Vierge")]:
    p = doc.add_paragraph(); a = p.add_run(lab + " : "); a.bold = True; p.add_run(val)
h3("Tutrice ou maître d'apprentissage")
for lab, val in [("Nom", "ABELA"), ("Prénom", "Camille"), ("Fonction", "Responsable de Projet e-commerce")]:
    p = doc.add_paragraph(); a = p.add_run(lab + " : "); a.bold = True; p.add_run(val)
h3("Exigences au regard du présent dossier")
for txt in [
    "l'entreprise autorise son accès à l'équipe pédagogique, aux évaluateurs et aux apprenants, sans restriction de temps ;",
    "l'entreprise autorise son accès à l'équipe pédagogique et aux évaluateurs, sans restriction de temps ;",
    "l'entreprise limite son accès à l'équipe pédagogique et aux évaluateurs, jusqu'à la tenue du jury de diplomation."]:
    p = doc.add_paragraph(); p.add_run("☐  " + txt)
gap(1); para("Signature et cachet de l'entreprise :")
pb()

# ================= REMERCIEMENTS
h1('Remerciements')
para("Avant d'entrer dans le vif de ce retour d'expérience, je souhaite adresser mes remerciements à toutes "
     "les personnes qui ont rendu cette alternance aussi riche.")
para("Je remercie tout particulièrement Camille Abela, ma tutrice et Responsable de Projet e-commerce, pour "
     "sa confiance, sa disponibilité et l'accompagnement qu'elle m'a offert tout au long de l'année. Ses "
     "briefs, ses retours et nos points hebdomadaires m'ont permis de progresser semaine après semaine et de "
     "gagner en autonomie sur un métier que je découvrais.")
para("Je remercie également Alexandra Cefai, créatrice de la marque J'ai vu la Vierge, ainsi que l'ensemble "
     "de l'équipe, qui m'ont accueillie avec bienveillance et m'ont fait confiance sur des sujets à forte "
     "visibilité.")
para("Mes remerciements vont enfin à l'équipe pédagogique et à mon référent de formation, qui m'ont donné les "
     "repères méthodologiques nécessaires pour mener à bien mes missions et pour prendre le recul attendu dans "
     "ce dossier.")
pb()

# ================= INTRODUCTION
h1('Introduction')
para("J'ai réalisé mon alternance de troisième année de Bachelor Communication, Marketing et Événementiel au "
     "sein de la marque J'ai vu la Vierge, selon un rythme de deux semaines en entreprise pour une semaine à "
     "l'école. J'y ai occupé le poste de Cheffe de Projet e-commerce, au sein du pôle digital, sous la "
     "responsabilité de ma tutrice Camille Abela.")
para("J'ai choisi cette alternance parce qu'elle correspondait précisément à mon projet professionnel. Je "
     "voulais apprendre à piloter des projets digitaux de bout en bout et découvrir le e-commerce, un univers "
     "que je connaissais peu et qui me semblait porteur. Rejoindre une marque à l'identité aussi singulière "
     "que J'ai vu la Vierge représentait un défi stimulant, à la croisée de la communication, du marketing et "
     "de l'événementiel. Cette expérience s'inscrit pleinement dans mon ambition de poursuivre en mastère puis "
     "de devenir cheffe de projet.")
para("La marque réinvente la statuette de la Vierge Marie en objet de décoration contemporain, à la rencontre "
     "de l'iconographie religieuse, de l'artisanat et de la culture pop. Ce positionnement fait à la fois sa "
     "force et sa principale difficulté de communication, car il faut proposer un objet à forte charge "
     "symbolique à un public large sans trahir son identité. De ce constat est née la problématique qui guide "
     "ce dossier.")
p = doc.add_paragraph(); p.alignment = CENTER
r = p.add_run("Comment développer la visibilité et les performances e-commerce de J'ai vu la Vierge grâce à "
              "une stratégie de communication digitale cohérente, tout en préservant une image de marque "
              "singulière et sensible ?"); r.bold = True; r.italic = True
para("Pour y répondre, je présente d'abord l'entreprise, son organisation et son environnement. J'expose "
     "ensuite mes missions et responsabilités, puis le projet central de mon alternance, la stratégie de "
     "communication digitale, avant de détailler l'ensemble de mes missions. Je termine par un retour "
     "d'expérience, une synthèse et un bilan.")
pb()

# ================= 1. L'ENTREPRISE
h1("1. L'entreprise")

h2("a. Présentation de l'entreprise")
h3("i. Historique et activités")
para("J'ai vu la Vierge est une marque de décoration qui revisite une figure très ancienne, la statuette de "
     "la Vierge Marie, pour en faire un objet contemporain, coloré et désirable. Là où l'objet religieux "
     "classique reste discret, la marque en fait une pièce de décoration assumée, à la fois spirituelle et "
     "pop, avec l'ambition de bousculer les codes de la décoration dévote.")
para("La société a été créée en 2018 par Alexandra Cefai, journaliste pendant vingt ans à La Provence, et son "
     "conjoint Damien Grauvogel, artiste et designer produit. Le couple tenait auparavant une galerie d'art "
     "au pied de Notre-Dame de la Garde, à Marseille. L'idée est née un lendemain de Fashion Week, en "
     "imaginant la Bonne Mère vêtue d'une robe rouge ou rose fluo, avec cette question amusée : pourquoi "
     "n'aurait-elle pas le droit de s'habiller comme elle le veut ? Le pari était lancé.")
para("L'aventure a d'abord été familiale. Alexandra s'occupait de la partie commerciale, Damien du design et "
     "de la production, et la mère de Damien du conditionnement. Le concept a connu un succès rapide, "
     "notamment grâce au salon Maison et Objet, qui a ouvert la marque à l'international. Aujourd'hui, "
     "l'entreprise est installée dans le quartier de La Pomme, à Marseille. Quelques chiffres clés résument "
     "son développement.")
bullet(("Statut : ", 'b'), "PME au statut de SAS, créée en 2018 à Marseille.")
bullet(("Effectif : ", 'b'), "de 3 salariés à ses débuts à 9 aujourd'hui.")
bullet(("Distribution : ", 'b'), "plus de 400 revendeurs en France et des revendeurs à l'international, "
        "notamment à Tokyo, New York et Séoul.")
bullet(("Bascule vers le digital : ", 'b'), "pendant le confinement, les ventes du site sont passées de "
        "2 715,85 euros à 34 105,74 euros de chiffre d'affaires net d'une année sur l'autre.")

h3("ii. Positionnement sur le marché")
para("La marque occupe un positionnement premium et affinitaire : on n'achète pas seulement un objet, on "
     "adhère à une histoire et à une esthétique. Elle s'adresse à une clientèle majoritairement féminine, "
     "avec un cœur de cible situé entre trente et soixante ans. Pour orienter mes contenus, je me suis "
     "appuyée sur un persona type : une femme active et urbaine, attirée par les objets qui racontent une "
     "histoire, présente sur Instagram et attachée à l'authenticité d'une marque.")
placeholder("précisez si vous le souhaitez le panier moyen et la fourchette de prix des produits")
para("La distribution repose sur plusieurs canaux complémentaires : le site e-commerce propulsé par Shopify, "
     "une plateforme dédiée aux revendeurs sous Odoo, et un réseau de partenaires physiques prestigieux comme "
     "Le Printemps, le Mucem, Maison et Objet, Boboboom ou l'Olympique de Marseille, sans oublier des "
     "collaborations médiatiques telles que celle menée avec Karine Le Marchand. Sur son marché, la marque "
     "évolue face à des concurrents qui exploitent le même imaginaire, notamment Sapristi et Miraculeuse. Ce "
     "qui la distingue tient à deux atouts : une présence sur les réseaux sociaux nettement plus dynamique et "
     "un réseau de très bons commerçants et partenaires.")

h3("iii. Analyse de l'environnement")
lead("Environnement externe.", "J'ai synthétisé l'environnement externe de la marque dans une grille PESTEL, "
     "qui passe en revue les grands facteurs qui influencent son activité.")
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
     ["Légal", "Cadre du RGPD pour l'emailing et obligations propres au e-commerce."]])
lead("Environnement interne et synthèse SWOT.", "En croisant les forces et faiblesses internes avec les "
     "opportunités et menaces externes, j'obtiens la matrice SWOT suivante, qui résume la situation "
     "stratégique de la marque.")
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

h2("b. L'organisation et les équipes")
h3("i. Organisation de la structure")
para("J'ai vu la Vierge est une structure à taille humaine, aujourd'hui composée de neuf salariés, avec un "
     "management de proximité dans un esprit encore familial hérité des débuts de la marque. L'organisation "
     "se répartit en quatre pôles : la direction, portée par Alexandra Cefai et Damien Grauvogel, le pôle "
     "digital auquel j'étais rattachée, le pôle commercial et le pôle atelier, où sont réalisées la peinture "
     "et la préparation des commandes. L'organigramme ci-dessous situe ma position au sein de cet ensemble.")
figure_placeholder("Figure 1 : Organigramme de J'ai vu la Vierge et positionnement de l'alternante")
h3("ii. Les différents métiers")
para("Chaque pôle regroupe des métiers complémentaires. La direction assure la création, le design produit "
     "et la stratégie globale. Le pôle commercial gère la relation avec les revendeurs et le développement "
     "des ventes professionnelles. Le pôle atelier réalise la production, la peinture et la préparation des "
     "commandes. Le pôle digital, enfin, porte l'image de la marque et les ventes en ligne, à travers le "
     "site e-commerce, les réseaux sociaux et l'emailing. C'est dans ce dernier pôle que s'inscrivait mon "
     "poste.")

h2("c. L'environnement technique")
para("Sur le plan technique, J'ai vu la Vierge s'appuie sur un écosystème d'outils numériques qui "
     "structurent son activité en ligne et sur lesquels reposait une grande partie de mon travail.")
bullet(("Shopify : ", 'b'), "le site e-commerce, les fiches produits et les données de vente.")
bullet(("Odoo : ", 'b'), "la gestion des commandes et de la relation avec les revendeurs professionnels.")
bullet(("Kiliba : ", 'b'), "l'emailing automatisé, piloté par l'intelligence artificielle et intégré à "
        "Shopify.")
bullet(("Un studio d'emailing sur mesure : ", 'b'), "pour les communications premium respectant "
        "parfaitement l'identité visuelle de la marque.")
bullet(("Trello : ", 'b'), "la planification et le suivi des tâches.")
bullet(("Les outils des plateformes sociales : ", 'b'), "Meta Business Suite pour Instagram et Facebook et "
        "les outils natifs de TikTok, pour la programmation et le suivi des publications.")
placeholder("ajoutez vos outils de création et de montage vidéo, par exemple Canva, CapCut ou la suite Adobe")
para("Cet environnement technique s'accompagne de relations suivies avec plusieurs acteurs externes. La "
     "marque collabore avec ses prestataires, s'adresse à ses clients particuliers par le site et les réseaux "
     "sociaux, et anime un large réseau de revendeurs et de partenaires physiques, dont je relayais les "
     "opérations sur les canaux digitaux.")
placeholder("précisez si vous le souhaitez vos prestataires clés, par exemple la logistique, le transporteur "
            "ou d'éventuels prestataires techniques")
pb()

# ================= 2. LES MISSIONS ET PROJETS
h1('2. Les missions et projets')

h2('a. Missions et responsabilités')
para("En tant que Cheffe de Projet e-commerce au sein du pôle digital, j'occupais un rôle transversal, entre "
     "communication, création de contenu et commerce en ligne. Mes interlocuteurs hiérarchiques étaient ma "
     "tutrice Camille Abela, qui me briefait et validait mes contenus, et Alexandra Cefai, la créatrice, pour "
     "tout ce qui touchait à l'identité visuelle. J'avais la responsabilité de faire vivre la marque au "
     "quotidien sur ses canaux digitaux, avec un vrai niveau d'autonomie sur la proposition et la production "
     "des contenus, dans le respect des validations. Pour mener à bien ces missions, je disposais des accès "
     "aux plateformes sociales, au site Shopify, à Odoo, à l'outil d'emailing et à Trello pour l'organisation.")

h2('b. Interaction avec les services')
para("Mon poste m'amenait à interagir avec l'ensemble des services de l'entreprise. Avec la direction, "
     "j'échangeais sur l'identité de la marque et la validation des contenus les plus sensibles. Avec le pôle "
     "commercial, je coordonnais la mise en avant des partenaires et des revendeurs sur les réseaux. Avec le "
     "pôle atelier, je récupérais les informations produits nécessaires aux fiches et aux visuels. Enfin, "
     "j'étais en relation directe avec les clients, à qui je répondais par mail et par la messagerie "
     "d'Instagram et de Facebook. Notre organisation reposait sur des rituels réguliers : un brief chaque "
     "lundi pour cadrer les priorités, un point hebdomadaire de suivi et un reporting transmis chaque lundi.")

h2('c. Stratégie de communication')
h3('i. Constat initial')
para("Au démarrage de mon alternance, la marque possédait déjà une belle communauté, mais très inégale d'un "
     "réseau à l'autre, et une visibilité qui se convertissait mal en ventes. La sensibilité de l'image "
     "ajoutait une contrainte, car il ne suffisait pas de communiquer plus, il fallait communiquer juste. Ce "
     "constat a fait naître la problématique du projet : développer la visibilité et les ventes en ligne "
     "grâce à une stratégie de communication digitale cohérente, tout en préservant une image singulière et "
     "sensible.")
h3('ii. Les cibles')
para("La cible principale correspond au persona décrit plus haut, cette femme de trente à soixante ans "
     "sensible à l'objet qui a du sens, présente sur les réseaux sociaux et sensible à l'authenticité. À côté "
     "de cette cible particulier, la marque adresse aussi une cible professionnelle, celle des revendeurs, "
     "que le pôle commercial anime.")
h3('iii. Les objectifs')
para("À partir de ces cibles, la marque m'avait fixé des objectifs clairs, qui ont servi de boussole tout au "
     "long du projet.")
bullet("Développer la visibilité et la notoriété de la marque.")
bullet("Augmenter le trafic et les ventes sur le site e-commerce.")
bullet("Élargir l'audience sans diluer ni trahir l'identité de la marque.")
bullet("Renforcer la relation et la fidélité des clients existants.")
h3('iv. L\'audit des réseaux sociaux')
para("Avant d'agir, j'ai dressé un état des lieux chiffré de notre présence digitale.")
bullet(("Instagram : ", 'b'), "environ 30 000 abonnés, de loin notre plateforme la plus forte.")
bullet(("Facebook : ", 'b'), "près de 3 000 abonnés, une communauté plus modeste.")
bullet(("TikTok : ", 'b'), "seulement 28 abonnés, un compte tout juste lancé et donc une vraie marge de "
        "progression.")
bullet(("Emailing : ", 'b'), "une base d'environ 1 200 contacts clients et des newsletters déjà envoyées "
        "régulièrement, un socle solide mais encore à optimiser.")
para("Cet audit confirmait une visibilité très concentrée sur Instagram et un fort potentiel inexploité, "
     "notamment sur la vidéo courte avec TikTok et sur la relation client par email.")

h2('d. Élaboration de la stratégie')
h3('i. Inspirations et analyse')
para("Je me suis inspirée des marques de décoration et de lifestyle qui réussissent sur les réseaux, en "
     "analysant leurs formats, leur ton et leur rythme de publication, puis en les confrontant à l'identité "
     "singulière de J'ai vu la Vierge pour ne garder que ce qui lui ressemblait.")
h3('ii. Élaboration')
para("J'ai raisonné autour de trois scénarios possibles, que j'ai comparés avant de trancher.")
add_table("Tableau 4 : Comparaison des trois scénarios de stratégie",
    ["Critère", "A : Tout organique", "B : Emailing / CRM", "C : Stratégie mixte"],
    [["Coût", "Faible", "Moyen (abonnement)", "Maîtrisé"],
     ["Cohérence avec l'image", "Très forte", "À surveiller", "Forte et maîtrisée"],
     ["Impact visibilité", "Fort", "Faible", "Fort"],
     ["Impact ventes", "Limité", "Fort", "Fort"]])
para("J'ai retenu le scénario C, la stratégie mixte, car c'est le seul qui répond à l'ensemble des objectifs "
     "à la fois. À l'intérieur de ce scénario, le levier emailing posait une question d'outil, que j'ai "
     "tranchée en privilégiant Kiliba pour le ciblage par intelligence artificielle et son intégration à "
     "Shopify, tout en développant un studio d'emailing sur mesure pour les communications premium.")
h3('iii. Organisation')
para("Pour piloter la stratégie, mon outil central était Trello, sur lequel je planifiais toutes les tâches "
     "dans une logique kanban, en suivant chaque contenu de l'idée jusqu'à la publication. Chaque création "
     "suivait un circuit de validation en deux temps, par la créatrice et par ma tutrice, ce qui garantissait "
     "la cohérence avec l'identité de la marque.")
h3('iv. Création de contenu')
para("J'ai construit une ligne éditoriale fidèle au ton de la marque, en équilibrant plusieurs familles de "
     "contenus : les contenus produits qui donnent envie d'acheter, les coulisses qui créent de la proximité, "
     "les temps forts qui font l'événement, et les formats spontanés inspirés des tendances qui captent de "
     "nouveaux publics.")
h3('v. Diffusion')
para("La diffusion suivait un planning réfléchi, avec une cadence régulière de publications adaptée à chaque "
     "plateforme et concentrée sur les temps forts à plus fort impact. Les actions se sont déployées "
     "progressivement sur l'année, selon le rétroplanning ci-dessous.")
add_table("Tableau 5 : Rétroplanning simplifié des actions sur l'année",
    ["Période", "Phase", "Actions principales"],
    [[("[à préciser]", 'ph'), "Prise en main", "Découverte de la marque, des outils et de la ligne éditoriale."],
     [("[à préciser]", 'ph'), "Montée en autonomie", "Animation régulière des réseaux, contenus et fiches produits."],
     [("[à préciser]", 'ph'), "Temps forts", "Opérations et collaborations, dont Karine Le Marchand."],
     [("[à préciser]", 'ph'), "Emailing", "Mise en place des solutions d'emailing et des premiers modèles."],
     [("[à préciser]", 'ph'), "Optimisation", "Analyse des performances et ajustements."]])
figure_placeholder("Figure 2 : Diagramme de Gantt du projet sur l'année d'alternance")
h3('vi. Outils utilisés')
para("Le projet s'appuyait sur un environnement technique complet : Shopify pour le site, les fiches produits "
     "et les données de vente, Odoo pour les revendeurs, Kiliba pour l'emailing automatisé, un studio "
     "d'emailing sur mesure pour les communications premium, Trello pour la gestion de projet, et les outils "
     "natifs d'Instagram, TikTok et Facebook pour la programmation et le suivi.")
placeholder("ajoutez vos outils de création de visuels et de montage vidéo, par exemple Canva, CapCut ou la suite Adobe")
h3('vii. Les différents formats')
para("J'ai travaillé une palette de formats variés pour couvrir tout le parcours d'attention : les posts "
     "pour installer l'univers, les carrousels pour raconter et informer, les stories pour l'instantané et "
     "l'interaction, et les vidéos courtes pour la portée.")
lead("Zoom sur les vidéos.", "Les stories et les Reels vidéo ont été un axe fort de mon travail. Ce sont les "
     "formats qui offrent aujourd'hui la meilleure portée organique et qui permettent de toucher de nouveaux "
     "publics. J'ai conçu, tourné et monté ces vidéos en m'appuyant sur les tendances, ce qui a soutenu la "
     "croissance de la marque, en particulier sur TikTok, où tout restait à construire.")
h3('viii. Indicateurs de performance')
para("Pour piloter la stratégie, j'ai suivi des indicateurs répartis sur tout le parcours client, de la "
     "notoriété jusqu'à la fidélisation.")
add_table("Tableau 6 : Les indicateurs de performance suivis",
    ["Objectif", "Indicateurs", "Outil de mesure"],
    [["Notoriété", "Abonnés, portée, impressions", "Meta Business Suite, TikTok Analytics"],
     ["Engagement", "Taux d'engagement, partages, enregistrements", "Outils natifs des plateformes"],
     ["Trafic", "Sessions, part du trafic social et email", "Shopify Analytics"],
     ["Conversion", "Taux de conversion, chiffre d'affaires, panier moyen", "Shopify"],
     ["Emailing", "Taux d'ouverture, taux de clic", "Kiliba, studio sur mesure"]])
add_table("Tableau 7 : Résultats avant et après la mise en œuvre",
    ["Indicateur", "Avant", "Après", "Objectif"],
    [["Abonnés Instagram", "environ 30 000", ("[à compléter]", 'ph'), ("[à compléter]", 'ph')],
     ["Abonnés Facebook", "environ 3 000", ("[à compléter]", 'ph'), ("[à compléter]", 'ph')],
     ["Abonnés TikTok", "28", ("[à compléter]", 'ph'), ("[à compléter]", 'ph')],
     ["Base de contacts email", "environ 1 200", ("[à compléter]", 'ph'), ("[à compléter]", 'ph')]])
placeholder("commentez vos chiffres réels une fois complétés : quelles actions ont le mieux fonctionné")

h2('e. Les différentes missions')
para("Au delà du pilotage de la stratégie, mon alternance s'est traduite par des missions concrètes et "
     "quotidiennes, que je détaille ici.")
h3('i. Animation des réseaux sociaux')
para("J'animais au quotidien les comptes Instagram, TikTok et Facebook de la marque. Cela comprenait la "
     "programmation et la publication des contenus, mais aussi tout le travail de communauté : répondre aux "
     "commentaires et aux messages, entretenir la relation avec les abonnés et faire remonter leurs retours. "
     "Cette présence régulière est ce qui maintient le lien vivant entre la marque et son public.")
h3('ii. Stories et Reels vidéo')
para("La création de stories et de Reels vidéo a occupé une place importante dans mes missions. Je concevais "
     "les idées, je tournais et je montais ces vidéos, en m'inspirant des tendances tout en respectant "
     "l'univers de la marque. J'ai particulièrement investi ce format court car c'est celui qui génère le "
     "plus de portée et qui a permis de faire connaître la marque à de nouveaux publics, notamment sur TikTok.")
h3('iii. Shootings et création visuelle')
para("Je participais aux shootings des produits et je préparais les visuels, en soignant la mise en scène et "
     "la cohérence avec l'identité de la marque. Chaque visuel était ensuite décliné selon les codes de "
     "chaque plateforme, afin d'être toujours au bon format et au bon endroit.")
h3('iv. Fiches produits et site e-commerce')
para("J'assurais la mise à jour du site e-commerce et la rédaction des fiches produits. L'enjeu était double : "
     "présenter chaque référence de façon claire et désirable pour donner envie d'acheter, et soigner la "
     "rédaction pour servir à la fois l'image de la marque et le référencement du site.")
h3('v. Emailing et newsletters')
para("Je participais à la conception et à l'envoi des campagnes email et des newsletters adressées à notre "
     "base de contacts. Ce canal, que la marque maîtrise totalement, servait à entretenir la relation client, "
     "à annoncer les nouveautés et les temps forts et à soutenir les ventes du site.")
h3('vi. Reporting et suivi des performances')
para("Chaque semaine, je réalisais un reporting des performances, en suivant les indicateurs des réseaux, du "
     "site et de l'emailing. Cette mission m'a appris à mesurer l'impact réel de chaque action, à en tirer "
     "des enseignements et à ajuster la stratégie en conséquence.")

h2('f. Retour d\'expérience')
para("La principale difficulté a été la sensibilité de l'image de la marque, illustrée par l'hésitation de "
     "l'Olympique de Marseille, qui m'a appris à communiquer avec justesse. Une autre difficulté, plus "
     "quotidienne, a été d'apprendre à jongler entre des tâches très différentes dans une même journée, ce "
     "que j'ai structuré grâce à la planification et aux rituels de la semaine.")
placeholder("ajoutez si vous le souhaitez une ou deux autres difficultés concrètes rencontrées")
para("Ma valeur ajoutée a été d'apporter à la marque une animation digitale régulière et cohérente, de "
     "contribuer à des temps forts comme la collaboration Karine Le Marchand, qui a généré plus de cinquante "
     "ventes à partir d'une seule story, et de faire monter en puissance des canaux encore peu exploités "
     "comme TikTok et l'emailing. Les principaux axes d'amélioration que j'identifie sont de structurer plus "
     "tôt le levier de l'emailing et la collecte des données clients, et de mettre en place dès le départ un "
     "tableau de suivi des indicateurs plus complet.")
pb()

# ================= 3. CONCLUSION
h1('3. Conclusion')
h2('a. Synthèse')
para("Durant mon alternance chez J'ai vu la Vierge, j'ai piloté la stratégie de communication digitale d'une "
     "marque à l'identité forte et sensible. Partant d'une visibilité concentrée sur Instagram et d'une "
     "conversion insuffisante, j'ai animé au quotidien Instagram, TikTok et Facebook, produit les contenus, "
     "les stories, les Reels et les fiches produits, participé à l'emailing et assuré le reporting. J'ai "
     "comparé plusieurs scénarios avant de retenir une stratégie mixte, et j'ai contribué à des opérations "
     "marquantes comme la collaboration avec Karine Le Marchand, qui a généré plus de cinquante ventes à "
     "partir d'une seule story. Cette lecture d'ensemble suffit à comprendre l'essentiel de ce que j'ai "
     "réalisé.")
h2('b. Bilan')
para(("Quelles compétences ai-je développées ? ", 'b'),
     "J'ai appris à piloter un projet de communication digitale en planifiant et en coordonnant les tâches "
     "à l'aide de Trello et d'un circuit de validation. J'ai développé la capacité à animer des réseaux "
     "sociaux et à créer des contenus, notamment des stories et des Reels vidéo adaptés à chaque plateforme. "
     "J'ai renforcé ma maîtrise de l'analyse de performance en suivant des indicateurs et en produisant un "
     "reporting hebdomadaire. J'ai enfin acquis des compétences e-commerce concrètes avec Shopify et Odoo.")
para(("Qu'ai-je appris en termes de savoir-être et de posture professionnelle ? ", 'b'),
     "J'ai surtout gagné en autonomie. Au début, lorsqu'il fallait répondre à des commentaires négatifs, je "
     "demandais systématiquement de l'aide ; avec le temps, j'ai appris à gérer ces messages seule, en "
     "gardant le bon ton. Le reporting m'intimidait, mais à force de le pratiquer, j'ai gagné en aisance pour "
     "exposer et défendre mon travail. J'ai aussi appris à décider seule quand la situation l'exigeait et à "
     "être force de proposition. Ce sont ces petits pas, répétés semaine après semaine, qui m'ont fait passer "
     "d'une posture d'exécutante à une posture de cheffe de projet.")
para(("Mon projet professionnel s'est-il conforté, a-t-il évolué ou est-il remis en question ? ", 'b'),
     "Cette expérience a nettement conforté mon projet. Elle m'a fait découvrir le e-commerce, un terrain qui "
     "me passionne désormais, et elle m'a donné le goût et la confiance du pilotage de projet. À l'issue de "
     "mon Bachelor, je souhaite poursuivre en mastère afin d'approfondir mes compétences et, à terme, piloter "
     "des projets digitaux de plus grande ampleur.")
pb()

# ================= 4. BIBLIOGRAPHIE
h1('4. Bibliographie')
for src in [
    "Site officiel de la marque : www.jaivulavierge.com",
    "Comptes Instagram, TikTok et Facebook de J'ai vu la Vierge",
    "Documentation Shopify et Kiliba (aide en ligne des plateformes)",
    "Meta Business Suite et TikTok Analytics (données de performance)"]:
    p = doc.add_paragraph(style='List Bullet'); p.add_run(src)
placeholder("ajoutez toute autre source utilisée : articles, études, ouvrages")
pb()

# ================= ANNEXES
h1('Annexes')
para("Les annexes rassemblent les éléments concrets qui appuient ce dossier.")
for a in [
    "Annexe 1 : organigramme détaillé de J'ai vu la Vierge.",
    "Annexe 2 : captures d'écran du studio d'emailing sur mesure.",
    "Annexe 3 : exemples de publications, de stories et de Reels réalisés.",
    "Annexe 4 : capture du tableau Trello de suivi des tâches.",
    "Annexe 5 : exemple de reporting hebdomadaire.",
    "Annexe 6 : extraits de statistiques (réseaux, site, emailing).",
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
    ("Reel", "format de vidéo courte sur Instagram."),
    ("Rétroplanning", "planning construit à rebours à partir de la date finale."),
    ("Taux de conversion", "part des visiteurs qui réalisent l'action attendue."),
    ("Taux d'ouverture", "part des destinataires qui ouvrent un email.")]:
    p = doc.add_paragraph(); r = p.add_run(term + " : "); r.bold = True; p.add_run(desc)

h2('Table des illustrations')
for item in illustrations:
    p = doc.add_paragraph(style='List Bullet'); p.add_run(item)

doc.core_properties.title = "Dossier BC3 EEMI - Estelle CASTEROT"
doc.core_properties.author = "Estelle CASTEROT"
out = "/home/user/newsletter_ynov/dossier-bc3/Dossier_BC3_EEMI_Estelle_CASTEROT.docx"
doc.save(out)
print("OK ->", out)
