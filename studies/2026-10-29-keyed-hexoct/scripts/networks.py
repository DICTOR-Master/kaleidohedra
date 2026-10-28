# The networks of the relay census: exact sites (rational coordinates, rational metric G), translation basis T, two kinds A, B with
# w_A = lam, w_B = 0. "expect": (lam, kind, number of faces, face sizes (3D) or number of corners (2D), bonds by neighbour kind,
# name of the known cell) - the sanity checks against classical cells.
from fractions import Fraction as Fr
from itertools import product

h = Fr(1, 2)
I2 = [[1, 0], [0, 1]]; I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
HEX2 = [[1, h], [h, 1]]                       # triangular lattice basis a1, a2 at 60 degrees, |a| = 1
HCP = [[1, h, 0], [h, 1, 0], [0, 0, Fr(8, 3)]]  # hexagonal basis a1, a2 (60 deg), c with c^2 = 8/3: ideal hcp, edge 1
fcc4 = [(0, 0, 0), (2, 2, 0), (2, 0, 2), (0, 2, 2)]
fcc8 = [(0, 0, 0), (4, 4, 0), (4, 0, 4), (0, 4, 4)]

NETS = {
    # ---- regressions: the two DICTONIC loops of the Bond Relay study, walked over their whole coexistence range
    "bcc": dict(name="bcc two-kind (golden loop sites)", G=I3, T=[(2, 0, 0), (0, 2, 0), (0, 0, 2)],
                motif=[("big", (0, 0, 0)), ("small", (1, 1, 1))], w={"big": (0, 1), "small": (0, 0)}, A="big", B="small",
                D2=24, units="half cube edge L/2 = 1 (big sites 2Z^3); golden loop x in [0, inf] is lam = 2s - 1 in [-1, 1]",
                expect=[(0, "big", 14, [4] * 6 + [6] * 8, {"big": 6, "small": 8}, "truncated octahedron (Voronoi cell of bcc)"),
                        (0, "small", 14, [4] * 6 + [6] * 8, {"big": 8, "small": 6}, "truncated octahedron (Voronoi cell of bcc)"),
                        (3, "big", 6, [4] * 6, {"big": 6}, "cube (Voronoi cell of the simple cubic big sites)"),
                        (-3, "small", 6, [4] * 6, {"small": 6}, "cube (Voronoi cell of the simple cubic small sites)")]),
    "delian": dict(name="fcc + all its tetrahedral holes (Delian loop sites)", G=[[h, 0, 0], [0, h, 0], [0, 0, h]],
                   T=[(2, 0, 0), (0, 2, 0), (0, 0, 2)],
                   motif=[("oct", p) for p in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]] +
                         [("tet", tuple(Fr(2 * a + 1, 2) for a in p)) for p in product((0, 1), repeat=3)],
                   w={"tet": (0, 1), "oct": (0, 0)}, A="tet", B="oct", D2=12,
                   units="octet edge 1 (app units); lam = w_tet - w_oct = (3/8)(2t - 1)",
                   expect=[(Fr(-1, 8), "oct", 8, [3] * 8, {"tet": 8}, "regular octahedron of the octet"),
                           (Fr(-1, 8), "tet", 4, [3] * 4, {"oct": 4}, "regular tetrahedron of the octet"),
                           (Fr(-3, 8), "oct", 12, [4] * 12, {"oct": 12}, "rhombic dodecahedron (Voronoi cell of fcc)"),
                           (Fr(3, 8), "tet", 6, [4] * 6, {"tet": 6}, "cube (Voronoi cell of the simple cubic tet sites)")]),
    # ---- 2D
    "square": dict(name="square lattice + centres (2D CsCl analogue)", G=I2, T=[(2, 0), (0, 2)],
                   motif=[("corner", (0, 0)), ("centre", (1, 1))], w={"corner": (0, 1), "centre": (0, 0)}, A="corner", B="centre",
                   D2=40, units="square edge 2 (corners 2Z^2, centres 2Z^2 + (1,1))",
                   expect=[(0, "corner", 4, 4, {"centre": 4}, "square (Voronoi cell of the centred square lattice)"),
                           (0, "centre", 4, 4, {"corner": 4}, "square (Voronoi cell of the centred square lattice)"),
                           (2, "corner", 4, 4, {"corner": 4}, "square (Voronoi cell of the square lattice)")]),
    "honeycomb": dict(name="honeycomb + hexagon centres (triangular lattice, two kinds 2:1)", G=HEX2, T=[(1, 1), (-1, 2)],
                      motif=[("honeycomb", (0, 0)), ("honeycomb", (1, 0)), ("centre", (0, 1))],
                      w={"honeycomb": (0, 1), "centre": (0, 0)}, A="honeycomb", B="centre", D2=20,
                      units="triangular lattice edge 1",
                      expect=[(0, "honeycomb", 6, 6, {"honeycomb": 3, "centre": 3}, "regular hexagon (Voronoi cell of the triangular lattice)"),
                              (0, "centre", 6, 6, {"honeycomb": 6}, "regular hexagon (Voronoi cell of the triangular lattice)"),
                              (1, "honeycomb", 3, 3, {"honeycomb": 3}, "triangle (Voronoi cell of the honeycomb points)"),
                              (-1, "centre", 6, 6, {"centre": 6}, "hexagon (Voronoi cell of the triangular lattice of centres)"),
                              (Fr(-1, 2), "centre", 6, 6, {"honeycomb": 6}, "hexagon of the trihexagonal tiling 3.6.3.6"),
                              (Fr(-1, 2), "honeycomb", 3, 3, {"centre": 3}, "triangle of the trihexagonal tiling 3.6.3.6")]),
    "kagome": dict(name="kagome + hexagon centres (triangular lattice, two kinds 3:1)", G=HEX2, T=[(2, 0), (0, 2)],
                   motif=[("kagome", (1, 0)), ("kagome", (0, 1)), ("kagome", (1, 1)), ("centre", (0, 0))],
                   w={"kagome": (0, 1), "centre": (0, 0)}, A="kagome", B="centre", D2=24,
                   units="triangular lattice edge 1 (kagome edge 1)",
                   expect=[(0, "kagome", 6, 6, {"kagome": 4, "centre": 2}, "regular hexagon (Voronoi cell of the triangular lattice)"),
                           (0, "centre", 6, 6, {"kagome": 6}, "regular hexagon (Voronoi cell of the triangular lattice)"),
                           (1, "kagome", 4, 4, {"kagome": 4}, "rhombus (rhombille tiling: Voronoi cell of the kagome points)"),
                           (-1, "centre", 6, 6, {"centre": 6}, "hexagon (Voronoi cell of the triangular lattice of centres)")]),
    # ---- 3D
    "nacl": dict(name="rock salt NaCl (fcc + fcc)", G=I3, T=[(2, 0, 0), (0, 2, 0), (0, 0, 2)],
                 motif=[("Na", p) for p in fcc4[:1] + [(1, 1, 0), (1, 0, 1), (0, 1, 1)]] +
                       [("Cl", p) for p in [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)]],
                 w={"Na": (0, 1), "Cl": (0, 0)}, A="Na", B="Cl", D2=20, units="Na-Cl distance 1 (cubic cell edge 2)",
                 expect=[(0, "Na", 6, [4] * 6, {"Cl": 6}, "cube (Voronoi cell of the simple cubic lattice)"),
                         (0, "Cl", 6, [4] * 6, {"Na": 6}, "cube (Voronoi cell of the simple cubic lattice)"),
                         (1, "Na", 12, [4] * 12, {"Na": 12}, "rhombic dodecahedron (Voronoi cell of fcc)"),
                         (-1, "Cl", 12, [4] * 12, {"Cl": 12}, "rhombic dodecahedron (Voronoi cell of fcc)")]),
    "zincblende": dict(name="zinc blende ZnS / diamond (fcc + one set of tetrahedral holes)", G=I3,
                       T=[(4, 0, 0), (0, 4, 0), (0, 0, 4)],
                       motif=[("Zn", p) for p in fcc4] + [("S", tuple(x + 1 for x in p)) for p in fcc4],
                       w={"Zn": (0, 1), "S": (0, 0)}, A="Zn", B="S", D2=64,
                       units="cubic cell edge 4 (Zn-S distance sqrt3)",
                       expect=[(0, "Zn", 16, [3] * 12 + [6] * 4, {"S": 4, "Zn": 12}, "triakis truncated tetrahedron (Voronoi cell of diamond)"),
                               (0, "S", 16, [3] * 12 + [6] * 4, {"Zn": 4, "S": 12}, "triakis truncated tetrahedron (Voronoi cell of diamond)"),
                               (3, "Zn", 12, [4] * 12, {"Zn": 12}, "rhombic dodecahedron (Voronoi cell of fcc)"),
                               (-3, "S", 12, [4] * 12, {"S": 12}, "rhombic dodecahedron (Voronoi cell of fcc)")]),
    "hcpholes": dict(name="hcp holes: octahedral + tetrahedral holes of ideal hcp (gyrated octet sites)", G=HCP, T=I3,
                     motif=[("oct", (Fr(2, 3), Fr(2, 3), Fr(1, 4))), ("oct", (Fr(2, 3), Fr(2, 3), Fr(3, 4))),
                            ("tet", (0, 0, Fr(3, 8))), ("tet", (0, 0, Fr(5, 8))),
                            ("tet", (Fr(1, 3), Fr(1, 3), Fr(1, 8))), ("tet", (Fr(1, 3), Fr(1, 3), Fr(7, 8)))],
                     w={"tet": (0, 1), "oct": (0, 0)}, A="tet", B="oct", D2=12,
                     units="hcp edge 1 (same as the Delian run); lam = w_tet - w_oct",
                     expect=[(Fr(-1, 8), "oct", 8, [3] * 8, {"oct": 2, "tet": 6}, "regular octahedron of the gyrated octet"),
                             (Fr(-1, 8), "tet", 4, [3] * 4, {"oct": 3, "tet": 1}, "regular tetrahedron of the gyrated octet"),
                             (Fr(-11, 24), "oct", 8, [4] * 6 + [6] * 2, {"oct": 8}, "hexagonal prism (Voronoi cell of the simple hexagonal lattice of octahedral holes)")]),
    "a15": dict(name="A15 (Cr3Si)", G=I3, T=[(2, 0, 0), (0, 2, 0), (0, 0, 2)],
                motif=[("Si", (0, 0, 0)), ("Si", (1, 1, 1))] +
                      [("Cr", p) for p in [(h, 0, 1), (3 * h, 0, 1), (1, h, 0), (1, 3 * h, 0), (0, 1, h), (0, 1, 3 * h)]],
                w={"Si": (0, 1), "Cr": (0, 0)}, A="Si", B="Cr", D2=12, units="cubic cell edge 2",
                expect=[(0, "Si", 12, [5] * 12, {"Cr": 12}, "pentagonal dodecahedron (Weaire-Phelan / A15 Voronoi)"),
                        (0, "Cr", 14, [5] * 12 + [6] * 2, {"Cr": 10, "Si": 4}, "tetrakaidecahedron (Weaire-Phelan / A15 Voronoi)"),
                        (Fr(5, 4), "Si", 14, [4] * 6 + [6] * 8, {"Si": 14}, "truncated octahedron (Voronoi cell of the bcc Si sites)")]),
    "c15": dict(name="C15 Laves (MgCu2)", G=I3, T=[(8, 0, 0), (0, 8, 0), (0, 0, 8)],
                motif=[("Mg", tuple((a + b) % 8 for a, b in zip(p, f))) for p in [(0, 0, 0), (6, 2, 6)] for f in fcc8] +
                      [("Cu", tuple((a + b) % 8 for a, b in zip(p, f))) for p in [(5, 5, 5), (3, 7, 1), (7, 1, 3), (1, 3, 7)] for f in fcc8],
                w={"Mg": (0, 1), "Cu": (0, 0)}, A="Mg", B="Cu", D2=100, units="cubic cell edge 8 (Cu-Cu 2 sqrt2, Mg-Mg 2 sqrt3)",
                expect=[(0, "Mg", 16, [5] * 12 + [6] * 4, {"Mg": 4, "Cu": 12}, "Friauf polyhedron Z16 dual (C15 Voronoi)"),
                        (0, "Cu", 12, [5] * 12, {"Cu": 6, "Mg": 6}, "Z12 cell (C15 Voronoi)"),
                        (11, "Mg", 16, [3] * 12 + [6] * 4, {"Mg": 16}, "triakis truncated tetrahedron (Voronoi cell of the diamond Mg sites)")]),
}
