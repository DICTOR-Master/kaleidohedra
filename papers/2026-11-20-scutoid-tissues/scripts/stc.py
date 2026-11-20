# DICTO · dictospheres.com — a convex-cell complex of space-time (x, y, t) for the figures: the Voronoi tessellation of
# Poisson seeds (the space-time Poisson–Voronoi model of studies/2026-11-15-tissue-null-models), with its corners, the index
# of every corner in the sweep by t, and the event each corner shows (Theorem 1(a)). Cells are convex polytopes cut from
# their halfspaces (Qhull), optionally clipped by a box; sections by planes t = c are convex polygons.
# Corner = Delaunay tetrahedron (four seeds); its four edges go to the circumcentres of the four neighbouring tetrahedra;
# the edge e_j across the face opposite seed j lies on every cell of the corner except cell j (Lemma 1).
import numpy as np
from scipy.spatial import Delaunay, HalfspaceIntersection, ConvexHull
from scipy.optimize import linprog

EPS = 1e-9


class Complex:
    def __init__(self, seeds):
        self.S = np.asarray(seeds, float); self.D = Delaunay(self.S)
        T = self.S[self.D.simplices]
        # circumcentres
        A = 2 * (T[:, 1:] - T[:, :1]); b = (T[:, 1:] ** 2).sum(2) - (T[:, :1] ** 2).sum(2)
        ok = np.abs(np.linalg.det(A)) > 1e-12; self.CC = np.full((len(T), 3), np.nan)   # flat tetrahedra (on a lattice's hull): no corner
        self.CC[ok] = np.linalg.solve(A[ok], b[ok][..., None])[..., 0]
        ptr, ind = self.D.vertex_neighbor_vertices; self.nb = [ind[ptr[i]:ptr[i + 1]] for i in range(len(self.S))]

    def corner(self, k):
        """(index, kinds): the index of corner k in the sweep by t and its event, or None at the hull."""
        nbr = self.D.neighbors[k]
        if (nbr < 0).any() or np.isnan(self.CC[nbr]).any() or np.isnan(self.CC[k]).any(): return None
        down = [self.CC[nbr[j]][2] < self.CC[k][2] for j in range(4)]
        i = sum(down); sd = self.D.simplices[k]
        if i == 1: ev = ('birth', [int(sd[j]) for j in range(4) if down[j]])        # the cell born: the one without the down edge
        elif i == 3: ev = ('death', [int(sd[j]) for j in range(4) if not down[j]])  # the cell dying: the one without the up edge
        elif i == 2: ev = ('swap', {'before': [int(sd[j]) for j in range(4) if not down[j]],   # these two touch below
                                    'after': [int(sd[j]) for j in range(4) if down[j]]})       # these two touch above
        else: ev = ('index %d' % i, [])
        return i, ev

    def halfspaces(self, i):
        s = self.S[i]; H = []
        for j in self.nb[i]:
            n = self.S[j] - s; H.append(np.r_[n, -(self.S[j] @ self.S[j] - s @ s) / 2])
        return np.array(H)

    def cell(self, i, box=None):
        """Cell i (∩ box = (lo, hi) if given) as a Poly."""
        H = self.halfspaces(i)
        if box is not None: H = np.vstack([H, box_halfspaces(*box)])
        return Poly.from_halfspaces(H)

    def corners_of(self, i):
        return [k for k in np.where((self.D.simplices == i).any(1))[0]]


def box_halfspaces(lo, hi):
    H = []
    for a in range(3):
        e = np.zeros(3); e[a] = 1
        H.append(np.r_[e, -hi[a]]); H.append(np.r_[-e, lo[a]])
    return np.array(H)


class Poly:
    """A convex polytope: corners V, faces (corner cycles, outward), the plane of each face."""
    def __init__(self, V, faces, planes):
        self.V, self.faces, self.planes = V, faces, planes
        self.edges = sorted({tuple(sorted((a, b))) for o in faces for a, b in zip(o, o[1:] + o[:1])})

    @staticmethod
    def from_halfspaces(H):
        A, b = H[:, :3], -H[:, 3]                 # A x <= b
        nrm = np.linalg.norm(A, axis=1)
        res = linprog(np.r_[0, 0, 0, -1], A_ub=np.c_[A, nrm], b_ub=b, bounds=[(None, None)] * 3 + [(0, None)], method='highs')
        if res.status != 0 or res.x[3] < 1e-7: return None
        hs = HalfspaceIntersection(H, res.x[:3])
        P = hs.intersections; V = []
        for p in P:
            if not any(np.linalg.norm(p - q) < 1e-8 for q in V): V.append(p)
        V = np.array(V); faces, planes = [], []
        for h in H:
            n = h[:3] / np.linalg.norm(h[:3]); d = -h[3] / np.linalg.norm(h[:3])
            on = [k for k in range(len(V)) if abs(V[k] @ n - d) < 1e-8]
            if len(on) < 3: continue
            c = V[on].mean(0); u = V[on[0]] - c; u /= np.linalg.norm(u); w = np.cross(n, u)
            on = sorted(on, key=lambda k: np.arctan2((V[k] - c) @ w, (V[k] - c) @ u))
            faces.append(on); planes.append((n, d))
        poly = Poly(V, faces, planes)
        assert poly.convex_ok(), 'not a convex polytope'
        return poly

    def convex_ok(self):
        nV, nE, nF = len(self.V), len(self.edges), len(self.faces)
        if nV - nE + nF != 2: return False
        return all((self.V @ n - d <= 1e-7).all() for n, d in self.planes)

    def section(self, c, axis=2):
        """The section by the plane x_axis = c, as a convex polygon (counter-clockwise), or None."""
        P = []
        for a, b in self.edges:
            ha, hb = self.V[a][axis], self.V[b][axis]
            if (ha - c) * (hb - c) < 0: s = (c - ha) / (hb - ha); P.append(self.V[a] + s * (self.V[b] - self.V[a]))
        if len(P) < 3: return None
        P = np.array(P); Q = np.delete(P, axis, 1); c2 = Q.mean(0)
        o = np.argsort(np.arctan2(Q[:, 1] - c2[1], Q[:, 0] - c2[0])); Q = Q[o]
        assert len(ConvexHull(Q).vertices) == len(Q), 'section not convex'
        return Q

    def centroid(self):
        return self.V.mean(0)
