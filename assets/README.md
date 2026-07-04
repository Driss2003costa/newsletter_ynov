# Assets du diaporama Bridgerton

Ressources utilisees par `generer_diaporama_bridgerton.py`.

## fonts/
Polices embarquees dans le `.pptx` (deux familles) :
- **Playfair Display** (titres, chiffres) : serif Didone a fort contraste.
- **EB Garamond** (corps) : serif classique.

Les deux sont sous licence **SIL Open Font License 1.1** (libre d'usage,
d'embarquement et de redistribution). Fichiers TTF fournis pour installation
manuelle si un lecteur ignore l'embarquement OOXML.

## ornaments/
Ornements vectoriels rendus en PNG a fond transparent (glycine, cachets de
cire, fleurons d'angle, rosette, abeille, filet). Generes par
`ornaments_generator.py` (SVG puis rasterisation). Utilises via `add_picture`
comme petites formes decoratives, jamais en image plaquee plein cadre.
