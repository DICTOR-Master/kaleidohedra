
**square** — square lattice + centres (2D CsCl analogue); λ = w_corner - w_centre; square edge 2 (corners 2Z^2, centres 2Z^2 + (1,1))

| λ | bond types | centre cell (faces) | centre bonds | corner cell (faces) | corner bonds |
|---|---|---|---|---|---|
| -2 | centre-centre | 4-gon | 4 centre | point |  |
| (-2, 0) | centre-centre, centre-corner | 8-gon | 4 centre, 4 corner | 4-gon | 4 centre |
| 0 | centre-corner | 4-gon | 4 corner | 4-gon | 4 centre |
| (0, 2) | centre-corner, corner-corner | 4-gon | 4 corner | 8-gon | 4 centre, 4 corner |
| 2 | corner-corner | point |  | 4-gon | 4 corner |

**honeycomb** — honeycomb + hexagon centres (triangular lattice, two kinds 2:1); λ = w_honeycomb - w_centre; triangular lattice edge 1

| λ | bond types | centre cell (faces) | centre bonds | honeycomb cell (faces) | honeycomb bonds |
|---|---|---|---|---|---|
| -1 | centre-centre | 6-gon | 6 centre | point |  |
| (-1, -1/2) | centre-centre, centre-honeycomb | 12-gon | 6 centre, 6 honeycomb | 3-gon | 3 centre |
| -1/2 | centre-honeycomb | 6-gon | 6 honeycomb | 3-gon | 3 centre |
| (-1/2, 1) | centre-honeycomb, honeycomb-honeycomb | 6-gon | 6 honeycomb | 6-gon | 3 centre, 3 honeycomb |
| 1 | honeycomb-honeycomb | point |  | 3-gon | 3 honeycomb |

**kagome** — kagome + hexagon centres (triangular lattice, two kinds 3:1); λ = w_kagome - w_centre; triangular lattice edge 1 (kagome edge 1)

| λ | bond types | centre cell (faces) | centre bonds | kagome cell (faces) | kagome bonds |
|---|---|---|---|---|---|
| -1 | centre-centre | 6-gon | 6 centre | point |  |
| (-1, 1) | centre-kagome, kagome-kagome | 6-gon | 6 kagome | 6-gon | 2 centre, 4 kagome |
| 1 | kagome-kagome | point |  | 4-gon | 4 kagome |

**bcc** — bcc two-kind (golden loop sites); λ = w_big - w_small; half cube edge L/2 = 1 (big sites 2Z^3); golden loop x in [0, inf] is lam = 2s - 1 in [-1, 1]

| λ | bond types | big cell (faces) | big bonds | small cell (faces) | small bonds |
|---|---|---|---|---|---|
| -3 | small-small | point |  | 6×4 | 6 small |
| (-3, -1) | big-small, small-small | 8×3 | 8 small | 8×3+6×8 | 8 big, 6 small |
| -1 | big-small, small-small | 8×3 | 8 small | 8×3+6×4 | 8 big, 6 small |
| (-1, 1) | big-big, big-small, small-small | 6×4+8×6 | 6 big, 8 small | 6×4+8×6 | 8 big, 6 small |
| 1 | big-big, big-small | 8×3+6×4 | 6 big, 8 small | 8×3 | 8 big |
| (1, 3) | big-big, big-small | 8×3+6×8 | 6 big, 8 small | 8×3 | 8 big |
| 3 | big-big | 6×4 | 6 big | point |  |

**delian** — fcc + all its tetrahedral holes (Delian loop sites); λ = w_tet - w_oct; octet edge 1 (app units); lam = w_tet - w_oct = (3/8)(2t - 1)

| λ | bond types | oct cell (faces) | oct bonds | tet cell (faces) | tet bonds |
|---|---|---|---|---|---|
| -3/8 | oct-oct | 12×4 | 12 oct | point |  |
| (-3/8, -1/8) | oct-oct, oct-tet | 8×3+12×6 | 12 oct, 8 tet | 4×3 | 4 oct |
| -1/8 | oct-tet | 8×3 | 8 tet | 4×3 | 4 oct |
| (-1/8, 3/8) | oct-tet, tet-tet | 8×3 | 8 tet | 4×3+6×6 | 4 oct, 6 tet |
| 3/8 | tet-tet | point |  | 6×4 | 6 tet |

**nacl** — rock salt NaCl (fcc + fcc); λ = w_Na - w_Cl; Na-Cl distance 1 (cubic cell edge 2)

| λ | bond types | Cl cell (faces) | Cl bonds | Na cell (faces) | Na bonds |
|---|---|---|---|---|---|
| -1 | Cl-Cl | 12×4 | 12 Cl | point |  |
| (-1, 0) | Cl-Cl, Cl-Na | 6×4+12×6 | 12 Cl, 6 Na | 6×4 | 6 Cl |
| 0 | Cl-Na | 6×4 | 6 Na | 6×4 | 6 Cl |
| (0, 1) | Cl-Na, Na-Na | 6×4 | 6 Na | 6×4+12×6 | 6 Cl, 12 Na |
| 1 | Na-Na | point |  | 12×4 | 12 Na |

**zincblende** — zinc blende ZnS / diamond (fcc + one set of tetrahedral holes); λ = w_Zn - w_S; cubic cell edge 4 (Zn-S distance sqrt3)

| λ | bond types | S cell (faces) | S bonds | Zn cell (faces) | Zn bonds |
|---|---|---|---|---|---|
| -3 | S-S | 12×4 | 12 S | point |  |
| (-3, -1) | S-S, S-Zn | 4×3+12×5 | 12 S, 4 Zn | 4×3 | 4 S |
| -1 | S-S, S-Zn | 16×3 | 12 S, 4 Zn | 4×3 | 4 S |
| (-1, 1) | S-S, S-Zn, Zn-Zn | 12×3+4×6 | 12 S, 4 Zn | 12×3+4×6 | 4 S, 12 Zn |
| 1 | S-Zn, Zn-Zn | 4×3 | 4 Zn | 16×3 | 4 S, 12 Zn |
| (1, 3) | S-Zn, Zn-Zn | 4×3 | 4 Zn | 4×3+12×5 | 4 S, 12 Zn |
| 3 | Zn-Zn | point |  | 12×4 | 12 Zn |

**hcpholes** — hcp holes: octahedral + tetrahedral holes of ideal hcp (gyrated octet sites); λ = w_tet - w_oct; hcp edge 1 (same as the Delian run); lam = w_tet - w_oct

| λ | bond types | oct cell (faces) | oct bonds | tet cell (faces) | tet bonds |
|---|---|---|---|---|---|
| -11/24 | oct-oct | 6×4+2×6 | 8 oct | point |  |
| (-11/24, -1/8) | oct-oct, oct-tet, tet-tet | 6×3+6×6+2×9 | 8 oct, 6 tet | 4×3 | 3 oct, 1 tet |
| -1/8 | oct-oct, oct-tet, tet-tet | 8×3 | 2 oct, 6 tet | 4×3 | 3 oct, 1 tet |
| (-1/8, 5/24) | oct-oct, oct-tet, tet-tet | 2×3+6×5 | 2 oct, 6 tet | 6×3+3×5+3×6+1×9 | 3 oct, 10 tet |
| 5/24 | oct-tet, tet-tet | 6×4 | 6 tet | 6×3+3×4+4×6 | 3 oct, 10 tet |
| (5/24, 3/8) | oct-tet, tet-tet | 6×4 | 6 tet | 9×4+4×6 | 3 oct, 10 tet |
| 3/8 | tet-tet | point |  | 6×3+3×4+1×6 | 10 tet |

**a15** — A15 (Cr3Si); λ = w_Si - w_Cr; cubic cell edge 2

| λ | bond types | Cr cell (faces) | Cr bonds | Si cell (faces) | Si bonds |
|---|---|---|---|---|---|
| -5/4 | Cr-Cr | 8×3+2×4 | 10 Cr | point |  |
| (-5/4, 1/4) | Cr-Cr, Cr-Si | 12×5+2×6 | 10 Cr, 4 Si | 12×5 | 12 Cr |
| 1/4 | Cr-Cr, Cr-Si | 8×4+4×5+2×6 | 10 Cr, 4 Si | 12×5 | 12 Cr |
| (1/4, 3/4) | Cr-Cr, Cr-Si, Si-Si | 8×4+2×6+4×7 | 10 Cr, 4 Si | 8×3+12×7 | 12 Cr, 8 Si |
| 3/4 | Cr-Si, Si-Si | 4×3 | 4 Si | 20×3 | 12 Cr, 8 Si |
| (3/4, 5/4) | Cr-Si, Si-Si | 4×3 | 4 Si | 12×3+6×6+8×9 | 12 Cr, 14 Si |
| 5/4 | Si-Si | point |  | 6×4+8×6 | 14 Si |

**c15** — C15 Laves (MgCu2); λ = w_Mg - w_Cu; cubic cell edge 8 (Cu-Cu 2 sqrt2, Mg-Mg 2 sqrt3)

| λ | bond types | Cu cell (faces) | Cu bonds | Mg cell (faces) | Mg bonds |
|---|---|---|---|---|---|
| -11 | Cu-Cu | 6×4 | 6 Cu | point |  |
| (-11, -5) | Cu-Cu, Cu-Mg | 6×3+6×7 | 6 Cu, 6 Mg | 12×3 | 12 Cu |
| -5 | Cu-Cu, Cu-Mg | 6×3+6×5 | 6 Cu, 6 Mg | 12×3 | 12 Cu |
| (-5, 7) | Cu-Cu, Cu-Mg, Mg-Mg | 12×5 | 6 Cu, 6 Mg | 12×5+4×6 | 12 Cu, 4 Mg |
| 7 | Cu-Cu, Cu-Mg, Mg-Mg | 12×4 | 6 Cu, 6 Mg | 12×4+4×6 | 12 Cu, 4 Mg |
| (7, 9) | Cu-Cu, Cu-Mg, Mg-Mg | 6×4+6×6 | 6 Cu, 6 Mg | 12×3+12×6+4×12 | 12 Cu, 16 Mg |
| 9 | Cu-Mg, Mg-Mg | 6×4 | 6 Mg | 12×3+12×4+4×12 | 12 Cu, 16 Mg |
| (9, 11) | Cu-Mg, Mg-Mg | 6×4 | 6 Mg | 12×4+12×5+4×12 | 12 Cu, 16 Mg |
| 11 | Mg-Mg | point |  | 12×3+4×6 | 16 Mg |
