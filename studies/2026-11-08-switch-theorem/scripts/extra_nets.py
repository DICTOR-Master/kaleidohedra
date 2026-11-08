# Two control networks for the switch theorem, added to the relay census's NETS (same format, same engine):
#  hbn       the honeycomb with its two sublattices as the two kinds (hexagonal boron nitride; B and N), edge 1;
#  sodalite  the vertices of the bitruncated cubic honeycomb (truncated octahedra; the tetrahedral sites of sodalite), split
#            into the two classes of its bipartite edge graph (the Si/Al order of sodalite that obeys Loewenstein's rule).
# Both have, at equal weights, dual cells that are not simplices and whose edges are all unlike (hexagons; truncated octahedra
# if the Delaunay test passes), so lam = 0 is a switch point by construction, with dual cells that are not quadrilaterals.
import os, sys
from fractions import Fraction as Fr
from itertools import permutations, product
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "2026-10-25-relay-census", "scripts"))
from networks import NETS, HEX2, I3  # noqa: E402


def sodalite_motif():
    verts = set()
    for cen in [(0, 0, 0), (2, 2, 2)]:
        for s in product((1, -1), repeat=2):
            for perm in set(permutations((0, s[0] * 1, s[1] * 2))):
                verts.add(tuple((a + b) % 4 for a, b in zip(cen, perm)))
    verts = sorted(verts)
    # edges: squared distance 2 (TO edge), mod 4Z^3; 2-colour by BFS
    def d2(u, v):
        return min(sum(((a - b + 4 * k) ** 2) for a, b, k in zip(u, v, kk)) for kk in product((-1, 0, 1), repeat=3))
    adj = {u: [v for v in verts if v != u and d2(u, v) == 2] for u in verts}
    col = {verts[0]: 0}; todo = [verts[0]]
    while todo:
        u = todo.pop()
        for v in adj[u]:
            if v not in col: col[v] = 1 - col[u]; todo.append(v)
            else: assert col[v] != col[u], "not bipartite"
    assert len(col) == len(verts) == 12 and all(len(adj[u]) == 4 for u in verts)
    return [("Si" if col[v] == 0 else "Al", v) for v in verts]


NETS["hbn"] = dict(name="honeycomb, two sublattices (h-BN)", G=HEX2, T=[(1, 1), (-1, 2)],
                   motif=[("B", (0, 0)), ("N", (1, 0))], w={"B": (0, 1), "N": (0, 0)}, A="B", B="N", D2=20,
                   units="honeycomb edge 1 (60 degree basis of the triangular lattice of edge 1)",
                   expect=[(0, "B", 3, 3, {"N": 3}, "triangle (Voronoi cell of the honeycomb points)"),
                           (0, "N", 3, 3, {"B": 3}, "triangle (Voronoi cell of the honeycomb points)"),
                           (1, "B", 6, 6, {"B": 6}, "hexagon (Voronoi cell of the triangular lattice of B sites)")])
NETS["sodalite"] = dict(name="sodalite T sites (vertices of the bitruncated cubic honeycomb), Si/Al alternating", G=I3,
                        T=[(4, 0, 0), (0, 4, 0), (0, 0, 4)], motif=sodalite_motif(), w={"Si": (0, 1), "Al": (0, 0)},
                        A="Si", B="Al", D2=24, units="cubic cell edge 4 (truncated octahedron edge sqrt2)", expect=[])
