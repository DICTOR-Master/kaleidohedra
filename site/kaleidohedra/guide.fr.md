# Guide de l'utilisateur de Kaleidohedra

Kaleidohedra, par DICTO, est le troisième frère de [Rhombiverse](https://rhombiverse.vercel.app) et [Polyhedraverse](https://polyhedraverse.vercel.app). Rhombiverse est le **paysage** : les réseaux eux-mêmes, qui s'étendent dans toutes les directions. Polyhedraverse est la **galerie de portraits** : les formes qui vivent dans ces réseaux, une à une, de près. Kaleidohedra **fait bouger le paysage** : vous pouvez cisailler et faire glisser tout le réseau, et chaque pièce bouge avec lui. Il s'en tient aux mondes où cela a un sens : les réseaux 3D+, ses mondes à lui (Euclid–Kepler–Pacioli Cell Network, Targets, Couches et Rhomboèdres dorés) et les Patrons, le passage des patrons plats à la 3D. Les mondes 1D et 4D à 6D sont dans Rhombiverse.

Ici, chaque pièce remplit parfaitement l'espace sur un vrai réseau cristallin : vous ne pouvez donc poser une pièce que là où le réseau a de la place. Touchez pour ajouter une pièce, appuyez longuement pour en retirer une, et regardez votre construction sous différentes vues.

La première partie de ce guide présente les tâches courantes. La seconde liste toutes les commandes.

Les noms des boutons sont écrits tels qu'ils apparaissent dans l'application (ceux que l'application ne traduit pas encore restent en anglais).

## Cisailler le réseau

Les commandes propres à Kaleidohedra sont dans le panneau **⟋ Shear**, en haut à droite. Elles déplacent tout le réseau d'un coup : tout ce que vous avez construit glisse avec lui, et la construction continue comme d'habitude.

- **↺ Reset to FCC** ramène tout au réseau FCC ordinaire et à son dodécaèdre rhombique régulier, si vous vous perdez.
- **Towards** choisit où va le réseau : **DICTO FCC** (du réseau FCC ordinaire au réseau cisaillé de DICTO) ou **Bain (BCC → FCC)**.
- **Path** fait glisser le long de ce chemin exact ; les boutons d'arrêt (comme FCC, halfway et DICTO FCC) sautent à ses points nommés.
- **Cell** change la forme de la cellule sur le même réseau : 0 est la cellule simplement cisaillée, 1 la cellule aux arêtes toutes égales (à l'arrêt DICTO FCC, le dodécaèdre rhombique incliné de DICTO). Une **bande rouge** sous le curseur Path marque où, pour cette valeur de Cell, la cellule ne remplit plus l'espace (près des extrémités du chemin) ; l'affichage l'indique aussi. Cell 0 remplit toujours l'espace.
- La jauge **Regularity** note la cellule par ses angles (1 signifie que tous les angles sont spéciaux : 36, 45, 60, 70,5, 72 ou 90°). Sur le chemin de Bain, elle compte aussi combien de ses disphénoïdes sont des tétraèdres réguliers.
- **◀ Find** et **Find ▶** sautent le long du chemin vers la cellule la plus régulière suivante, ou le prochain moment où apparaît un hexagone régulier. Touchez d'abord un arrêt.
- **Six sliders** règle directement les longueurs a, b, c et les angles α, β, γ du réseau.
- **Export member** enregistre l'état actuel sous le nom de votre choix, en petit fichier JSON (un membre de la population).
- **☆ Garder** garde l'état actuel dans votre propre liste **Gardés**, dans ce navigateur seulement. Elle enregistre l'ID de l'état et une empreinte, jamais la forme elle-même : **Ouvrir** la régénère à partir de l'ID, et une marque indique si elle est revenue identique (✓), si l'appli fait maintenant une autre forme pour cet état (⚠) ou si elle ne peut plus être faite (✗). **Copier l'ID** copie l'ID, à envoyer à DICTO si vous pensez qu'il a sa place dans le registre.

Dans Euclid–Kepler–Pacioli Cell Network, le panneau Shear ne déplace que le réseau : les centres des cellules glissent, et chaque pièce reste un solide régulier. Il se masque dans Targets, où le cisaillement changerait les angles. Les découvertes de Kaleidohedra, et la façon dont chacune est vérifiée, sont dans [DISCOVERIES.md](https://github.com/DICTOR-Master/kaleidohedra/blob/master/DISCOVERIES.md).

## Premiers pas

### Choisir une dimension

Après **ENTER**, le sélecteur de dimension s'ouvre : une forme qui tourne lentement et dont les faces sont **2D+** et **3D+**. Touchez **3D+** pour construire sur les réseaux, ou **2D+** pour plier des patrons plats en solides (Patrons). Faites glisser pour tourner la forme. Les boutons **3D+**, **EKP** et **Targets** de l'écran d'accueil y mènent directement.

Vous pouvez changer plus tard depuis **Menu → Change Dimension**, ou depuis le **Wizard** (en haut à gauche) : **3D+** présente chaque réseau avec ses pièces en fils de fer qui tournent, ainsi que les mondes propres à Kaleidohedra, et **2D+** ouvre les Patrons.

### Poser votre première pièce

Un monde vide affiche un **contour orange** là où va la première pièce. Touchez-le. Touchez ensuite une face de n'importe quelle pièce pour ajouter une voisine de l'autre côté.

On construit une pièce à la fois. En 3D+, le **RD** (dodécaèdre rhombique) est sélectionné au départ. La pièce que vous posez est affichée sur le bouton **Shape**, en bas à gauche ; touchez-le pour en choisir une autre.

### Retirer une pièce

- **Téléphone ou tablette :** appuyez longuement sur la pièce.
- **Souris :** faites un clic droit sur la pièce. Le clic droit retire dans tous les modes.

Pour annuler votre dernière modification, touchez **Undo** (↶, en bas à droite). Maintenez-le pour revenir plusieurs étapes en arrière d'un coup. Chaque dimension a son propre historique : annuler dans les Patrons ne touche jamais votre construction 3D+.

### Déplacer la caméra

- **Tourner :** faites glisser un doigt, ou faites glisser avec le bouton gauche de la souris.
- **Zoomer :** pincez, ou utilisez la molette.
- **Déplacer :** faites glisser deux doigts.

## Choisir quoi construire

### Les pièces, par réseau

**Patrons 2D** (Wizard → 2D+) : de la 2D à la 3D. Choisissez un solide dans le panneau : les **cellules de Voronoï**, cube, RD et TO (octaèdre tronqué), les cellules qui pavent l'espace des réseaux cubiques simple, à faces centrées et centré ; son patron apparaît comme un fantôme pâle. Suivez-le : touchez pour construire la première face côté par côté, en cellules 1D, puis chaque toucher construit la face suivante. Quand le patron est complet, touchez et il se plie en solide (l'indicateur affiche **2D+/3D+**) ; le **curseur de pliage** le plie et le déplie à la main, et **Ouvrir en 3D+** y emmène le solide terminé. Un appui long retire une face (ou déplie). Chaque solide garde sa propre progression. Les **solides de Platon** forment un second groupe : tétraèdre, octaèdre, icosaèdre, dodécaèdre et le cube. **Ouvrir en 3D+** apparaît pour les solides que le monde 3D+ a comme pièces (cube, RD, TO, octaèdre). **⊘** à côté d'Undo efface le patron en cours.

**Peindre** (3D+) : le pinceau de la rangée du bas, ou l'interrupteur Peindre au centre de la roue des couleurs, recolore les pièces déjà posées. Activez-le, choisissez une couleur, touchez une pièce ; désactivez-le pour reconstruire. Il passe les couleurs en Choisir, pour que chaque pièce montre sa propre couleur. (Couches, Rhomboèdres dorés, EKP et Targets colorent leurs pièces à leur façon, donc Peindre n'y est pas proposé, ni dans les Patrons.) Quand l'emplacement de la rangée du bas est pris par un sélecteur d'assemblage (Rhombohedra et Pyrochlore), le pinceau se place juste au-dessus.

**3D+ :**

| Réseau | Pièces |
|---|---|
| FCC | Rhombic Dodecahedron (RD, dodécaèdre rhombique), Hemi RD, Hourglass, RD Quarter, Cube, Pyramid |
| DICTO FCC | DICTO RD : le dodécaèdre rhombique oblique de DICTO en tiges bleues Zometool (six losanges de 60° et six de 72°, volume φ² pour une arête de 1), empilé en FCC cisaillé ; DICTO Blocks : ses quatre blocs, deux blocs tout en losanges et deux rhomboèdres aplatis, face contre face |
| RD Dual | Cuboctahedron (CO, cuboctaèdre), Octahedron (octaèdre) |
| BCC | Truncated Octahedron (TO, octaèdre tronqué) |
| BCC Interstitial | Flattened Octahedron, Disphenoid |
| Elongated Dodecahedron | Elongated Dodecahedron (ED, dodécaèdre allongé) |
| Hexagonal | Hex Prism (prisme hexagonal) |
| Rhombohedral | Rhombohedra (rhomboèdres) |
| Pyrochlore (Kagome 3D) | Truncated Tetrahedron (tétraèdre tronqué ; les tétraèdres entre eux sont ajoutés pour vous) |

Essayez ceci en FCC : posez six Pyramid pour former un Cube. Ajoutez ensuite une Pyramid sur chaque face du Cube : il devient un RD. Retirez de nouveau ces six-là pour revenir à un Cube.

**RD Quarter** est l'un des 4 rhomboèdres en lesquels se découpe un RD. Touchez un RD près d'un de ses coins pour remplir ce coin, puis touchez une face d'un quart pour poser son image miroir de l'autre côté de cette face. L'image miroir retombe toujours sur le réseau RD : vous pouvez donc faire croître les quarts de cellule en cellule. Pour un réseau libre de rhomboèdres avec Copy (copie) en plus de Mirror (miroir), utilisez **Rhombohedra**.

### Couleurs

Les pièces sont colorées selon le réglage **Couleurs** (dans Réglages) : **Cyan** (toutes cyan, par défaut), **Type** (chaque type de pièce dans sa couleur, modifiable dans la liste affichée) ou **Choisir** (chaque pièce garde la couleur avec laquelle elle a été posée). Touchez le **bouton de couleur** (en bas à gauche) pour choisir parmi 15 couleurs : en Cyan, cela passe à Choisir ; en Type, cela change la couleur du type de pièce que vous posez. Changer de mode ne perd jamais les couleurs de pose.

## Regarder votre construction

| Vue | Ce qu'elle montre | Comment l'activer |
|---|---|---|
| World View | Couleur, Translucide ou Squelette | Touchez le bouton World View pour alterner |
| Lattice View | Votre construction et chaque emplacement libre un cran plus loin, pour la pièce choisie | Touchez le bouton Lattice View pour parcourir les pièces |
| X-Ray | Une coupe. Faites glisser le plan à travers la structure, y compris en diagonale | Bouton X-Ray (⛶) |
| Spherical | Touchez pour alterner : chaque pièce en sphère (les RD entiers touchent leurs douze voisins), puis les vides entre RD entiers (octaédriques en or, tétraédriques en rose, seulement là où ils sont fermés), toutes les sphères rendues pâles. Un curseur règle la taille de toutes les sphères (cran à la taille propre de chaque forme ; en dessous = écartées, au-delà = qui se chevauchent). Avec Lattice View activé, chaque place libre du réseau apparaît comme une sphère pâle. Une vue seulement | Bouton Spherical (◯) : éteint → sphères → vides |
| Duality | Le pavage apériodique que projette cette structure cristalline | Bouton Duality (◐) |
| Dualize | Échange FCC et BCC | Paramètres → Dualize Preview |

Paramètres propose aussi une **Vue en coupe** : choisissez un axe, faites glisser le curseur pour déplacer la coupe, et cochez **Retourner** pour voir l'autre côté.

## Couches

Un monde 3D pour construire des **enveloppes** : des couches de dodécaèdres rhombiques (RD), chaque couche avec sa bande de couleur, comptées depuis votre première pièce. Choisissez-le dans l'écran 3D+ du Wizard.

- **+ Couche** remplit la couche suivante, **− Couche** retire la plus extérieure. **Enveloppe** choisit comment les couches se comptent : **Pas** (un cuboctaèdre : 13, 55, 147 … pièces), **Distance** (vers une sphère), ou une forme cible (tétraèdre, cube, octaèdre, RD ou octaèdre tronqué). **Rogner** coupe l'enveloppe exactement à plat selon cette forme.
- Mode **Fragmenter** : touchez une pièce, puis choisissez une **Découpe** (moitiés, tiers, quarts, sixièmes, huitièmes, douzièmes, seizièmes, vingt-quatrièmes ou quarante-huitièmes) ; **Tourner** change la coupe. En mode Construire, le menu **Pièce** pose aussi des parties seules.
- **Échelle** construit avec des RD plus grands (×2 à ×4). **Fusionner ×2 / ×3** sur une pièce ciblée montre le contour du grand RD, puis **Confirmer la fusion** le met en place ; le menu Découpe le rouvre.
- **Infos** montre le diagramme d'anneaux : touchez un anneau pour masquer ou afficher cette couche et voir l'intérieur, retirez n'importe quelle couche et choisissez les couleurs des bandes.

## Rhomboèdres dorés

Un monde 3D avec les deux pièces du pavage de Penrose en 3D. Choisissez-le dans l'écran 3D+ du Wizard. Touchez le contour orange, puis une face pour ajouter la pièce **Allongée** ou **Aplatie** choisie dans le menu Pièce. Le **Contrôle Penrose** colore en vert les pièces qui appartiennent au vrai pavage apériodique et en rouge celles qui s'en écartent ; Lattice View montre le vrai pavage autour, et toucher un fantôme le pose.

Ces deux blocs sont aussi les pièces de **RHOMBITURE** de DICTO, un système d'armature extractible pour la taille et le modelage : [doi:10.5281/zenodo.23173896](https://doi.org/10.5281/zenodo.23173896).

## Euclid–Kepler–Pacioli Cell Network (EKP)

Un monde 3D sur une seule cellule exacte. Posez les toits d'Euclide sur un cube et vous obtenez un dodécaèdre régulier ; repliez les toits vers l'intérieur à travers les faces du cube et ils forment un icosaèdre régulier. Les arêtes du cube, du dodécaèdre et de l'icosaèdre sont dans le rapport φ² : φ : 1. Choisissez-le dans l'écran 3D+ de l'Assistant. Touchez le contour orange, choisissez une **Pièce** (cube, dodécaèdre, icosaèdre, grand dodécaèdre étoilé, octaèdre, stella octangula ou rectangles d'or) et touchez un solide : la pièce va dans cette cellule si elle n'y est pas encore, sinon dans la cellule suivante de l'autre côté de la face touchée. Les petits solides se logent dans les grands : utilisez **Rayons X** ou la vue translucide pour les voir. **Vue** redessine la même construction : deux solides en alternance selon un **Motif**, un damier, ou la surface extérieure fusionnée de tous les dodécaèdres. **Sommets** marque les coins du cube ou tous les sommets, et **Infos** donne le groupe d'espace (Pm-3 pour la cellule ; chaque motif a le sien). En faisant croître des dodécaèdres par leurs faces, on n'atteint que les cellules de même couleur dans le motif diagonal ; passez par une face du cube pour atteindre les autres. **Tourner les cubes impairs** fait tourner chaque pièce de chaque cube impair d'un quart de tour autour de l'axe vertical, de sorte que les cubes voisins alternent. Elle s'applique aussi à la surface extérieure fusionnée.

Trois de ces pièces complètent un hommage à Kepler : l'**octaèdre** sur les centres des faces du cube, avec les sommets de l'icosaèdre sur ses arêtes à la section dorée ; la **stella octangula**, deux tétraèdres réguliers sur des sommets alternés du cube qui se recouvrent dans cet octaèdre ; et les trois **rectangles d'or** entrelacés de Pacioli, qui sont exactement là où se rencontrent les faîtes des toits des cellules voisines. Ensemble, les cinq solides de Platon s'emboîtent dans une seule cellule : icosaèdre, octaèdre, tétraèdres, cube, dodécaèdre.

Le **Dogstar** est aussi une pièce, entre l'octaèdre et la stella octangula dans l'ordre d'emballage : le creux que laissent les dodécaèdres réguliers dans leur empilement le plus dense (la stellation 8 du dodécaèdre de George W. Hart, 1996), à l'intérieur de la stella et contenant le dodécaèdre de la cellule suivante, 1/φ³ fois plus petit. Dans 2D+ → Patrons, il se déplie en un seul patron de 60 triangles. **Dodécaèdre / Dogstar** remplit les creux de la façon habituelle : des dodécaèdres sur les cellules paires et des Dogstars dans les creux entre eux, le pavage du Sunstar Lattice.

La cellule de ce monde est la **cellule Euclid–Kepler–Pacioli**, et les grands dodécaèdres étoilés et icosaèdres qui ne se touchent que par les sommets forment le **réseau Euclid–Kepler–Pacioli**, tous deux de DICTO. À citer comme [doi:10.5281/zenodo.23173809](https://doi.org/10.5281/zenodo.23173809).

## Études

Un monde 3D+ de constructions exactes sur la cellule Euclid–Kepler–Pacioli, une à la fois (Wizard → 3D+ → Studies). Choisissez une **Étude** : **Fenêtres** (le dodécaèdre creusé des stellas octangulas de ses six voisins par une face, ce qui laisse 12 losanges épais de Penrose aux angles mêmes des faces du dodécaèdre), **Fenêtres, avec les six stellas**, **Dodécaèdres et leurs Dogstars** (les dodécaèdres réguliers des cellules paires laissent un trou dans chaque cellule impaire : le Dogstar, une étoile à 8 pointes, stellation partielle d'un dodécaèdre 1/φ³ fois plus petit, à l'intérieur de la stella octangula de la cellule ; ensemble ils remplissent l'espace, et **Écarter** les sépare), **Fenêtres et stellas, en damier** (la stella octangula est l'autre moitié des fenêtres : fenêtres dans les cellules paires et stellas dans les impaires remplissent exactement l'espace, 12 + 4 = deux cubes ; le curseur **Écarter** les sépare pour les voir s'emboîter), **Fenêtres rendues convexes** (chaque losange poussé droit vers l'extérieur ; le curseur **Poussée** s'arrête au point doré, où 6 losanges d'or apparaissent, 74 faces en tout), **Des fenêtres à l'icosidodécaèdre** et **Des fenêtres au dodécaèdre rhombique** (le curseur **Métamorphose** amène les losanges à chacun ; l'enveloppe est dessinée opaque, les losanges incrustés, leurs contours visibles à travers elle en chemin) et **Dodécaèdre étiré** (8 pentagones, 4 hexagones et 2 rectangles ; le curseur **Étirer** s'arrête à une arête, où les rectangles sont des carrés, et au pas du réseau). Les études se cisaillent aussi : en copies exactes sur le réseau ou, d'une touche, comme le solide lui-même.

## Stella–Jewel Lattice

Un monde 3D+ (Wizard → 3D+ → Stella–Jewel Lattice) de deux pièces qui remplissent l'espace ensemble en damier : le **Dragon Jewel** (DJ, le nom donné par DICTO au solide des fenêtres du monde Studies) dans les cellules paires et la **stella octangula** dans les impaires. Touchez le Dragon Jewel cyan pour le poser, puis touchez une face pour ajouter la pièce de l'autre côté ; appui long pour retirer. **Vue** bascule entre les deux pièces et **Dragon Jewels seuls**, accolés face à face par leurs 12 losanges, qui laissent des trous en forme de stella. **Cisaillement** fonctionne comme dans Studies : copies exactes sur les centres qui bougent, ou tout l'empilement plié. **Axes d'ordre cinq** trace les six axes d'ordre cinq de chaque Dragon Jewel et, sur chaque face, les cinq places possibles d'une fenêtre, celle que choisit le cube en clair. Lattice View montre les cellules vides à remplir. **Chaîne du dragon** montre dans chaque Dragon Jewel la chaîne qui s'y emboîte, chaque étape se touchant : son cube, sa stella octangula, un Dogstar, le dodécaèdre cœur du Dogstar (1/φ³) et le Dragon Jewel suivant, 1/φ³ fois plus petit.

## Sunstar Lattice

Un monde 3D+ (Wizard → 3D+ → Sunstar Lattice) de dodécaèdres réguliers dans leur empilement en réseau le plus dense sur les cellules paires et, dans chaque trou qu'ils laissent sur les impaires, un **Dogstar** : une étoile à 8 pointes, exactement une stellation partielle d'un dodécaèdre 1/φ³ fois plus petit, aux arêtes toutes dorées. Un dodécaèdre entouré de ses Dogstars est un **Sunstar**, le soleil et ses parhélies (noms de DICTO). Touchez le dodécaèdre cyan pour le poser, puis une face pour ajouter la pièce de l'autre côté ; appui long pour retirer. **Vue** montre les deux, les **Dogstars seuls** (ils partagent leurs sommets, quatre à chaque coin du cube, comme un Kagome 3D ; une touche ajoute le Dogstar le plus proche partageant un point) ou les **dodécaèdres seuls**. **Cisaillement** et **Axes d'ordre cinq** fonctionnent comme dans Stella–Jewel Lattice. **Sunstars entiers** ajoute et retire un dodécaèdre avec les 6 Dogstars de ses faces (un Dogstar qu'un autre Sunstar possède encore reste). **Dogstars dans chaque cellule** place aussi un Dogstar dans chaque dodécaèdre (il y tient entier : Dogstar dans la stella, dans le cube, dans le dodécaèdre), les dodécaèdres transparents ; les Dogstars occupent alors toutes les cellules, huit pointes se rejoignant à chaque coin du cube. **Réaction en chaîne stellaire** (nom donné par DICTO, comme la réaction en chaîne du Soleil) montre dans chaque dodécaèdre la chaîne qui s'y emboîte exactement, chaque étape se touchant : sa grande étoile (le grand dodécaèdre étoilé du cœur du Dogstar), dedans un Sunstar entier 1/φ³ fois plus petit, dans son dodécaèdre la grande étoile suivante, et un Sunstar 1/φ⁶. Le Dogstar est la stellation 8 du dodécaèdre de George W. Hart (1996), qui a noté qu'il remplit l'espace en alternance avec des dodécaèdres réguliers ; Polyhedra-World le montre aussi.

## Targets

Une galerie 3D des 160 cellules cibles : toute cellule qui remplit l'espace, à arêtes toutes égales, dont les arêtes ne se rencontrent qu'à des angles particuliers (36°, 45°, 60°, 70,53°, 72° et 90°), trouvées par une recherche exacte menée de deux façons (voir [TARGETS.md](https://github.com/DICTOR-Master/kaleidohedra/blob/master/TARGETS.md)). Choisissez-le dans l'écran 3D+ de l'Assistant. Choisissez un **Type** (parallélépipède, prisme hexagonal, dodécaèdre rhombique, dodécaèdre allongé ou octaèdre tronqué) et une cellule, ou parcourez-les avec ◀ ▶. Chacune est nommée par son type, son numéro dans TARGETS.md et ses angles ; ✓ marque celles déjà dans Polyhedraverse. **Afficher** dessine la cellule seule, avec ses voisines par les faces, ou en bloc 3×3×3 de son réseau, pour la voir remplir l'espace. Les faces sont colorées par sorte : carrés en bleu, losanges en rose, hexagones réguliers en or, autres hexagones en violet. **Info** donne ses faces, les angles entre ses directions d'arêtes, son volume (arête 1), le réseau selon lequel elle pave, et si elle est déjà dans Polyhedraverse. Rien ne se construit ici, et le panneau Shear se cache pour que les angles restent exacts.

## Enregistrer votre travail

Votre monde est enregistré automatiquement dans ce navigateur, pour toutes les dimensions, après chaque modification. Il revient quand vous rouvrez le site sur le même appareil et le même navigateur.

Dans **Paramètres** :

- **Exporter le Monde** enregistre tout, chaque réseau et monde 3D+ et vos patrons, dans un seul fichier. Utilisez-le pour garder une sauvegarde ou transférer votre monde sur un autre appareil.
- **Importer un Monde** ouvre un fichier exporté. **Undo** annule une importation.
- **Clear World** (⊘, en haut à droite) recommence avec un monde vide. Undo peut le rétablir.

## Découvrir les mathématiques

- **Almanac :** les mathématiques et la géométrie derrière chaque pièce et chaque réseau. Ouvrez-le depuis Menu → Almanac.
- **What's New** liste les changements récents.

---

# Référence des commandes

## Boutons à l'écran

| Commande | Ce qu'elle fait |
|---|---|
| DICTO (en haut à gauche) | L'assistant : l'appli par laquelle vous êtes entré, les deux autres (Kaleidohedra, Rhombiverse, Polyhedraverse) à un grand bouton près. Le grand libellé à côté indique la dimension où vous êtes |
| Shape (en bas à gauche) | La pièce que vous posez. Touchez pour la changer |
| Couleur (en bas à gauche) | Couleur de construction. Touchez pour la changer |
| Lattice View | Alterne entre Off et une vue pour chaque pièce |
| Choix d'assemblage | Affiché seulement pour les pièces qui s'assemblent de plusieurs façons (Rhombohedra : Copie / Miroir ; Pyrochlore : petit / tétraèdre entier) : touchez pour changer |
| Undo (↶, en bas à droite) | Touchez pour annuler une étape dans la dimension actuelle. Maintenez pour remonter plus loin |
| Paint (pinceau) | Recolorer des pièces posées : activez, choisissez une couleur, touchez une pièce. À la place du sélecteur d'assemblage dans la rangée du bas ; quand ce sélecteur est nécessaire, il se place juste au-dessus |
| ⊘ Effacer (à côté d'Undo, Patrons) | Efface le patron en cours pour recommencer ; Undo le rétablit |
| Menu | Ouvre l'assistant DICTO (clavier : Tab ou Espace) |

## Outils (en haut à droite)

Une colonne de boutons dans le coin supérieur droit, de la couleur de l'appli dans l'espace de laquelle vous êtes.

| Bouton | Commande |
|---|---|
| ⚙ | Réglages |
| 3D / ∥ / ISO | Projection : perspective, parallèle (orthographique) ou isométrique (touchez pour changer) |
| ⛶ | X-Ray |
| ◐ | Duality |
| ◯ | Spherical (éteint → sphères → vides) |
| ⊘ | Clear World |
| ↻ | Recharger (si quelque chose semble bloqué) |

## Assistant DICTO

**DICTO** (en haut à gauche) ouvre l'assistant en plein écran. Il s'ouvre sur l'appli par laquelle vous êtes entré, avec ses dimensions et ses mondes dans sa couleur. Les deux autres applis sont les deux grands boutons en haut : touchez-en un pour parcourir sa liste, dans sa couleur. Choisir quoi que ce soit vous fait entrer dans l'espace de cette appli : ses couleurs et ses outils (le Shear de Kaleidohedra n'apparaît que là). Polyhedraverse ouvre pour l'instant son propre site.

## Paramètres

| Paramètre | Ce qu'il fait |
|---|---|
| Sensibilité de la vue | Vitesse de rotation de la caméra |
| Inverser l'axe Y | Inverse le glissement vertical |
| Champ de vision | Largeur de l'objectif de la caméra |
| Qualité graphique | Basse, Moyenne ou Haute |
| Afficher le compteur de FPS | Compteur d'images par seconde |
| Volume | Niveau sonore |
| Langue | English, 日本語, Español, Français, 한국어, 中文, Русский (aussi avec le sélecteur 🌐 en haut de l'écran d'accueil et de ce guide) |
| Couleurs | Cyan, Type ou Choisir : la coloration des pièces |
| Vue en coupe, axe, position, Retourner | Coupe le long d'un axe |
| Dualize Preview | Mode de construction spécial |
| Exporter le Monde, Importer un Monde | Sauvegarder et restaurer (toutes les dimensions) |

## Clavier et souris

| Entrée | Action |
|---|---|
| Clic gauche sur une face | Ajouter une pièce |
| Clic droit sur une pièce | La retirer |
| Glisser avec le bouton gauche | Tourner la caméra |
| Molette | Zoomer |
| Tab ou Espace | Ouvrir l'assistant DICTO |
| Échap | Fermer le menu, le Wizard ou l'Almanac |
| Entrée | Entrer depuis l'écran d'accueil |

## Tactile

| Geste | Action |
|---|---|
| Toucher une face | Ajouter une pièce |
| Appui long sur une pièce | La retirer |
| Glisser un doigt | Tourner la caméra |
| Pincer | Zoomer |
| Glisser deux doigts | Déplacer |
