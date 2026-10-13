# Brief for Fable: "Capturing the In-betweens: a Study of Transitional Polyhedral Shells"

Author: DICTO (credit "DICTO", dictospheres.com, on everything). One job: a complete first draft of the paper, for DICTO to read.
Nothing is uploaded or released anywhere (no Zenodo, no GitHub release, no push); DICTO decides.

## The idea (DICTO's own words, 2026-10-13)
"These forms may be known about, but possibly not viewed as transitional shapes between the regular well-known solids, and there may
be hidden value in analysing the transitional steps that show as the models build and change." DICTO found them by eye, scrubbing
the Top shell slider in the Kaleidohedra app's Multi-shell chains world: about 11 striking shapes on Chain step 2, 5 on the Lotus
seed, 4 on the Dodecahedral Chain, and 6 more on the other views, "intermediate really, but the images change dramatically even
where the structure is close".

**Your own conclusion (DICTO's request):** judge for yourself what value these transitional structures have (or do not have), from
the evidence: mathematical, educational, design, physical or other. DICTO's thesis is the starting point, not the verdict; say
plainly where the evidence is thin. DICTO's pointer for where the value may lie: read the transitional shells in the light of
**crystal growth and viral (capsid) growth**, **materials science**, **chemistry** (clusters, nanoparticles, quasicrystals,
coordination shells) and **medicine** (viruses, drug-delivery cages, protein assemblies), and any other relevant field you find.
Test each connection against the literature; keep only what holds.

**What happens next (state it as the plan, not as a finding):** the transitional shells are being added to Polyhedraverse as their
own group, and the app gets a movie slider that plays the transitions the build goes through.

## The structures (DICTO's published findings; cite by concept DOI)
- Chain of Karma, DISCOVERIES #22, doi:10.5281/zenodo.23310541 (Lotus seed, Chain step 2, Dodecahedral Chain).
- Spheres of Dharma, #23, doi:10.5281/zenodo.23310833 (one Ritsudō cycle: icosahedron → icosidodecahedron → dodecahedron →
  truncated icosahedron → rhombic triacontahedron → icosahedron φ³; inner half, outer half, hinge).
- The Bodhi Seed, #24, doi:10.5281/zenodo.23311353 (seed; Kit A; Kit B; the hollow).
Piece names are DICTO's (AXE, CLEO, FUJI, Vajra, Crown Jewel, Diadem L/R, ...): keep them, untranslated.

## Timing
The figure set (`renders/` and `renders/index.json`) and the corrected counts are being produced while you start (a recount fixed
face counts on large builds). Start with the library and the literature; before choosing figures, wait until
`renders/index.json` exists (check every few minutes; Claude will also write `renders/READY` when it is complete).

## What is in this folder (use it; do not recompute what is here)
- `renders/` — every catalogued stage as a 900 px PNG in the catalogue's look, and `renders/index.json` with each figure's facts
  (structure, step, what it adds, convex or not, faces, face shapes, planes, leads). Orange = the pieces added at that step (or the
  partial ring); other colours = earlier rings. **Choose how many figures the paper needs** (and compose plates/strips from them).
- `catalogue.html` (also at https://claude.ai/artifact/TS4VQDDKB1eBncYiWfBdMo): the main route of each structure, every convex
  stage, the partial rings on complete shells, the app's own Top shell stages for all 11 views, and the growth film.
- `steps.json`, `stages.json`, `partials.json`, `selection.json`, `stages-facts.json`, `appstages.json`, `appstages2.json`: the data.
  Full counts (kept as data, not figures): Spheres of Dharma 107 whole-ring and 5,569 partial-ring stages; Karma 7 / 124; Bodhi 10 / 363.
- `README.md`, `facets.json`: the first pass (opening the shells by large facets: frusta where the inner and outer solids are similar;
  pyramids with recesses otherwise).
- `scripts/`: how everything was counted. Faces = the fused solid's outside, coplanar touching faces merged; rounding gaps closed.

## Leads to check, not claims (verify each before it goes in the paper)
- Karma step 2 (icosahedron + 20 CLEO): 60 visible triangles on 12 planes, the look of Kepler's great stellated dodecahedron.
- Karma step 3 (+30 AXE): faces on the 20 planes of the centre icosahedron: a stellation of the icosahedron (which one?).
- Bodhi Kit B step 2 (+60 Vajras): faces on the 30 planes of the centre triacontahedron: a stellation of the RT (which one?).
- Spheres of Dharma: a convex 80-corner stage (60 triangles, 30 rectangles, 12 pentagons) — named or not?; 45 convex stages among
  the partial rings on complete shells.
- Chain step 2's stages (several with faces on few planes).

## What to write
1. A full draft (Markdown + a print-ready PDF with figures), professional and checkable: claims only where checked; interpretation
   kept out of the abstract. Sections at your judgement; DICTO's thesis above is the starting point.
2. **Relevant fields and references.** Search DICTO's reference library FIRST (`~/Documents/kaleidohedra-references/`, INDEX and
   READING-LIST; history/ has Kepler 1596 and 1619, Jamnitzer 1568, Dürer 1525, Pacioli 1509, Hogan 1976 and more), then the wider
   literature: e.g. stellations (Coxeter et al., The Fifty-Nine Icosahedra; Wenninger), Mackay icosahedra and cluster magic numbers,
   nested Platonic solids (Kepler's Mysterium), polyhedral transitions/morphs (Jessen, jitterbug, cuboctahedron–icosahedron),
   quasicrystal approximant shells, virus capsids, nanoparticle/Mackay/anti-Mackay growth, self-assembly pathways, deployable
   structures, design/architecture. Credit everything found; **add every new reference to the library** (as its README/INDEX do).
3. **Cut-out materials** (DICTO: "of course cut-out-and-glue paper shapes should be included"): printable cut-and-fold nets (A4 PDF, numbered glue tabs, DICTO mark) for a small set of the most telling
   transitional shells (your choice, e.g. one per structure), so readers can build the in-between solids by hand. Check each net
   folds to the right solid (no overlaps) before including it.
4. Your own conclusion on their value, then the plan above (Polyhedraverse group + movie slider in the app).

## Conventions (DICTO)
Dated study folder (this one); data raw + with checks; figures in the app's style; a short report of what was checked and how;
DICTO · dictospheres.com on every figure, net and PDF. Heavy computation goes to dicto-node (`ssh 192.168.0.7`; Python with numpy,
scipy, shapely in `~/fusedenv`; this folder mirrored at `~/fused-shells`). Commit to the local repo only; do not push.
