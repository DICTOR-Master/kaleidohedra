# DICTO · dictospheres.com — the nine most regular space-fillers (DICTO's census in the Kaleidohedra app: every equal-edged
# space-filling zonohedron whose faces are only squares, regular hexagons and 60° rhombi), built exactly as zonohedra of their
# edge directions (generators as in the app's Polyhedraverse shapes, krp-core regular-nine and the five shapes it names), with
# exact checks in sympy: every edge 1, every face a square, a regular hexagon or a 60° rhombus, and the Dehn invariant zero
# edge by edge (every dihedral angle a rational multiple of π, or the edges at θ and at π − θ cancelling for each θ).
# Also records whether all face normals meet at angles in ℚπ (then Theorem 7 (i) applies as stated).
import itertools, json, os
import numpy as np
import sympy as sp
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
h, r2, r3, r6 = sp.Rational(1, 2), sp.sqrt(2), sp.sqrt(3), sp.sqrt(6)
U, V60, X120, Z = (1, 0, 0), (h, r3 / 2, 0), (-h, r3 / 2, 0), (0, 0, 1)
BAIN = [(h, h, r2 / 2), (h, -h, -r2 / 2), (-h, h, -r2 / 2), (-h, -h, r2 / 2)]
NINE = [  # name, generators, faces (for the label), key in the app
    ('cube', [U, (0, 1, 0), Z], '6 squares', 'CUBE'),
    ('60° rhombohedron', [U, V60, (h, r3 / 6, sp.sqrt(sp.Rational(2, 3)))], '6 rhombi of 60°', 'RHOMBOHEDRON_60'),
    ('leaning square prism', [U, (0, 1, 0), (h, h, r2 / 2)], '2 squares, 4 rhombi of 60°', 'LEANING_SQUARE_PRISM'),
    ('60° rhombic prism', [U, V60, Z], '2 rhombi of 60°, 4 squares', 'RHOMBIC_PRISM_60'),
    ('hexagonal prism', [U, V60, X120, Z], '2 regular hexagons, 6 squares', 'PRISM_6'),
    ('60° leaning hexagonal prism', [U, V60, X120, (0, 1 / r3, sp.sqrt(sp.Rational(2, 3)))], '2 hexagons, 2 squares, 4 rhombi', 'LEANING_HEX_PRISM_60'),
    ('Bain rhombic dodecahedron', BAIN, '4 squares, 8 rhombi of 60°', 'BAIN_RD'),
    ('regular-hexagon elongated dodecahedron', BAIN + [U], '4 hexagons, 4 squares, 4 rhombi', 'REGULAR_HEX_ED'),
    ('truncated octahedron', [(1, 1, 0), (1, -1, 0), (1, 0, 1), (1, 0, -1), (0, 1, 1), (0, 1, -1)], '8 regular hexagons, 6 squares', 'TRUNCATED_OCTAHEDRON'),
]
RATCOS2 = {sp.Integer(0), sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(3, 4), sp.Integer(1)}   # cos² of the angles kπ/12 (quadratic ones)
S = lambda x: sp.nsimplify(sp.radsimp(sp.expand(x)))
dot = lambda a, b: S(sum(x * y for x, y in zip(a, b)))
cross = lambda a, b: (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
sub = lambda a, b: tuple(x - y for x, y in zip(a, b))


class Zono:
    def __init__(s, name, gens, label, key):
        s.name, s.label, s.key = name, label, key
        g = [tuple(sp.nsimplify(x) if not isinstance(x, sp.Basic) else x for x in v) for v in gens]
        if key == 'TRUNCATED_OCTAHEDRON': g = [tuple(x / r2 for x in v) for v in g]          # unit edges
        assert all(dot(v, v) == 1 for v in g), name
        pts = [tuple(S(sum(e * v[i] for e, v in zip(eps, g)) / 2) for i in range(3)) for eps in itertools.product((1, -1), repeat=len(g))]
        Pf = np.array([[float(x) for x in p] for p in pts]); H = ConvexHull(Pf); keep = sorted(set(H.vertices))
        idx = {}; s.V = []
        for i in keep:
            k = tuple(np.round(Pf[i], 9))
            if k not in idx: idx[k] = len(s.V); s.V.append(pts[i])
        Vf = s.vf(); groups = {}
        for simp, eq in zip(H.simplices, H.equations):
            groups.setdefault(tuple(np.round(eq, 7)), set()).update(idx[tuple(np.round(Pf[i], 9))] for i in simp)
        s.F = []
        for ids in groups.values():
            ids = list(ids); a, b, c = (s.V[i] for i in ids[:3]); n = tuple(S(x) for x in cross(sub(b, a), sub(c, a))); d = dot(n, a)
            if any(float(dot(n, v) - d) > 1e-9 for v in s.V): n = tuple(-x for x in n); d = -d
            assert all(dot(n, s.V[i]) == d for i in ids)                                        # planar, exactly
            ce = Vf[ids].mean(0); nf = np.array([float(x) for x in n]); nf /= np.linalg.norm(nf)
            u = Vf[ids[0]] - ce; u /= np.linalg.norm(u); w = np.cross(nf, u)
            ids.sort(key=lambda i: np.arctan2((Vf[i] - ce) @ w, (Vf[i] - ce) @ u)); s.F.append((n, d, ids))
        E = {}
        for k, f in enumerate(s.F):
            for a, b in zip(f[2], f[2][1:] + f[2][:1]): E.setdefault(tuple(sorted((a, b))), []).append(k)
        assert all(len(x) == 2 for x in E.values()) and len(s.V) - len(E) + len(s.F) == 2
        s.E = []; s.kinds = {}
        for (a, b), (i, j) in sorted(E.items()):
            e = sub(s.V[a], s.V[b]); assert dot(e, e) == 1, (name, 'edge')
            n1, n2 = s.F[i][0], s.F[j][0]; p = dot(n1, n2); c2 = S(p * p / (dot(n1, n1) * dot(n2, n2)))
            rat = c2 in RATCOS2; sg = -int(sp.sign(p))                                              # sign of cos(dihedral)
            s.E.append((a, b, 1, (c2, sg), rat))
        for k, (n, d, o) in enumerate(s.F):                                                         # face shapes, exactly
            cs = []
            for t in range(len(o)):
                p0, p1, p2 = s.V[o[t - 1]], s.V[o[t]], s.V[o[(t + 1) % len(o)]]
                cs.append(dot(sub(p0, p1), sub(p2, p1)))                                           # cos of the corner angle (unit edges)
            kind = {4: {(0,): 'square', (-h, h): 'rhombus 60°'}, 6: {(-h,): 'regular hexagon'}}[len(o)][tuple(sorted(set(cs)))]
            s.kinds[kind] = s.kinds.get(kind, 0) + 1

    def vf(s): return np.array([[float(x) for x in v] for v in s.V])

    def dehn_zero(s):
        """Σ length ⊗ angle = 0 mod ℚπ: for each irrational θ = arccos|cos|, the edges at θ (cos > 0) and at π − θ (cos < 0) cancel."""
        # arccos(1/√3) ≡ −½ arccos(1/3) mod ℚπ, since 2 arccos(1/√3) = π − arccos(1/3) (as in the proof of Theorem 8)
        RED = {sp.Rational(1, 3): (sp.Rational(1, 9), -h)}
        bal = {}; seen = set()
        for a, b, l, (c2, sg), rat in s.E:
            if rat: continue
            seen.add(c2); base, f = RED.get(c2, (c2, 1)); bal[base] = bal.get(base, 0) + sg * l * f
        return all(v == 0 for v in bal.values()), sorted(float(sp.acos(sp.sqrt(c))) * 180 / np.pi for c in seen)

    def normals_rational(s):
        N = [n for n, d, o in s.F]
        return all(S(dot(a, b) ** 2 / (dot(a, a) * dot(b, b))) in RATCOS2 for a, b in itertools.combinations(N, 2))


def build():
    out = []
    for name, gens, label, key in NINE:
        Zz = Zono(name, gens, label, key); ok, irr = Zz.dehn_zero(); assert ok, name
        out.append((Zz, irr, Zz.normals_rational()))
    return out


if __name__ == '__main__':
    log = []
    for Zz, irr, nr in build():
        log.append(f'{Zz.name}: {len(Zz.V)} corners, {len(Zz.F)} faces {Zz.kinds}, {len(Zz.E)} edges of length 1; Dehn invariant 0 '
                   + ('(every dihedral angle in ℚπ)' if not irr else f'(edges at θ and π − θ cancel, with 2 arccos(1/√3) = π − arccos(1/3), for θ = {", ".join(f"{x:.4f}°" for x in irr)})')
                   + ('; all face normals at angles in ℚπ: Theorem 7 (i) applies' if nr else ''))
    open(os.path.join(HERE, 'nine-fillers.log'), 'w').write('\n'.join(log) + '\nFINAL ok\n'); print('\n'.join(log)); print('FINAL ok')
