# Kepler cycle of TI: S0 = TI, tips by Kepler's first stellation along each face axis (pentagon tips = corners of TI's own icosahedron,
# hexagon tips = corners of its own dodecahedron), S1 = hull of the tips, S2 = hull of S1's Kepler tips (shape of TI again, x (105-18sqrt5)/55).
# Checks: (1) the shape of S1 against the Star Halo, the Catalan pentakis dodecahedron, the core, the dataset's FPD/Palintriacontahedron;
# (2) nesting S0 ⊂ star ⊂ S1 and S1 ⊂ star1 ⊂ S2; (3) exact fill of each layer by corner pyramids and edge tetrahedra (volume and
# overlaps), with the outer solid of each layer the next S (not s.S as in the TI Star).
import json, itertools, numpy as np
from fractions import Fraction as Fr
from scipy.spatial import ConvexHull, HalfspaceIntersection
phi = (1 + 5 ** .5) / 2
raw = json.load(open('data/stations-exact.json'))
P = np.array([[float(Fr(a)) + float(Fr(b)) * 5 ** .5 for a, b in v] for v in raw['TI']])
def facelist(Q):
    hq = ConvexHull(Q); V = Q[hq.vertices]; out = {}
    for eq in hq.equations:
        k = tuple(np.round(eq, 7))
        if k not in out: out[k] = (eq, [i for i, p in enumerate(V) if abs(eq[:3] @ p + eq[3]) < 1e-8])
    return V, list(out.values())
def ktips(V, FL):
    T = []
    for fi, (eq, ids) in enumerate(FL):
        n = eq[:3]; d = -eq[3]; best = None
        for fj, (eq2, ids2) in enumerate(FL):
            if fj == fi or len(set(ids) & set(ids2)) < 2: continue
            den = eq2[:3] @ n
            if abs(den) < 1e-12: continue
            lam = -eq2[3] / den
            if lam > d + 1e-9 and (best is None or lam < best): best = lam
        T.append(best * n)
    return T
def shape(V):
    W = V / np.linalg.norm(V, axis=1).max(); d = np.linalg.norm(W[:, None] - W[None], axis=2)
    return (len(W), tuple(sorted({round(x, 6) for x in d.ravel() if x > 1e-9})[:5]), tuple(sorted({round(x, 6) for x in np.linalg.norm(W, axis=1)})))
def pl(Q):
    u = {}
    for eq in ConvexHull(Q).equations: u.setdefault(tuple(np.round(eq, 7)), eq)
    return np.array(list(u.values()))
cut = lambda H: (lambda W: W[ConvexHull(W).vertices])(HalfspaceIntersection(H, np.zeros(3)).intersections)
inside = lambda A, B: bool(np.all(A @ pl(B)[:, :3].T + pl(B)[:, 3] <= 1e-9))
vol = lambda Q: ConvexHull(Q).volume
# reference shapes
V0, F0 = facelist(P)
feet = np.array([(-eq[3]) * eq[:3] for eq, _ in F0])
starhalo = feet                                   # hull of TI's face feet: Star Halo shape
catalan = cut(np.hstack([V0, -np.ones((len(V0), 1))]))
pen = np.array([phi * V0[ids].mean(0) for _, ids in F0 if len(ids) == 5]); hexa = np.array([phi * V0[ids].mean(0) for _, ids in F0 if len(ids) == 6])
core = cut(np.vstack([pl(pen), pl(hexa)]))
def rd(p):
    L = [l.split('#')[0].strip() for l in open(p)]; L = [l for l in L if l]; n = int(L[1].split()[0]); A = np.array([[float(x) for x in L[2 + i].split()[:3]] for i in range(n)]); return A - A.mean(0)
import os
refs = {'Star Halo': starhalo, 'Catalan pentakis': catalan, 'core (1/phi^3)': core}
for nm, f in [('FPD / Palintriacontahedron', '/home/dicto/kres-tmp/census/solids/dicto-fpd.off'), ('GTI', '/home/dicto/kres-tmp/census/solids/dicto-gti.off')]:
    if os.path.exists(f): refs[nm] = rd(f)
def layer(S, nxt):
    V, FL = facelist(S); T = ktips(V, FL)
    fa = {v: [fi for fi, (_, ids) in enumerate(FL) if v in ids] for v in range(len(V))}
    def is_edge(a, b):
        fs = [fi for fi in fa[a] if fi in fa[b]]
        if len(fs) != 2: return False
        m = (V[a] + V[b]) / 2; return all(abs(FL[f][0][:3] @ m + FL[f][0][3]) < 1e-8 for f in fs)
    E = [e for e in itertools.combinations(range(len(V)), 2) if is_edge(*e)]
    spikes = [np.vstack([V[ids], T[fi]]) for fi, (_, ids) in enumerate(FL)]
    star = vol(V) + sum(vol(Q) for Q in spikes); TP = np.array(T)
    L1 = [np.vstack([V[v]] + [T[f] for f in fa[v]]) for v in range(len(V))] + [np.vstack([V[a], V[b]] + [T[f] for f in fa[a] if f in fa[b]]) for a, b in E]
    ok = abs(sum(map(vol, L1)) - (vol(TP) - star)) < 1e-9 * vol(TP)
    return TP, dict(star_over_S=star / vol(V), hull_over_S=vol(TP) / vol(V), spikes=len(spikes), fill_pieces=len(L1), fill_exact=bool(ok),
                    star_inside_hull=all(inside(Q, TP) for Q in spikes)), [V] + spikes + L1
S1, info0, pieces0 = layer(P, None); S2, info1, pieces1 = layer(S1, None)
out = dict(step0=info0, step1=info1,
           S1_corners=len(ConvexHull(S1).vertices), S1_same_shape_as=[k for k, v in refs.items() if shape(v[ConvexHull(v).vertices]) == shape(S1[ConvexHull(S1).vertices])],
           S1_radius_ratio=float(np.linalg.norm(S1, axis=1).max() / np.linalg.norm(S1, axis=1).min()),
           S2_is_TI_shape=shape(S2[ConvexHull(S2).vertices]) == shape(P), factor=float(np.linalg.norm(S2, axis=1).max() / np.linalg.norm(P, axis=1).max()))
# overlaps in layer 0 (TI + spikes + fill)
def axes(Q):
    hq = ConvexHull(Q); n = [eq[:3] for eq in hq.equations]
    ed = {tuple(sorted((a, b))) for sm in hq.simplices for a, b in [(sm[0], sm[1]), (sm[1], sm[2]), (sm[0], sm[2])]}
    return n, [Q[b] - Q[a] for a, b in ed]
def overlaps(pieces):
    AX = [axes(Q) for Q in pieces]; C = [Q.mean(0) for Q in pieces]; Rr = [np.linalg.norm(Q - Q.mean(0), axis=1).max() for Q in pieces]; bad = 0
    for i, j in itertools.combinations(range(len(pieces)), 2):
        if np.linalg.norm(C[i] - C[j]) > Rr[i] + Rr[j] + 1e-9: continue
        ok = False
        for ax in AX[i][0] + AX[j][0] + [np.cross(u, v) for u in AX[i][1] for v in AX[j][1]]:
            nn = np.linalg.norm(ax)
            if nn < 1e-12: continue
            pa, pb = pieces[i] @ (ax / nn), pieces[j] @ (ax / nn)
            if pa.max() <= pb.min() + 1e-9 or pb.max() <= pa.min() + 1e-9: ok = True; break
        bad += not ok
    return bad
out['overlaps_step0'] = overlaps(pieces0); out['overlaps_step1'] = overlaps(pieces1)
print(json.dumps(out, indent=1, default=float)); json.dump(out, open('data/kepler-cycle.json', 'w'), indent=1, default=float)
