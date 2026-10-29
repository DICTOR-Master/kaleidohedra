# Spiked TI cycle (DICTO, 2026-10-30)

**Idea (DICTO):** a new golden cycle beginning with a spiked core; core chosen by DICTO: TI (truncated icosahedron, TI) with its 32 face pyramids (study 2026-10-30-ti-pyramids) turned outwards, as the Cleo star turns the icosahedron's Cleo-Icos outwards.

**One-line conclusion.** The spiked TI starts an exact endless cycle of four stations, TI → spiked TI → pentakis hull of the spike tips → TI again, larger; with the pyramids mirrored (tips at 2 × the face centres) it is a **doubling** cycle (×2), and with the spikes at 1/φ of the pyramids' height (tips at φ × the face centres) it is a **golden** cycle (×φ, spiked TI = φ·TI, one turn = φ³ in volume). Each turn is 32 spikes + 300 tetrahedra in 6 shapes (doubling) or fewer (golden), all exact by volume and free of overlap (333 pieces each).
**Status:** done (float volumes to 1e-12 on exact Q(√5) corners; separating-axis overlap test). The spike tips touch no station of DICTO's twelve-station cycle at any golden scale φ^-2..φ^4 (data/contacts.json), so this is a cycle of its own, not a branch of #54.

## The cycle (frame of #54: the icosahedron I of edge 1/φ; TI = (39√5 − 35)/4 = 13.0517)
| Station | Doubling (s = 2) | Golden (s = φ) |
|---|---|---|
| TI | 1 | 1 |
| spiked TI (TI + 12 pentagonal + 20 hexagonal spikes) | 2 TI (each spike a mirrored face pyramid) | φ TI |
| hull of the 32 tips: a pentakis dodecahedron, 60 congruent triangles (not the Catalan one: pentagon tips stand out 1.0265 × the hexagon tips; for s = 2 the hull is 30 + 22√5) | 6.0677 TI | 3.2129 TI |
| s·TI, whose face centres are the tips | 8 TI | φ³ TI = 4.2361 TI |

Pieces of one turn (both scales):
- 32 spikes (pentagonal, hexagonal);
- layer 1, spiked TI → hull: 60 corner tetrahedra (a TI corner and the three tips over its faces), 90 edge tetrahedra (a TI edge and the two tips over its faces; two kinds, pentagon–hexagon and hexagon–hexagon edges);
- layer 2, hull → s·TI: 60 corner tetrahedra (a corner of s·TI and the three tips, which are the centres of its faces there), 90 edge tetrahedra (an edge of s·TI and the two face centres).
Volumes: data/layers-2.json, data/layers-phi.json (layer sums equal the layer volumes to 1e-12; 0 overlapping pairs of 333). In the golden cycle the layer-1 edge tetrahedra of both kinds have one volume (0.103006), and one layer-2 edge tetrahedron has volume exactly 1/12.

## Why it is not golden by itself
Mirroring a face pyramid in its face puts the tip at twice the face centre, so the cycle closes at 2·TI; the golden ratio enters only if the spikes are 1/φ of the pyramids' height. DICTO's Cleo star is the doubling case for the icosahedron (Cleo star = 2·I, #54); its cycle closes through D′ because the Cleo-star tips are the corners of a dodecahedron, which the spiked TI's tips are not.

## Prior art
Stellating or "augmenting" a solid with face pyramids (Kepler; the Catalan and Kleetope constructions) is classical; the pentakis dodecahedron is the Kleetope of the dodecahedron. The two cycles, their pieces and their exact fills are new as far as the sources checked show (the library queries of study 2026-10-30-ti-pyramids; no source treats nested cycles through the truncated icosahedron's outward pyramids).

## Files
scripts/spiked.py (spikes, hull, stations), scripts/contacts.py (contacts with the twelve stations at golden scales), scripts/layers.py (SCALE=2 or SCALE=phi: the two layers, volumes, overlaps). data/stations-exact.json from study 2026-10-25-gnomon-shapes. Run on dicto-big-brother (~/kres-tmp/spiked).
