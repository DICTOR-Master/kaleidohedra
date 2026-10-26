# Pyrochlore Halves

**Authors:** DICTO and collaborators

## 1. Introduction

DICTO's idea extends the "rule of halves" established in prior work (#57) to the pyrochlore network, proposing that the weighted division of this lattice follows a universal halving rule regardless of the stacking order of its layers. This study applies the rule of halves to the pyrochlore network, where layers are stacked in any sequence, maintaining the structural integrity of the network's geometric properties.

## 2. Main Theorem

We state that for any close-packed stacking of the pyrochlore network, the weighted pieces of the atoms and holes at specific rational weights ($\lambda$) decompose exactly into the halves of the corresponding pure stacking layers.

**Theorem 1 (Pyrochlore Halves):** For the pyrochlore network constructed from a close-packed stacking word, the weighted census of pieces at $\lambda \in \{-1/4, -1/5, -1/10, 0, 1/10\}$ yields exactly 204 pieces at each weight, where every piece of a mixed stacking (e.g., 4H, 6H, 9R, 15R) equals the same piece of the pure stacking of its layer (3C if $c$, 2H if $h$).

*Proof Status:* PENDING. The exact proof of the halves, following the methodology of #57 (locality over the 16 $h/c$ windows of six layers, then exact corner functions per stretch), is marked as pending. Exact walks for the cubic (3C) and hexagonal (2H) stackings have been completed and checked.

## 3. Construction

The pyrochlore network is constructed as the set of bond midpoints of a diamond-type crystal, where the diamond structure itself is defined by balls and the tetrahedral holes "over $X$ at $3/4$" above each ball. In this construction, each atom's four bond midpoints form a regular tetrahedron of edge $1/2$, a property checked for 3C, 2H, 4H, and 6H stackings to confirm that every corner lies in exactly two tetrahedra. Per gap in the stacking, there are four sites: $S$ (ball), $C$ (diamond atom), $O$ (octahedral hole), and $Y$ (tetrahedral hole over $Y$ at $1/4$), with the two empty holes per gap constituting the network's voids.

## 4. The Weight Walk

Using the power cells with weights $w(S) = w(C) = \lambda$ and $w(O) = w(Y) = 0$ (from #57's census engine), we determine the exact stops for the cubic and hexagonal stackings. For the cubic (3C) stacking, the stops occur at $-3/8$ (atom pieces vanish), $-1/4$ (atoms become regular tetrahedra, holes become truncated tetrahedra with 12 corners, forming the tetrahedral-truncated tetrahedral "quarter cubic" honeycomb), $+1/4$ (roles swapped: atoms 12 corners, holes 4 corners), and $+3/8$ (hole pieces vanish). For the hexagonal (2H) stacking, the exact stops are $-11/36, -1/4, -3/20, 0, 1/8, 1/6, 1/4$; at $-1/4$, the diamond-atom pieces over hexagonal layers are regular tetrahedra, but the ball pieces have 10 corners, meaning the regular pyrochlore tetrahedra are exact pieces only on cubic layers.

## 5. The Rule of Halves

The rule of halves states that the $O$ and $Y$ pieces are cut at the gap's mid-height into a bottom half (layer $k$) and a top half (layer $k+1$), while the $S$ piece remains whole (its own layer) and the $C$ piece remains whole (nearest layer $k+1$). Evidence from the census engine checks shows that every piece of 4H, 6H, 9R, and 15R equals the same piece of the pure stacking of its layer, with 204 pieces found at each of $\lambda = -1/4, -1/5, -1/10, 0, 1/10$, and none off (float, 7 decimals).

## 6. Prior Art and Credit

We credit the pyrochlore lattice as the bond-midpoint (medial) lattice of diamond and as alternating kagome and triangular layers along $[111]$, as described in standard frustrated-magnetism papers. We also credit the known stackings of diamond/lonsdaleite and zincblende/wurtzite, the classical quarter cubic honeycomb, and the rule of halves from #57 (DICTO). Not found in the sources searched (library of 302 references; web, 2026-10-27) is the rule of halves for pyrochlore stackings or their weighted division.

## 7. Methods and Data

The methods employed include exact rational arithmetic via #57's census engine, unchanged from prior work. The data for this study is located in `k-research studies/2026-10-27-pyrochlore-halves`, containing the scripts `pyro.py`, `cells.py`, `halves.py`, and `pyro_walk.py`.

---
**References**
#57 The Rule of Halves: 10.5281/zenodo.23647898
#58 From the Octet to Every Stacking: 10.5281/zenodo.23665944
