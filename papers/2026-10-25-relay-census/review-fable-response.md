# Response to the referee report on #53 (review-fable.md), v2, 2026-10-25

| Point | Change |
|---|---|
| 1 MAJOR (Obs. 1 is a theorem) | Observation 1 removed; new **Proposition 1 (the unlike bond can never break)** in §4 with the referee's elementary proof, and the three-kind statement ("each kind keeps some unlike bond, not necessarily with every other kind"), which explains the perovskite. In short: "…never breaks, and we prove that it never can." Conclusion: "…and Proposition 1 shows it cannot." "We found no general statement" → "We found no statement of this elementary fact in the sources searched." Remaining observations renumbered 1–4. Study README updated (commit 5307e7b). |
| 2 MAJOR (closed rectangle) | Main theorem (v): "cells of positive volume exactly on the open rectangle −2 < λ < 2, −1 < μ < 1 (its closure has area 8)". In short: "the open rectangle". Figure 4 caption: "(open; its edges are where one kind has shrunk to points)". |
| 3 MINOR (Zn sites) | "Zn: the points 2(a, b, c) of 2ℤ³ with a + b + c even, that is 2D₃". Audit row 45 now records the v1 error. |
| 4 MINOR (hcp −11/24) | Observation 4: exact derivation (three oct holes at 3/8, fourth neighbour the other tet at 1/6, cell shrinks to (0, 0, c/2), 1/24 − λ = 1/2) and the general rule (end = ±d² exactly when the vanishing cell shrinks onto its own site). Study README updated. |
| 5 MINOR (wall segments) | New exact check `scripts/walls.py` in the study (5 midpoints, 5 PASS; total 648); proof of (v) explains why one point per open segment suffices; claim now "no point of the open rectangle (chamber, wall or corner) has only unlike bonds". |
| 6 MINOR (switch points are walls in general) | Corollary 2 opens with the general two-line argument (bipartite dual edges; a simplex with ≥ 3 corners of two kinds has a like edge). Observation 1 (diagonal swap) kept as open. |
| 7 MINOR (Fig. 4 title clipped) | Title shortened to "6 squares + 12 hexagons"; panel margins added. |
| 8 MINOR (figure order) | 3D stops are now Figure 3 (cited in Cor. 3), perovskite map Figure 4 (cited in Cor. 6); files renamed. |
| 9 MINOR (Cor. 4 fluorite) | "tet–tet bonds are born (at squared distance 1/2, as in fluorite, and also at 1)". |
| 10 MINOR (reference order) | #37a and #40 renumbered [4], [5]; all others shifted; list in numeric order. |
| 11 NIT (Weaire–Phelan) | "0 (the polyhedral Weaire–Phelan cells, before Weaire and Phelan relaxed them into a curved foam)". |
| 12 NIT (Fig. 2 dots) | Checked: dots were drawn for both kinds (a debug render with axes shows the centre site (1, 1) inside its blue cell), but too small to see under the bond lines. Dots enlarged with white rims; caption: "black dots: the sites of both kinds". |
| 13 NIT (pages of [13], [21]) | Not added: the page ranges are from memory and could not be verified against a copy; left without pages. |
| 14 NIT (Wang et al.) | No change (citation kept, as advised). |
| 15 NIT (changeover remark) | Not added, as advised (and as instructed). |
| 16 NIT (Obs. on equal weights) | No change needed; Observation 3 already says the honeycomb and fluorite switches are not at equal weights. |

Rules kept: no "ask"/"question" (grep: 0 hits); DICTO's title, number and term unchanged.
