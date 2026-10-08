# Kaleidohedra User Guide

Kaleidohedra by DICTO is the third sibling of [Rhombiverse](https://rhombiverse.vercel.app) and [Polyhedraverse](https://polyhedraverse.vercel.app). Rhombiverse is the **landscape**: the lattices themselves, stretching out in every direction. Polyhedraverse is the **portrait gallery**: the shapes that live in those lattices, one at a time, up close. Kaleidohedra **moves the landscape**: you can shear and slide the whole lattice, and every piece moves with it. It keeps to the worlds where that means something: the 3D+ lattices, its own worlds (Euclid–Kepler–Pacioli Cell Network, Targets, Shells and Golden Rhombohedra) and Nets, the way from flat nets into 3D. The 1D and 4D to 6D worlds live in Rhombiverse.

Here, every piece fills space perfectly on a real crystal lattice, so you can only put a piece where the lattice has room for it. Tap to add a piece, long-press to remove one, and look at what you've built in different views.

The first part of this guide walks through common tasks. The second part lists every control.

## Shearing the lattice

Kaleidohedra's own controls are in the **⟋ Shear** panel at the top right. They move the whole lattice at once: everything you've built slides with it, and building carries on as usual.

- **↺ Reset to FCC** takes everything back to the ordinary FCC lattice with its regular rhombic dodecahedron, if you lose your way.
- **Towards** picks where the lattice is heading: **DICTO FCC** (from the ordinary FCC lattice to DICTO's sheared one) or **Bain (BCC → FCC)**.
- **Path** slides along that exact route; the stop buttons (such as FCC, halfway and DICTO FCC) jump to its named points.
- **Cell** changes the cell's shape on the same lattice: 0 is the plain sheared cell, 1 the cell with all edges equal (at the DICTO FCC stop, DICTO's skewed rhombic dodecahedron).
- The **Regularity** meter scores the cell by its angles (1 means every angle is special: 36, 45, 60, 70.5, 72 or 90°). On the Bain path it also counts how many of its disphenoids are regular tetrahedra.
- **◀ Find** and **Find ▶** jump along the path to the next most regular cell or the next moment a regular hexagon appears. Tap a stop first.
- **Six sliders** set the lattice's lengths a, b, c and angles α, β, γ directly.
- **Export member** saves the current state under a name you choose, as a small JSON file (a population member).

In Euclid–Kepler–Pacioli Cell Network the Shear panel moves the lattice only: the cell centres slide, and every piece stays a true regular solid. It hides in Targets, where shearing would change the angles. The findings behind Kaleidohedra, and how each one is checked, are in [DISCOVERIES.md](https://github.com/DICTOR-Master/kaleidohedra/blob/master/DISCOVERIES.md).

## Getting started

### Pick a dimension

After **ENTER**, the dimension picker opens: a slowly turning shape whose faces are **2D+** and **3D+**. Tap **3D+** to build on the lattices, or **2D+** to fold flat nets into solids (Nets). Drag to turn the shape. The welcome screen's **3D+**, **EKP** and **Targets** buttons take you straight in.

You can switch later from **Menu → Change Dimension**, or from the **Wizard** (top left): **3D+** lists every lattice with its pieces as rotating wireframes, together with Kaleidohedra's own worlds, and **2D+** opens Nets.

### Place your first piece

An empty world shows an **orange outline** where the first piece goes. Tap it. Then tap a face of any piece to add a neighbour on the other side of it.

You build one piece at a time. 3D+ starts with the **RD** (rhombic dodecahedron) selected. The piece you're placing is shown in the **Shape** button at the bottom left; tap it to choose a different one.

### Remove a piece

- **Phone or tablet:** long-press the piece.
- **Mouse:** right-click the piece. Right-click removes in every mode.

To take back your last change, tap **Undo** (↶, bottom right). Hold it to scrub back several steps at once. Each dimension keeps its own undo history, so undoing in Nets never touches your 3D+ build.

### Move the camera

- **Rotate:** drag with one finger, or drag with the left mouse button.
- **Zoom:** pinch, or use the scroll wheel.
- **Pan:** drag with two fingers.

## Choosing what to build

### The pieces, by lattice

**2D Nets** (Wizard → 2D+): from 2D to 3D. Pick a solid in the panel: the **Voronoi cells**, Cube, RD and TO (truncated octahedron), the space-filling cells of the simple, face-centred and body-centred cubic lattices; its net shows as a faint ghost. Follow it: tap to build the first face side by side, in 1D cells, then each tap builds the next face. When the net is complete, tap and it folds up into the solid (the indicator reads **2D+/3D+**); the **fold slider** folds and unfolds it by hand, and **Open in 3D+** takes the finished solid there. Long-press takes back a face (or unfolds). Each solid keeps its own progress. The **Platonic solids** are a second group: tetrahedron, octahedron, icosahedron, dodecahedron and the cube. **Open in 3D+** appears for the solids the 3D+ world has as pieces (cube, RD, TO, octahedron). **⊘** beside Undo clears the net you're on.

**Paint** (3D+): the brush on the bottom row, or the Paint switch in the middle of the colour wheel, recolours pieces you've already placed. Turn it on, pick a colour, tap a piece; turn it off to build again. It switches colours to Pick, so each piece shows its own colour. (Shells, Golden Rhombohedra, EKP and Targets colour their pieces their own way, so Paint isn't offered there, nor in Nets.) When the bottom row's slot is taken by an attach toggle (Rhombohedra and Pyrochlore), the brush sits just above it.

**3D+:**

| Lattice | Pieces |
|---|---|
| FCC | Rhombic Dodecahedron (RD), Hemi RD, Hourglass, RD Quarter, Cube, Pyramid |
| DICTO FCC | DICTO RD: DICTO's skewed rhombic dodecahedron of blue Zometool struts (six 60° and six 72° rhombi, volume φ² at edge 1), packed as a sheared FCC; DICTO Blocks: its four blocks, two all-rhombus blocks and two flattened rhombohedra, placed face to face |
| RD Dual | Cuboctahedron (CO), Octahedron |
| BCC | Truncated Octahedron (TO) |
| BCC Interstitial | Flattened Octahedron, Disphenoid |
| Elongated Dodecahedron | Elongated Dodecahedron (ED) |
| Hexagonal | Hex Prism |
| Rhombohedral | Rhombohedra |
| Pyrochlore (3D Kagome) | Truncated Tetrahedron (the tetrahedra between them are added for you) |

Try this on FCC: place six Pyramids to form a Cube. Then add one Pyramid to each face of the Cube, and it becomes an RD. Remove those six again to go back to a Cube.

**RD Quarter** is one of the 4 rhombohedra an RD splits into. Tap an RD near one of its corners to fill that corner in, then tap a quarter's face to place its mirror image across that face. The mirror image always lands back on the RD lattice, so you can extend quarters from cell to cell. For a free rhombohedron lattice with Copy as well as Mirror, use **Rhombohedra**.

### Colours

Pieces are coloured by the **Colours** setting (in Settings): **Cyan** (every piece cyan, the default), **Type** (each kind of piece in its own colour, editable in the list shown) or **Pick** (each piece keeps the colour it was placed with). Tap the **Colour** button (bottom left) to choose from 15 colours: in Cyan this switches to Pick, and in Type it changes the colour of the kind of piece you're placing. Switching never loses the colours pieces were placed with.

## Looking at your build

| View | What it shows | How to turn it on |
|---|---|---|
| World View | Colour, Translucent or Skeleton | Tap the World View button to cycle |
| Lattice View | Your build plus every open slot one step out, for the chosen piece | Tap the Lattice View button (or ⬡ on the corner wheel) to cycle through the pieces |
| X-Ray | A cutaway. Drag the plane through the structure, including on a diagonal | X-Ray button (⛶) |
| Spherical | Tap to cycle: each piece as a sphere (whole RDs touch their twelve neighbours), then the voids between whole RDs (octahedral gold, tetrahedral rose, where fully enclosed) with every sphere made faint. A slider sizes every sphere (a click-stop at each shape's own size; below = apart, beyond = overlapping). With Lattice View on, every open lattice slot shows as a faint sphere. View only | Spherical button (◯): off → spheres → voids |
| Duality | The aperiodic tiling that this crystal structure casts | Duality button (◐) |
| Dualize | Swaps FCC and BCC | Settings → Dualize Preview |

Settings also has a **Section view**: pick an axis, drag the slider to move the cut, and tick **Flip** to see the other side.

## Shells

A 3D world for building **hulls**: shells of rhombic dodecahedra (RDs), each shell its own colour band, counted out from your first piece. Choose it in the Wizard's 3D+ screen.

- **+ Shell** fills the next shell, **− Shell** removes the outermost. **Hull** chooses how shells count: **Steps** (a cuboctahedron: 13, 55, 147 … pieces), **Distance** (toward a sphere), or a target shape (tetrahedron, cube, octahedron, RD or truncated octahedron). **Trim** cuts the hull exactly flat into that shape.
- **Fragment** mode: tap a piece, then pick a **Breakdown** (halves, thirds, quarters, sixths, eighths, twelfths, sixteenths, 24ths or 48ths); **Turn** changes the cut. In Build mode the **Piece** menu places single parts too.
- **Scale** builds with bigger RDs (×2 to ×4). **Merge ×2 / ×3** on a targeted piece shows the big RD's outline, then **Confirm** swaps in one big RD; the Breakdown menu opens it again.
- **Info** shows the ring diagram: tap a ring to hide or show that shell and look inside, remove any shell, and pick the band colours.

## Golden Rhombohedra

A 3D world for the two pieces of the 3D Penrose tiling. Choose it in the Wizard's 3D+ screen. Tap the orange outline, then tap a face to add the **Prolate** or **Oblate** piece chosen in the Piece menu. **Penrose check** colours pieces green where they belong to the true aperiodic tiling and red where your build has drifted; Lattice View shows the true tiling around you, and tapping a ghost places it.

The same two blocks are the pieces of DICTO's **RHOMBITURE**, an extractable armature system for carving and modelling: [doi:10.5281/zenodo.23173896](https://doi.org/10.5281/zenodo.23173896).

## Euclid–Kepler–Pacioli Cell Network (EKP)

A 3D world on one exact cell. Put Euclid's roofs on a cube and you get a regular dodecahedron; fold the roofs back in through the cube's faces and they make a regular icosahedron. The cube, dodecahedron and icosahedron edges are in the ratio φ² : φ : 1. Choose it in the Wizard's 3D+ screen. Tap the orange outline, then pick a **Piece** (cube, dodecahedron, icosahedron, great stellated dodecahedron, octahedron, stella octangula or golden rectangles) and tap a solid: the piece goes into that cell if it isn't there yet, otherwise into the next cell across the tapped face. Smaller solids sit inside larger ones, so use **X-ray** or the translucent view to see them. **View** redraws the same build: two solids alternating by a **Pattern**, a checkerboard, or the merged outer surface of all the dodecahedra. **Vertices** marks the cube corners or every vertex, and **Info** shows the space group (Pm-3 for the cell itself; each pattern has its own). Adding dodecahedra across their faces only ever reaches cells of the same colour in the diagonal pattern; add across a cube face to reach the others. **Turn odd cubes** turns every piece in each odd cube a quarter turn about the vertical axis, so neighbouring cubes alternate. It also turns the merged outer surface.

Three of those pieces complete a homage to Kepler: the **octahedron** on the cube's face centres, with the icosahedron's corners on its edges at the golden section; the **stella octangula**, two regular tetrahedra on alternate cube corners that overlap in that octahedron; and Pacioli's three interlocking **golden rectangles**, which are exactly where the neighbouring cells' roof ridges meet. Together all five Platonic solids nest in one cell: icosahedron, octahedron, tetrahedra, cube, dodecahedron.

The cell behind this world is the **Euclid–Kepler–Pacioli cell**, and great stellated dodecahedra and icosahedra touching only at corners form the **Euclid–Kepler–Pacioli network**, both by DICTO. Cite them as [doi:10.5281/zenodo.23173809](https://doi.org/10.5281/zenodo.23173809).

## Studies

A 3D+ world of exact constructions on the Euclid–Kepler–Pacioli cell, shown one at a time (Wizard → 3D+ → Studies). Pick a **Study**: **Windows** (the dodecahedron with its six face-neighbours' stella octangulas carved out, leaving 12 Penrose thick rhombi at the dodecahedron's own face angles), **Windows, with the six stellas**, **Dodecahedra and their Dogstars** (regular dodecahedra on the even cells leave one hole in each odd cell: the Dogstar, an 8-pointed star, a partial stellation of a dodecahedron 1/φ³ their size, inside the cell's stella octangula; together they fill space, and **Apart** pulls them apart), **Windows and stellas, checkerboard** (the stella octangula is the windows' other half: windows in the even cells and stellas in the odd ones fill space exactly, 12 + 4 = two cubes; the **Apart** slider pulls them apart to see them fit), **Windows made convex** (each rhombus pushed straight out; the **Push** slider snaps at the golden point, where 6 golden rhombi appear, 74 faces in all), **Windows into the icosidodecahedron** and **Windows into the rhombic dodecahedron** (the **Morph** slider moves the rhombi into each; the hull is drawn solid with the rhombi inlaid, their outlines showing through it on the way), and **Stretched dodecahedron** (8 pentagons, 4 hexagons and 2 rectangles; the **Stretch** slider snaps at one edge, where the rectangles are squares, and at the lattice spacing). Studies shear too: as exact copies on the lattice or, one tap away, as the solid itself.

## Stella–Jewel Lattice

A 3D+ world (Wizard → 3D+ → Stella–Jewel Lattice) of two pieces that fill space together in a checkerboard: the **Dragon Jewel** (DJ, DICTO's name for the windows solid of the Studies world) on the even cells and the **stella octangula** on the odd cells. Tap the cyan Dragon Jewel to place it, then tap any face to add the piece across it; long-press to remove. **View** switches between both pieces and **Dragon Jewels alone**, which meet face to face on all 12 of their rhombi and leave stella-shaped holes. **Shear** works as in Studies: exact copies on the moving cell centres, or the whole packing bent. **Five-fold axes** draws each Dragon Jewel's six five-fold axes and, on each face, the five places a window could sit, the one the cube picks bright. Lattice View shows the empty cells you can fill next.

## Sunstar Lattice

A 3D+ world (Wizard → 3D+ → Sunstar Lattice) of regular dodecahedra in their densest lattice packing on the even cells and, in each hole they leave on the odd cells, a **Dogstar**: an 8-pointed star, exactly a partial stellation of a dodecahedron 1/φ³ their size, with only golden edge lengths. A dodecahedron with the Dogstars round it is a **Sunstar**, the sun with its sun dogs (DICTO's names). Tap the cyan dodecahedron to place it, then tap any face to add the piece across it; long-press to remove. **View** shows both, the **Dogstars alone** (they share corners, four at each cube corner, like a 3D Kagome; a tap adds the nearest Dogstar sharing a point) or the **dodecahedra alone**. **Shear** and **Five-fold axes** work as in the Stella–Jewel Lattice.

## Targets

A 3D gallery of the 160 target cells: every space-filling cell with all edges equal whose edges meet only at special angles (36°, 45°, 60°, 70.53°, 72° and 90°), found by an exact search done two ways (see [TARGETS.md](https://github.com/DICTOR-Master/kaleidohedra/blob/master/TARGETS.md)). Choose it in the Wizard's 3D+ screen. Pick a **Type** (parallelepiped, hexagonal prism, rhombic dodecahedron, elongated dodecahedron or truncated octahedron) and a cell, or step through them with ◀ ▶. Each is named by its type, its number in TARGETS.md and its angles; ✓ marks the ones already in Polyhedraverse. **Show** draws the cell alone, with its face neighbours, or as a 3×3×3 block of its lattice, so you can see it fill space. Faces are coloured by kind: squares blue, rhombi pink, regular hexagons gold, other hexagons purple. **Info** lists its faces, the angles between its edge directions, its volume (edge 1), the lattice it tiles as, and whether it is in Polyhedraverse yet. Nothing is built here, and the Shear panel hides, so the angles stay exact.

## Saving your work

Your World saves automatically in this browser, every dimension, after each change. It comes back when you reopen the site on the same device and browser.

In **Settings**:

- **Export World** saves everything, every 3D+ lattice and world and your nets, to one file. Use it to keep a backup or move your World to another device.
- **Import World** opens an exported file. **Undo** takes an import back.
- **Clear World** (⊘ on the corner wheel) starts again with an empty world. Undo can bring it back.

## Learning the maths

- **Almanac:** the maths and geometry behind every piece and lattice. Open it from Menu → Almanac.
- **What's New** lists recent changes.

---

# Control reference

## Screen buttons

| Control | What it does |
|---|---|
| Wizard (top left) | Browse dimensions and lattices, each with its pieces. The large orange label beside it shows the dimension you're in |
| Shape (bottom left) | The piece you're placing. Tap to change it |
| Colour (bottom left) | Build colour. Tap to change it |
| Lattice View | Cycles through Off and a view for each piece |
| Attach toggle | Only shown for pieces that attach more than one way (Rhombohedra: Copy / Mirror; Pyrochlore: small / whole tetrahedron): tap to switch |
| Undo (↶, bottom right) | Tap to undo one step in the current dimension. Hold to scrub back further |
| Paint (brush) | Recolour placed pieces: turn on, pick a colour, tap a piece. In the attach toggle's place on the bottom row; when that toggle is needed it sits just above it |
| ⊘ Clear (beside Undo, Nets) | Clears the net you're on to start again; Undo brings it back |
| Menu | Opens the menu wheel (keyboard: Tab or Space) |

## Corner wheel

Drag the small wheel in the corner to turn it. Tap a face to use it.

| Symbol | Control |
|---|---|
| ⚙ | Settings |
| ⛶ | X-Ray |
| ◐ | Duality |
| ⬡ | Lattice View |
| ◇ | Menu |
| ⊘ | Clear World |
| ↻ | Reload (use it if something looks stuck) |
| ◯ | Spherical (off → spheres → voids) |
| — | World View |

## Menu wheel

The menu is a rhombic dodecahedron. Each face is a section: tap a face to open it, and use **Home** to go back. **Almanac** is always on a top face.

| Section | Contents |
|---|---|
| Home | Piece, Colour, Change Dimension |
| Piece | RD family, Cube, Pyramid, TO, Flattened Octahedron, Disphenoid, CO, Octahedron |
| RD family | RD, Hemi RD, Hourglass, RD Quarter, ED, Hex Prism, Rhombohedra, Pyrochlore |
| Change Dimension | 2D+, 3D+ |

## Settings

| Setting | What it does |
|---|---|
| Look sensitivity | Camera rotation speed |
| Invert Y | Reverses vertical drag |
| Field of view | Camera lens width |
| Graphics quality | Low, Medium or High |
| Show FPS meter | Frame-rate counter |
| Volume | Sound level |
| Language | English, 日本語, Español, Français, 한국어, 中文, Русский (also the 🌐 picker at the top of the welcome screen and this guide) |
| Colours | Cyan, Type or Pick: how pieces are coloured |
| Section view, axis, position, Flip | Cutaway along one axis |
| Dualize Preview | Special build mode |
| Export World, Import World | Back up and restore (every dimension) |

## Keyboard and mouse

| Input | Action |
|---|---|
| Left-click a face | Add a piece |
| Right-click a piece | Remove it |
| Left-drag | Rotate the camera |
| Scroll wheel | Zoom |
| Tab or Space | Open the menu wheel |
| Escape | Close the menu, Wizard or Almanac |
| Enter | Enter from the welcome screen |

## Touch

| Gesture | Action |
|---|---|
| Tap a face | Add a piece |
| Long-press a piece | Remove it |
| One-finger drag | Rotate the camera |
| Pinch | Zoom |
| Two-finger drag | Pan |
