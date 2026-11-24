# Exact proof for every "shadow die" found by scan_shadow.py: a die whose faces project from the centre onto unions of
# fundamental triangles of G (Oh: 48 triangles; Ih: 120), equally many per face, hence fair exactly.
# For each hit:
#  1. each corner is put on its axis direction a_v (exact, in Q(sqrt5)^3); unknown corner radii lam_v and plane offsets h_i
#     (plane q_i.x = h_i, q_i the exact unnormalised normal) solve q_i.a_v lam_v = h_i on every incidence, h_1 = 1 (exact, Q(sqrt5));
#  2. every incidence holds exactly and every corner is strictly inside every other plane (exact signs), so these are the corners
#     of P = {q_i.x <= h_i}: each face's corners, in cyclic order, have every side a supporting line (exact), each side is shared by
#     exactly two faces, so the listed faces form a closed surface = the boundary of conv(corners), and conv(corners) = P;
#  3. every side of every face projects into a mirror of G (n.a_v = n.a_w = 0 exactly), so the projection of each face is a union
#     of fundamental triangles; its area (arb) divided by 4 pi/|G| is the integer k_i (enclosure width < 1/2 around one integer);
#  4. fair iff every k_i = |G|/N.  By Alexandrov's uniqueness (prescribed normals and solid angles fix the polytope up to scale)
#     this exact die is the catalogue die, whose depths it gives in closed form.
# usage: prove_shadow.py HITS.json OUT.json
import json, sys, os
from fractions import Fraction as Q
import numpy as np
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from groups import DIRS, DFAM
from qsqrt5 import K, PHI, IPHI, dot, cross, sub, scl, cyc_signs
from scan_shadow import corners, GROUPS
from flint import arb, ctx
ctx.prec = 200
ONE, Z = K(1), K(0)
PAT = {'C6': (ONE, Z, Z), 'O8': (ONE, ONE, ONE), 'RD12': (ONE, ONE, Z), 'D12': (Z, PHI, ONE), 'I12': (Z, IPHI, PHI), 'RT24': (ONE, PHI, IPHI),
       'D12p': (Z, ONE, PHI), 'I12p': (Z, PHI, IPHI), 'RT24p': (PHI, ONE, IPHI)}
EX = []
for v, f in zip(DIRS, DFAM):
    m = [w for w in cyc_signs(PAT[f]) if np.abs(np.array([float(x) for x in w]) / np.linalg.norm([float(x) for x in w]) - v).max() < 1e-9]
    assert len(m) == 1; EX.append(m[0])
def arbv(v): s5 = arb(5).sqrt(); return [arb(x.a.numerator) / x.a.denominator + arb(x.b.numerator) / x.b.denominator * s5 for x in v]
def sph_area(P):
    P = [arbv(v) for v in P]; tot = arb(0)
    def d3(a, b, c): return a[0] * (b[1] * c[2] - b[2] * c[1]) - a[1] * (b[0] * c[2] - b[2] * c[0]) + a[2] * (b[0] * c[1] - b[1] * c[0])
    def dt(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
    for i in range(1, len(P) - 1):
        a, b, c = P[0], P[i], P[i + 1]
        la, lb, lc = dt(a, a).sqrt(), dt(b, b).sqrt(), dt(c, c).sqrt()
        tot += 2 * arb.atan2(abs(d3(a, b, c)), la * lb * lc + dt(a, b) * lc + dt(a, c) * lb + dt(b, c) * la)
    return tot
def ksym(x): return sp.Rational(x.a.numerator, x.a.denominator) + sp.Rational(x.b.numerator, x.b.denominator) * sp.sqrt(5)
def prove(r):
    g = GROUPS[r['G']]; order = g['order']; idx = r['idx']; N = len(idx)
    axes = [i for i, f in enumerate(DFAM) if f in g['axes']]; mirrors = [EX[i] for i, f in enumerate(DFAM) if f in g['mirrors']]
    V, inc = corners(idx, r['sizes'], np.array(r['depths'], float))
    Vn = V / np.linalg.norm(V, axis=1)[:, None]
    A = [EX[axes[int(np.abs(DIRS[axes] - v).max(1).argmin())]] for v in Vn]
    q = [EX[i] for i in idx]
    h = [None] * N; lam = [None] * len(V); h[0] = ONE; todo = True
    while todo:
        todo = False
        for v, I in enumerate(inc):
            for i in I:
                if h[i] is not None and lam[v] is None: lam[v] = h[i] / dot(q[i], A[v]); todo = True
                if lam[v] is not None and h[i] is None: h[i] = lam[v] * dot(q[i], A[v]); todo = True
    assert all(x is not None for x in h + lam)
    P = [scl(lam[v], A[v]) for v in range(len(V))]
    ok_inc = all((h[i] - dot(q[i], P[v])).sign() == (0 if i in inc[v] else 1) for v in range(len(V)) for i in range(N))
    # faces: cyclic order, supporting sides, each side in two faces
    edges = {}; ok_side = True; ok_mirror = True; ks = []
    for i in range(N):
        S = [v for v in range(len(V)) if i in inc[v]]
        if len(S) < 3: return dict(ok=False, why='face with < 3 corners')
        c = V[S].mean(0); e1 = V[S[0]] - c; e2 = np.cross(DIRS[idx[i]], e1)
        S = sorted(S, key=lambda v: np.arctan2((V[v] - c) @ e2, (V[v] - c) @ e1))
        for a in range(len(S)):
            v, w = S[a], S[(a + 1) % len(S)]
            sg = {dot(q[i], cross(sub(P[w], P[v]), sub(P[x], P[v]))).sign() for x in S if x not in (v, w)}
            ok_side &= len(sg) == 1 and 0 not in sg
            edges[frozenset((v, w))] = edges.get(frozenset((v, w)), 0) + 1
            ok_mirror &= any(dot(n, A[v]).sign() == 0 and dot(n, A[w]).sign() == 0 for n in mirrors)
        ar = sph_area([A[v] for v in S]) * order / (4 * arb.pi())
        k = int(round(float(ar.mid())))
        ok_k = bool(abs(ar - k) < arb(1) / 4)
        if not ok_k: return dict(ok=False, why='area not near an integer')
        ks.append(k)
    ok_closed = all(c == 2 for c in edges.values())
    fair = all(k * N == order for k in ks)
    # exact depths d_i = h_i / |q_i| relative to d of face 0; one per orbit
    cut = np.cumsum([0] + r['sizes'])[:-1]
    dep = [sp.radsimp(sp.nsimplify(ksym(h[c]) / sp.sqrt(ksym(dot(q[c], q[c]))) / (ksym(h[0]) / sp.sqrt(ksym(dot(q[0], q[0])))))) for c in cut]
    rel = [float(r['depths'][j]) / float(r['depths'][0]) for j in range(len(cut))]
    agree = max(abs(float(d) - x) for d, x in zip(dep, rel))
    ok_same = all(abs(float(ksym(h[i]) / sp.sqrt(ksym(dot(q[i], q[i])))) - float(dep[list(cut).index(max(c for c in cut if c <= i))] * ksym(h[0]) / sp.sqrt(ksym(dot(q[0], q[0]))))) < 1e-12 for i in range(N))
    return dict(ok=bool(ok_inc and ok_side and ok_closed and ok_mirror and fair and agree < 1e-9 and ok_same), incidences_exact=ok_inc, sides_supporting=ok_side,
                closed_surface=ok_closed, sides_on_mirrors=ok_mirror, triangles_per_face=sorted(set(ks)), fair=fair, corners=len(V),
                depth_ratios=[str(d) for d in dep], depth_ratios_float=[float(d) for d in dep], catalogue_agree=agree,
                corner_axes=sorted({DFAM[axes[int(np.abs(DIRS[axes] - v).max(1).argmin())]] for v in Vn}))
if __name__ == '__main__':
    hits = json.load(open(sys.argv[1])); out = []; allok = True
    for r in hits:
        res = prove(r); allok &= res['ok']
        out.append(dict(src=r['src'], sid=r['sid'], group=r['group'], N=r['N'], label=r['label'], G=r['G'], **res))
        print(r['G'], r['src'].split('/')[-1], r['sid'], r['group'], 'N', r['N'], r['label'], '|', {k: v for k, v in res.items() if k not in ('depth_ratios_float',)}, flush=True)
    json.dump(out, open(sys.argv[2], 'w'), indent=1)
    print('proved %d of %d' % (sum(o['ok'] for o in out), len(out)))
    print('FINAL ok' if allok else 'FINAL FAIL')
