# Flip test (DICTO, queued 2026-10-13; run 2026-10-16)

Every piece of each Spheres of Dharma skin turned over through the sphere midway between its two solids, as a physical half-turn
(DICTO's choice): a half-turn about a line on the midway sphere, at the point on the piece's own axis halfway between the inner and outer
solid (all Dharma pieces have a mirror plane through their axis, so this equals reflection in the midway plane). `scripts/flip.py`
on `data/dharma_cycle.json`; results `data/flip-dharma.txt`.

| Skin | Midway sphere covered | Twice | Worst overlap |
|---|---|---|---|
| I -> ID | 100% | 35% | 0.369 |
| ID -> D | 3% | 0 | none (pieces apart) |
| D -> TI | 67% | 4% | 0.163 |
| TI -> Hecatodihedron | 8% | 0 | none |
| Hecatodihedron -> RT | 18% | 0.1% | 0.070 |
| RT -> I(phi^2) | 100% | 36% | 0.309 |

**Result: no skin flips into a closed shell.** Few-piece skins of large pyramids drift apart (points inward, 3-8% cover); closed skins
crowd (a third doubled). Nearest: D -> TI. In every skin the flipped pieces rest on the inner solid and never cut into it (their inner
face lands on that surface). Reading: Dharma's pieces are shaped for their direction; "inside out" needs polar reciprocation (new pieces),
the third part of DICTO's 2026-10-13 idea. Not yet run: Karma, Bodhi, the 13s.
