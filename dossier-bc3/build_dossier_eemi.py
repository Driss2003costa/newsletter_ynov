# -*- coding: utf-8 -*-
"""
Dossier BC3 (Retour d'expérience) d'Estelle CASTEROT - Ynov Aix.
Structure : cahier des charges EEMI + plan de l'Exemple 1. Ton humanisé.
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
r = hp.add_run('[ Logo entreprise ]        Estelle Casterot        [ Logo Ynov ]')
r.font.size = Pt(9); r.font.highlight_color = WD_COLOR_INDEX.YELLOW
fp = sec.footer.paragraphs[0]
tabs = fp.paragraph_format.tab_stops
tabs.add_tab_stop(Cm(8), WD_TAB_ALIGNMENT.CENTER)
tabs.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT)
fp.add_run('Bachelor 3 - 2025 / 2026\tEstelle Casterot\t')
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
C('[ Logo J\'ai vu la Vierge ]          [ Logo Ynov ]', 12, hl=True); gap(2)
C("Dossier de Retour d'Expérience sur activités professionnelles", 24, bold=True)
C("Épreuve certifiante du Bloc de Compétences 3 (BC3)", 13)
C("Titre Chef de projets digitaux", 12, italic=True); gap(2)
C("Estelle CASTEROT", 18, bold=True); gap(1)
C("Bachelor 3 Communication, Marketing et Événementiel", 12)
C("Ynov Campus Aix-en-Provence", 12)
C("Promotion 2025 / 2026", 12); gap(2)
for lab, val in [("Entreprise d'accueil", "J'ai vu la Vierge"),
                 ("Poste occupé", "Alternante Cheffe de Projet e-commerce"),
                 ("Créatrice de la marque", "Alexandra Cefai"),
                 ("Tutrice en entreprise", "Camille Abela, Responsable de Projet e-commerce")]:
    p = doc.add_paragraph(); p.alignment = CENTER
    a = p.add_run(lab + " : "); a.bold = True; a.font.size = Pt(12)
    b = p.add_run(val); b.font.size = Pt(12)
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
para("Avant de commencer, je tiens à remercier les personnes qui ont fait de cette alternance une année "
     "aussi enrichissante.")
para("Merci d'abord à Camille Abela, ma tutrice et Responsable de Projet e-commerce. Elle m'a fait confiance "
     "dès le début, s'est toujours rendue disponible et m'a accompagnée toute l'année. Grâce à ses briefs, à "
     "ses retours et à nos points du lundi, j'ai vraiment senti que je progressais semaine après semaine, sur "
     "un métier que je découvrais presque entièrement.")
para("Merci aussi à Alexandra Cefai, la créatrice de J'ai vu la Vierge, et à toute l'équipe. Ils m'ont "
     "accueillie avec beaucoup de bienveillance et m'ont confié des sujets visibles, ce qui m'a beaucoup "
     "responsabilisée.")
para("Enfin, merci à l'équipe pédagogique d'Ynov et à mon référent de formation, qui m'ont donné les méthodes "
     "nécessaires pour mener mes missions et pour prendre le recul attendu dans ce dossier.")
pb()

# ================= INTRODUCTION
h1('Introduction')
para("J'ai effectué mon alternance de troisième année de Bachelor Communication, Marketing et Événementiel à "
     "Ynov Aix, au sein de la marque J'ai vu la Vierge. Mon rythme était de deux semaines en entreprise pour "
     "une semaine à l'école, et j'y occupais le poste de Cheffe de Projet e-commerce, dans le pôle digital, "
     "aux côtés de ma tutrice Camille Abela.")
para("Si j'ai choisi cette alternance, c'est parce qu'elle collait vraiment à ce que je veux faire plus tard. "
     "J'avais envie d'apprendre à gérer des projets digitaux du début à la fin et de découvrir le e-commerce, "
     "un univers qui m'attirait mais que je connaissais mal. Et puis rejoindre une marque aussi singulière que "
     "J'ai vu la Vierge, c'était un vrai défi, à la croisée de la communication, du marketing et de "
     "l'événementiel. Cette année s'inscrit dans mon projet : continuer en mastère, puis devenir cheffe de "
     "projet.")
para("J'ai vu la Vierge réinvente la statuette de la Vierge Marie en objet de décoration. C'est une marque à "
     "part, entre iconographie religieuse, artisanat et culture pop. Ce positionnement fait toute sa force, "
     "mais c'est aussi sa plus grande difficulté en communication : il faut parler d'un objet très symbolique "
     "à un large public, sans jamais trahir son esprit. C'est de là qu'est venue la question qui guide ce "
     "dossier.")
p = doc.add_paragraph(); p.alignment = CENTER
r = p.add_run("Comment développer la visibilité et les performances e-commerce de J'ai vu la Vierge grâce à "
              "une stratégie de communication digitale cohérente, tout en préservant une image de marque "
              "singulière et sensible ?"); r.bold = True; r.italic = True
para("Pour y répondre, je commence par présenter l'entreprise, son organisation et ses outils. Je parle "
     "ensuite de mon poste et de mes responsabilités, puis du projet qui a occupé le cœur de mon année, la "
     "stratégie de communication digitale, avant de détailler chacune de mes missions. Je termine par un "
     "retour d'expérience, une synthèse et un bilan.")
pb()

# ================= 1. L'ENTREPRISE
h1("1. L'entreprise")

h2("a. Présentation de l'entreprise")
h3("i. Historique et activités")
para("J'ai vu la Vierge est une marque de décoration qui prend une figure très ancienne, la statuette de la "
     "Vierge Marie, pour en faire un objet d'aujourd'hui, coloré et désirable. Là où l'objet religieux "
     "classique reste sage et discret, la marque en fait une pièce déco assumée, à la fois spirituelle et pop. "
     "Son idée de départ, c'est de dépoussiérer les codes de la bondieuserie.")
para("La société a été créée en 2018 par Alexandra Cefai, journaliste pendant vingt ans à La Provence, et son "
     "conjoint Damien Grauvogel, artiste et designer produit. Avant cela, le couple tenait une galerie d'art "
     "au pied de Notre-Dame de la Garde, à Marseille. L'idée de la marque leur est venue un lendemain de "
     "Fashion Week, en imaginant la Bonne Mère habillée d'une robe rouge ou rose fluo, avec cette phrase "
     "restée célèbre en interne : pourquoi n'aurait-elle pas le droit de s'habiller comme elle veut ? Le pari "
     "était lancé.")
para("Au début, tout se faisait en famille. Alexandra s'occupait du commercial, Damien du design et de la "
     "production, et la maman de Damien du conditionnement. Le succès est venu vite, notamment grâce au salon "
     "Maison et Objet, qui a ouvert la marque à l'international. Aujourd'hui, l'entreprise est installée dans "
     "le quartier de La Pomme, à Marseille. Quelques chiffres résument bien ce parcours.")
bullet(("Statut : ", 'b'), "PME sous forme de SAS, créée en 2018 à Marseille.")
bullet(("Effectif : ", 'b'), "de 3 salariés au départ à 9 aujourd'hui.")
bullet(("Distribution : ", 'b'), "plus de 400 revendeurs en France et des revendeurs à l'international, "
        "notamment à Tokyo, New York et Séoul.")
bullet(("Bascule vers le digital : ", 'b'), "pendant le confinement, les ventes du site sont passées de "
        "2 715,85 euros à 34 105,74 euros de chiffre d'affaires net d'une année sur l'autre.")

h3("ii. Positionnement sur le marché")
para("La marque se place sur un segment premium et affinitaire : quand on achète une statuette, on achète "
     "surtout une histoire et une esthétique. Sa clientèle est majoritairement féminine, avec un cœur de "
     "cible entre trente et soixante ans. Pour écrire mes contenus, je gardais toujours en tête un persona : "
     "une femme active et citadine, qui aime les objets qui ont une histoire, qui est présente sur Instagram "
     "et qui tient à l'authenticité d'une marque.")
placeholder("précisez si vous le souhaitez le panier moyen et la fourchette de prix des produits")
para("Côté distribution, la marque joue sur plusieurs canaux : le site e-commerce sous Shopify, une "
     "plateforme revendeurs sous Odoo, et un réseau de partenaires physiques prestigieux comme Le Printemps, "
     "le Mucem, Maison et Objet, Boboboom ou l'Olympique de Marseille. À cela s'ajoutent des collaborations "
     "médiatiques, comme celle avec Karine Le Marchand. Sur son marché, elle croise quelques concurrents qui "
     "jouent sur le même imaginaire, notamment Sapristi et Miraculeuse. Ce qui fait vraiment la différence, "
     "ce sont deux choses : une présence beaucoup plus vivante sur les réseaux, et un très bon réseau de "
     "commerçants et de partenaires.")

h3("iii. Analyse de l'environnement")
lead("Environnement externe.", "Pour bien situer le contexte, j'ai résumé l'environnement externe de la "
     "marque dans une grille PESTEL.")
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
     ["Écologique", "Attentes de plus en plus fortes sur l'origine des produits et une fabrication "
      "responsable."],
     ["Légal", "Cadre du RGPD pour l'emailing et obligations propres au e-commerce."]])
lead("Environnement interne et synthèse SWOT.", "En croisant tout cela, les forces et les faiblesses internes "
     "d'un côté, les opportunités et les menaces externes de l'autre, j'obtiens la matrice SWOT ci-dessous, "
     "qui résume assez bien la situation de la marque.")
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
para("J'ai vu la Vierge reste une petite structure, neuf salariés aujourd'hui, avec un management de "
     "proximité et un esprit encore un peu familial, hérité des débuts. L'entreprise s'organise en quatre "
     "pôles : la direction, portée par Alexandra Cefai et Damien Grauvogel, le pôle digital dans lequel je "
     "travaillais, le pôle commercial et le pôle atelier, où l'on peint les pièces et où l'on prépare les "
     "commandes. L'organigramme ci-dessous montre où je me situais.")
figure_placeholder("Figure 1 : Organigramme de J'ai vu la Vierge et positionnement de l'alternante")
h3("ii. Les différents métiers")
para("Chaque pôle a ses métiers. La direction gère la création, le design produit et la stratégie. Le pôle "
     "commercial s'occupe des revendeurs et des ventes professionnelles. Le pôle atelier fabrique, peint et "
     "prépare les commandes. Et le pôle digital, le mien, porte l'image de la marque et les ventes en ligne, "
     "à travers le site, les réseaux sociaux et l'emailing.")

h2("c. L'environnement technique")
para("D'un point de vue technique, mon travail reposait sur plusieurs outils, qui forment l'environnement "
     "numérique de la marque.")
bullet(("Shopify : ", 'b'), "le site e-commerce, les fiches produits et les données de vente.")
bullet(("Odoo : ", 'b'), "la gestion des commandes et de la relation avec les revendeurs.")
bullet(("Kiliba : ", 'b'), "l'emailing automatisé, piloté par l'intelligence artificielle et branché sur "
        "Shopify.")
bullet(("Un studio d'emailing sur mesure : ", 'b'), "pour les envois premium qui doivent coller parfaitement "
        "à l'identité de la marque.")
bullet(("Trello : ", 'b'), "la planification et le suivi de mes tâches.")
bullet(("Les outils des réseaux : ", 'b'), "Meta Business Suite pour Instagram et Facebook, et les outils "
        "de TikTok, pour programmer et suivre les publications.")
placeholder("ajoutez vos outils de création et de montage vidéo, par exemple Canva, CapCut ou la suite Adobe")
para("À côté de ces outils, la marque entretient des relations régulières avec plusieurs acteurs : ses "
     "prestataires, ses clients particuliers qu'elle touche par le site et les réseaux, et son grand réseau "
     "de revendeurs et de partenaires physiques, dont je relayais les opérations en ligne.")
placeholder("précisez si vous le souhaitez vos prestataires clés, par exemple la logistique ou le transporteur")
pb()

# ================= 2. LES MISSIONS ET PROJETS
h1('2. Les missions et projets')

h2('a. Missions et responsabilités')
para("Comme Cheffe de Projet e-commerce dans le pôle digital, j'avais un rôle assez transversal, entre "
     "communication, création et vente en ligne. Mes deux interlocutrices principales étaient Camille, ma "
     "tutrice, qui me briefait et validait mes contenus, et Alexandra, la créatrice, dès qu'il s'agissait de "
     "l'identité visuelle. Concrètement, j'étais responsable de faire vivre la marque au quotidien sur ses "
     "canaux digitaux. J'avais une vraie liberté pour proposer et produire les contenus, du moment que je "
     "respectais les validations. Pour cela, j'avais accès aux réseaux, au site Shopify, à Odoo, à l'outil "
     "d'emailing et à Trello.")

h2('b. Interaction avec les services')
para("Mon poste me faisait travailler avec presque tous les services. Avec la direction, on parlait de "
     "l'identité de la marque et de la validation des contenus les plus délicats. Avec le pôle commercial, je "
     "mettais en avant les partenaires et les revendeurs sur les réseaux. Avec l'atelier, je récupérais les "
     "informations produits dont j'avais besoin pour les fiches et les visuels. Et j'étais en contact direct "
     "avec les clients, à qui je répondais par mail et en messagerie sur Instagram et Facebook. Tout cela "
     "était rythmé par des rituels simples : un brief le lundi pour fixer les priorités, un point de suivi "
     "dans la semaine, et un reporting chaque lundi.")

h2('c. Stratégie de communication')
h3('i. Constat initial')
para("Quand je suis arrivée, la marque avait déjà une jolie communauté, mais très déséquilibrée d'un réseau "
     "à l'autre, et une visibilité qui se transformait mal en ventes. La sensibilité de l'image compliquait "
     "encore les choses : il ne suffisait pas de communiquer plus, il fallait communiquer juste. C'est ce "
     "constat qui a fait naître la question du projet : comment développer la visibilité et les ventes en "
     "ligne avec une communication digitale cohérente, sans jamais abîmer une image aussi particulière ?")
h3('ii. Les cibles')
para("La cible principale, c'est le persona dont je parlais plus haut : cette femme de trente à soixante ans, "
     "sensible aux objets qui ont du sens, active sur les réseaux et attachée à l'authenticité. À côté, la "
     "marque vise aussi une cible professionnelle, les revendeurs, mais c'est le pôle commercial qui s'en "
     "occupe.")
h3('iii. Les objectifs')
para("À partir de ces cibles, on m'avait fixé des objectifs clairs, qui m'ont servi de fil rouge toute "
     "l'année.")
bullet("Développer la visibilité et la notoriété de la marque.")
bullet("Augmenter le trafic et les ventes sur le site e-commerce.")
bullet("Élargir l'audience sans diluer ni trahir l'identité de la marque.")
bullet("Renforcer la relation et la fidélité des clients existants.")
h3('iv. L\'audit des réseaux sociaux')
para("Avant de me lancer, j'ai fait un état des lieux chiffré de notre présence en ligne.")
bullet(("Instagram : ", 'b'), "environ 30 000 abonnés, de loin notre plateforme la plus forte.")
bullet(("Facebook : ", 'b'), "près de 3 000 abonnés, une communauté plus modeste.")
bullet(("TikTok : ", 'b'), "seulement 28 abonnés, un compte tout juste lancé, donc tout était à construire.")
bullet(("Emailing : ", 'b'), "une base d'environ 1 200 contacts et des newsletters déjà envoyées "
        "régulièrement, un bon point de départ mais encore à optimiser.")
para("Cet audit confirmait ce que je pressentais : une visibilité très concentrée sur Instagram, et "
     "beaucoup de potentiel encore inexploité, surtout du côté de la vidéo courte sur TikTok et de la "
     "relation client par email.")

h2('d. Élaboration de la stratégie')
h3('i. Inspirations et analyse')
para("Je me suis inspirée des marques de déco et de lifestyle qui marchent bien sur les réseaux. J'ai "
     "regardé leurs formats, leur ton et leur rythme de publication, puis j'ai confronté tout cela à "
     "l'identité de J'ai vu la Vierge pour ne garder que ce qui lui ressemblait vraiment.")
h3('ii. Élaboration')
para("J'ai réfléchi à trois scénarios possibles, que j'ai comparés avant de choisir.")
add_table("Tableau 4 : Comparaison des trois scénarios de stratégie",
    ["Critère", "A : Tout organique", "B : Emailing / CRM", "C : Stratégie mixte"],
    [["Coût", "Faible", "Moyen (abonnement)", "Maîtrisé"],
     ["Cohérence avec l'image", "Très forte", "À surveiller", "Forte et maîtrisée"],
     ["Impact visibilité", "Fort", "Faible", "Fort"],
     ["Impact ventes", "Limité", "Fort", "Fort"]])
para("J'ai retenu le scénario C, la stratégie mixte, parce que c'est le seul qui répond à tous les objectifs "
     "en même temps. Restait la question de l'outil d'emailing : j'ai choisi Kiliba pour son ciblage par "
     "intelligence artificielle et son intégration à Shopify, tout en gardant un studio d'emailing sur mesure "
     "pour les envois les plus soignés.")
h3('iii. Organisation')
para("Pour tout piloter, mon outil central était Trello. J'y planifiais mes tâches en colonnes, façon kanban, "
     "et je suivais chaque contenu de l'idée jusqu'à la publication. Rien ne partait sans validation : chaque "
     "création passait entre les mains de la créatrice et de ma tutrice, ce qui garantissait qu'on restait "
     "toujours fidèle à l'image de la marque.")
h3('iv. Création de contenu')
para("J'ai construit une ligne éditoriale fidèle au ton de la marque, en alternant plusieurs types de "
     "contenus : les contenus produits qui donnent envie, les coulisses qui créent de la proximité, les temps "
     "forts qui font l'événement, et des formats plus spontanés, calés sur les tendances, pour aller chercher "
     "de nouvelles personnes.")
h3('v. Diffusion')
para("Côté diffusion, je suivais un planning, avec une cadence régulière adaptée à chaque plateforme et un "
     "effort concentré sur les temps forts. Les actions se sont mises en place petit à petit sur l'année, "
     "comme le montre le rétroplanning ci-dessous.")
add_table("Tableau 5 : Rétroplanning simplifié des actions sur l'année",
    ["Période", "Phase", "Actions principales"],
    [[("[à préciser]", 'ph'), "Prise en main", "Découverte de la marque, des outils et de la ligne éditoriale."],
     [("[à préciser]", 'ph'), "Montée en autonomie", "Animation régulière des réseaux, contenus et fiches produits."],
     [("[à préciser]", 'ph'), "Temps forts", "Opérations et collaborations, dont Karine Le Marchand."],
     [("[à préciser]", 'ph'), "Emailing", "Mise en place des solutions d'emailing et des premiers modèles."],
     [("[à préciser]", 'ph'), "Optimisation", "Analyse des performances et ajustements."]])
figure_placeholder("Figure 2 : Diagramme de Gantt du projet sur l'année d'alternance")
h3('vi. Outils utilisés')
para("Le projet s'appuyait sur tout un ensemble d'outils : Shopify pour le site, les fiches produits et les "
     "ventes, Odoo pour les revendeurs, Kiliba pour l'emailing automatisé, un studio d'emailing sur mesure "
     "pour les envois premium, Trello pour l'organisation, et les outils d'Instagram, de TikTok et de "
     "Facebook pour programmer et suivre les publications.")
placeholder("ajoutez vos outils de création et de montage vidéo, par exemple Canva, CapCut ou la suite Adobe")
h3('vii. Les différents formats')
para("J'ai utilisé une palette de formats assez large pour capter l'attention à chaque étape : des posts "
     "pour poser l'univers, des carrousels pour raconter, des stories pour l'instantané et l'interaction, et "
     "des vidéos courtes pour la portée.")
lead("Zoom sur les vidéos.", "Les stories et les Reels vidéo ont vraiment été un gros morceau de mon travail. "
     "Ce sont les formats qui touchent le plus de monde en ce moment, et ceux qui permettent d'aller chercher "
     "de nouvelles personnes. Je les imaginais, je les tournais et je les montais moi-même, en m'appuyant sur "
     "les tendances. C'est surtout cela qui a fait décoller la marque sur TikTok, où tout était à construire.")
h3('viii. Indicateurs de performance')
para("Pour piloter tout cela, je suivais des indicateurs à chaque étape du parcours, de la notoriété jusqu'à "
     "la fidélité.")
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
placeholder("commentez vos chiffres réels une fois complétés : ce qui a le mieux marché et pourquoi")

h2('e. Les différentes missions')
para("Au delà de la stratégie, mon année s'est surtout traduite par des missions concrètes, tous les jours. "
     "Les voici en détail.")
h3('i. Animation des réseaux sociaux')
para("J'animais au quotidien les comptes Instagram, TikTok et Facebook. Cela voulait dire programmer et "
     "publier les contenus, bien sûr, mais aussi tout le travail de communauté : répondre aux commentaires "
     "et aux messages, garder le lien avec les abonnés, faire remonter ce qu'ils disaient. C'est ce travail "
     "de tous les jours qui fait qu'une marque reste vivante.")
h3('ii. Stories et Reels vidéo')
para("La création de stories et de Reels vidéo a pris une grande place dans mes journées. J'avais les idées, "
     "je tournais, je montais, en m'inspirant des tendances tout en restant fidèle à l'univers de la marque. "
     "J'ai beaucoup misé sur ce format court, parce que c'est celui qui rapporte le plus de visibilité et qui "
     "nous a fait connaître de nouvelles personnes, surtout sur TikTok.")
h3('iii. Shootings et création visuelle')
para("Je participais aux shootings produits et je préparais les visuels, en soignant la mise en scène et la "
     "cohérence avec la marque. Ensuite, chaque visuel était décliné selon les codes de chaque plateforme, "
     "pour être toujours au bon format, au bon endroit.")
h3('iv. Fiches produits et site e-commerce')
para("Je m'occupais aussi de la mise à jour du site et de la rédaction des fiches produits. Là, l'enjeu était "
     "double : présenter chaque produit de façon claire et donner envie de l'acheter, mais aussi soigner les "
     "textes pour servir à la fois l'image de la marque et le référencement du site.")
h3('v. Emailing et newsletters')
para("Je participais à la création et à l'envoi des campagnes email et des newsletters adressées à notre base "
     "de contacts. C'est un canal que la marque maîtrise complètement, et il servait à garder le lien avec "
     "les clients, à annoncer les nouveautés et les temps forts, et à soutenir les ventes du site.")
h3('vi. Reporting et suivi des performances')
para("Enfin, chaque semaine, je faisais un reporting des performances, en suivant les chiffres des réseaux, "
     "du site et de l'emailing. C'est une mission qui m'a appris à mesurer l'impact réel de ce que je "
     "faisais, à en tirer des leçons et à ajuster la suite.")

h2('f. Retour d\'expérience')
para("La plus grosse difficulté, cela a été la sensibilité de l'image de la marque. L'hésitation de "
     "l'Olympique de Marseille m'a bien fait comprendre qu'il fallait communiquer avec beaucoup de tact. Une "
     "autre difficulté, plus quotidienne, a été d'apprendre à jongler entre des tâches très différentes dans "
     "une même journée. Au début, cela me dispersait un peu, et c'est l'organisation et les rituels de la "
     "semaine qui m'ont aidée à tenir le cap.")
placeholder("ajoutez si vous le souhaitez une ou deux autres difficultés concrètes rencontrées")
para("Ma valeur ajoutée, je la vois surtout dans trois choses : avoir apporté à la marque une animation "
     "digitale régulière et cohérente, avoir participé à des temps forts comme la collaboration avec Karine "
     "Le Marchand, qui a généré plus de cinquante ventes avec une seule story, et avoir fait décoller des "
     "canaux encore peu exploités comme TikTok et l'emailing. Si je devais m'améliorer, je m'attaquerais plus "
     "tôt à l'emailing et à la collecte des données clients, et je mettrais en place dès le début un vrai "
     "tableau de suivi des indicateurs.")
pb()

# ================= 3. CONCLUSION
h1('3. Conclusion')
h2('a. Synthèse')
para("Pendant mon alternance chez J'ai vu la Vierge, j'ai piloté la stratégie de communication digitale "
     "d'une marque à l'identité forte et sensible. Au départ, la visibilité était concentrée sur Instagram et "
     "se transformait mal en ventes. J'ai animé au quotidien Instagram, TikTok et Facebook, produit les "
     "contenus, les stories, les Reels et les fiches produits, participé à l'emailing et assuré le reporting. "
     "J'ai comparé plusieurs scénarios avant de choisir une stratégie mixte, et j'ai participé à des "
     "opérations marquantes comme la collaboration avec Karine Le Marchand, qui a rapporté plus de cinquante "
     "ventes à partir d'une seule story. En lisant simplement cette synthèse, on comprend l'essentiel de ce "
     "que j'ai fait et de ce que cela a donné.")
h2('b. Bilan')
para(("Quelles compétences ai-je développées ? ", 'b'),
     "J'ai appris à piloter un projet de communication digitale, en planifiant et en coordonnant les tâches "
     "avec Trello et un circuit de validation. J'ai développé ma capacité à animer des réseaux sociaux et à "
     "créer des contenus, en particulier des stories et des Reels vidéo pensés pour chaque plateforme. J'ai "
     "gagné en aisance sur l'analyse des performances, en suivant des indicateurs et en faisant un reporting "
     "chaque semaine. Et j'ai acquis des compétences e-commerce très concrètes avec Shopify et Odoo.")
para(("Qu'ai-je appris en termes de savoir-être et de posture professionnelle ? ", 'b'),
     "C'est surtout en autonomie que j'ai le plus grandi. Au début, dès qu'il fallait répondre à un "
     "commentaire négatif, je demandais de l'aide, parce que ce n'était pas évident. Petit à petit, j'ai "
     "appris à gérer ces messages toute seule, en gardant le bon ton. Le reporting aussi m'impressionnait, et "
     "je l'appréhendais chaque semaine, mais à force de le faire, j'ai fini par être à l'aise pour présenter "
     "et défendre mon travail. J'ai aussi appris à décider seule quand il le fallait et à proposer mes "
     "propres idées. Ce sont tous ces petits pas, semaine après semaine, qui m'ont fait passer d'une posture "
     "d'exécutante à une posture de cheffe de projet.")
para(("Mon projet professionnel s'est-il conforté, a-t-il évolué ou est-il remis en question ? ", 'b'),
     "Cette expérience a vraiment conforté mon projet. Elle m'a fait découvrir le e-commerce, un domaine qui "
     "me passionne aujourd'hui, et elle m'a donné le goût et la confiance de piloter des projets. Après mon "
     "Bachelor, je veux continuer en mastère pour approfondir tout cela, et à terme piloter des projets "
     "digitaux plus ambitieux.")
pb()

# ================= 4. BIBLIOGRAPHIE
h1('4. Bibliographie')
for src in [
    "Site officiel de la marque : www.jaivulavierge.com",
    "Comptes Instagram, TikTok et Facebook de J'ai vu la Vierge",
    "Documentation en ligne de Shopify et de Kiliba",
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

doc.core_properties.title = "Dossier BC3 - Estelle CASTEROT"
doc.core_properties.author = "Estelle CASTEROT"
out = "/home/user/newsletter_ynov/dossier-bc3/Dossier_BC3_EEMI_Estelle_CASTEROT.docx"
doc.save(out)
print("OK ->", out)
