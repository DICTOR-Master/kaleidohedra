# Plan: the fused-shells catalogue (DICTO 2026-10-13)

DICTO: every stage between the start and the finish of the nested structures (Chain of Karma, Spheres of Dharma, Bodhi Seed Kit B),
each taken as one fused solid; "the whole catalogue should be comprehensive for the paper; interesting ones should be built, and a
selection of them used to show alternative exploded versions". Study folder: `studies/2026-10-13-fused-shells/`. Page:
https://claude.ai/artifact/TS4VQDDKB1eBncYiWfBdMo

Every subset of pieces is far too many (Dharma: 2^237), so the catalogue is complete within stated rules, each counted up to the
structure's own rotations:

1. **Whole-ring stages** (DONE, counting): the centre plus any set of whole rings (all pieces of one kind at one distance) that is one
   connected solid. Dharma 107 (8 convex), Karma 7 (2), Bodhi 10 (2). `stages.py`, `stage_facts.py`.
2. **Symmetric partials**: a whole-ring stage plus one symmetric part of one ring touching it: one orbit of a large subgroup of the
   icosahedral rotations (tetrahedral T, 5-fold D5, 3-fold D3, 2-fold D2). Deduplicated up to rotation.
3. **Hemispheres and caps**: for each stage and ring, the half on one side of a plane through the centre, and the polar cap round one
   5-, 3- or 2-fold axis.
4. **Growth film** (DONE 2026-10-13): the main route built one piece at a time (pieces in order of distance, ties by angle round a 5-fold axis), as a
   slider on the page.
5. **Facts and leads** for every stage: faces, face shapes, planes, convex, symmetry; leads to names (stellations: all faces on one
   solid's planes; classic convex solids; compounds).
6. **Interesting ones built** in the app (Multi-shell chains → a Stages view), chosen by DICTO from the leads: convex stages, named
   look-alikes, stellations, highest-symmetry partials.
7. **Exploded versions** for a selection: Pull apart from the centre, by face, and by ring (each ring moves out as one piece).
8. **Paper**: DICTO's. Library first (Kepler 1596, Jamnitzer 1568, Hogan 1976; add Mackay 1962), then a draft; never uploaded
   without DICTO's OK.

Heavy runs (2–3: thousands of unions) go to dicto-node as logged background jobs.

DICTO · dictospheres.com
