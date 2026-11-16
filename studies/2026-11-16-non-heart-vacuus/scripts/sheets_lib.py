# Vacuus as slotted sheets (16 Nov 2026, after DICTO: "better vacuus figures but they don't appear as vacuus in the figures").
# Exact part: the 3D cross-section of a 4D Vacuus through its centre.
# A plate (fin) of a 4D shape is the cone from the centre over one 2-face R. A 3D hyperplane H through the centre (normal u) cuts
# that cone in the cone from the centre over R ∩ H, i.e. in a flat triangle (centre, p, q), where p, q are the two points where H
# crosses the boundary of R (corners of R on H, or points where H crosses a side of R). All arithmetic is exact in Q(sqrt5)
# (q5.Q5, reused from study 2026-10-27-4d-shadows through the Queens' vicinity library). Every piece is checked exactly: p and q
# lie on the plate (n . p = n . q = 0, n the plate normal from the 2-face) and on H (u . p = u . q = 0).
import os, sys
from fractions import Fraction as Fr
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '2026-11-16-queens-vicinity-vacuus', 'scripts'))
import qv_lib as L  # noqa: E402
from qv_lib import Q5, ZERO, ONE, PHI, dot, cross4, canon, key, neg, fl  # noqa: E402,F401


def plate_normal(V, R):
    R = list(R); a = R[0]
    for b in R[1:]:
        for c in R[2:]:
            if c == b: continue
            n = cross4(V[a], V[b], V[c])
            if any(not x.iszero() for x in n): return canon(n)
    raise ValueError('degenerate 2-face')


def section(V, edges, ridges, u):
    """V exact 4D corners (centre at the origin), edges (i, j), ridges = vertex sets of the 2-faces, u exact normal of H.
    Returns the pieces [{'plate': key, 'ridge': R, 'p': exact, 'q': exact}] and the number of exact checks passed."""
    s = [dot(v, u) for v in V]
    eset = {tuple(sorted(e)) for e in edges}
    pieces, nchk = [], 0
    for R in ridges:
        Rs = set(R); n = plate_normal(V, R)
        for i in R:
            assert dot(V[i], n).iszero()
        pts = {}
        for i in R:
            if s[i].iszero(): pts[key(V[i])] = V[i]
        for (i, j) in eset:
            if i in Rs and j in Rs and s[i].sign() * s[j].sign() < 0:
                t = s[i] / (s[i] - s[j]); p = tuple(V[i][k] + t * (V[j][k] - V[i][k]) for k in range(4)); pts[key(p)] = p
        assert all(not s[i].iszero() for i in R) or len(pts) <= 2 or False, 'a 2-face lies in H'
        if len(pts) < 2: continue
        assert len(pts) == 2, ('H meets a 2-face in more than two boundary points', len(pts))
        p, q = list(pts.values())
        for x in (p, q):
            assert dot(n, x).iszero(), 'piece corner off its plate'
            assert dot(u, x).iszero(), 'piece corner off the hyperplane'
            nchk += 2
        pieces.append({'plate': key(n), 'ridge': frozenset(R), 'p': p, 'q': q})
    return pieces, nchk


def classify(pieces, ridges_per_plate):
    """per piece: 'through' = its opposite piece (-p, -q) is on the same plate (a sheet through the centre);
    'shared' = its plate carries two or more 2-faces but the opposite piece is absent; 'single' = its plate carries one 2-face."""
    by = {}
    for pc in pieces: by.setdefault(pc['plate'], set()).add(frozenset((key(pc['p']), key(pc['q']))))
    out = []
    for pc in pieces:
        opp = frozenset((key(neg(pc['p'])), key(neg(pc['q']))))
        if opp in by[pc['plate']]: out.append('through')
        elif ridges_per_plate[pc['plate']] >= 2: out.append('shared')
        else: out.append('single')
    return out


def ortho_basis(rows, against):
    """orthonormal float basis of the span of `rows` projected off the unit vectors in `against`."""
    B = []
    for r in rows:
        v = np.array(r, float)
        for a in list(against) + B: v = v - (v @ a) * a
        if np.linalg.norm(v) > 1e-9: B.append(v / np.linalg.norm(v))
    return np.array(B)
