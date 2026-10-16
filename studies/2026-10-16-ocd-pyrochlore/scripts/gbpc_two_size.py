# Fable, GBPC two-size question (2026-10-16, pass 2 on DICTO's go). Exact in Q(sqrt5) unless a line says FLOAT.
# Can G' (golden region minus the 24 GBPCs per bcc cell) be tiled by big prolates (edge lam = phi/9 |v|) and phi-smaller oblates (edge 1/9 |v|)?
# 1. face-to-face: tiles that share a face share its edges, so all tiles in a connected face-to-face tiling have one edge length.
# 2. any tiling: each 36-degree convex edge of G' must be covered, end to end, by acute (36-degree) edges of oblates; check its ends are blocked.
# 3. check of the Galois count on a known case: the Ammann-Kramer tiling (A = 0) must come out prolate:oblate = phi:1.
import sys, io, os, contextlib, itertools, json, numpy as np
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); STUDY = os.path.dirname(HERE)
src = open(os.path.join(HERE, 'golden_fill.py')).read().split('# ---- all bodies')[0]
cwd = os.getcwd(); os.chdir(STUDY)
with contextlib.redirect_stdout(io.StringIO()):
    exec(src)
os.chdir(cwd)
out = []; say = lambda s: (print(s, flush=True), out.append(s))
say("DICTO · dictospheres.com — Fable, GBPC two-size question (exact in Q(sqrt5) unless marked FLOAT)")
phi = Q(Fr(1, 2), Fr(1, 2)); sig = lambda x: Q(x.a, -x.b)
v5 = AX['5']
# ---- golden rhombohedra: dihedral angles exactly (cos^2 of the angle between face normals)
def dihedral_cos2(u, v, w):   # dihedral along edge u between faces (u,v) and (u,w), as cos^2 and the sign of cos
    n1, n2 = cross(u, v), cross(u, w)
    # interior angle: between the half-planes containing v and w; cos = (n1.n2)/(|n1||n2|) with orientation fixed below
    c = dot(n1, n2); c2 = c * c / (dot(n1, n1) * dot(n2, n2))
    # sign of cos of the interior dihedral angle = sign of (v_perp . w_perp)
    vp = sub(mul(v, dot(u, u)), mul(u, dot(u, v))); wp = sub(mul(w, dot(u, u)), mul(u, dot(u, w)))
    return c2, sgn(dot(vp, wp))
kinds = {}
for a, b, c in itertools.combinations(v5, 3):
    d = det3(a, b, c); d = d if sgn(d) > 0 else -d
    angs = set()
    for u, v, w in ((a, b, c), (b, a, c), (c, a, b)):
        for sv in (1, -1):
            for sw in (1, -1):
                angs.add(dihedral_cos2(u, mul(v, Q(sv)), mul(w, Q(sw))))
    kinds.setdefault(repr(d), (d, angs))
dO, dP = sorted([k[0] for k in kinds.values()], key=lambda x: x.f())
cos36sq = phi * phi / 4; cos72sq = (phi - 1) * (phi - 1) / 4
acute = {repr(d): any(c2 == cos36sq and s > 0 for c2, s in angs) for d, angs in kinds.values()}
say(f"golden rhombohedra spanned by three five-fold vectors: volumes {dO!r} (oblate) and {dP!r} (prolate) = phi x oblate: {dP == dO * phi}")
say(f"36-degree dihedral (cos^2 = phi^2/4, exact): oblate {acute[repr(dO)]}, prolate {acute[repr(dP)]}")
assert acute[repr(dO)] and not acute[repr(dP)]
# ---- the 48 convex 36-degree edges: the GBPC side edges lying in the neighbour's face plane
RT = polytope([(s, max((dot(s, v) for v in OCD), key=lambda x: x.f())) for u in AX['2'] for s in (u, neg(u))])
sites = [[Z, Z, Z]]
for m in itertools.product(range(-3, 4), repeat=3):
    c = add(add(mul(LB[0], Q(m[0])), mul(LB[1], Q(m[1]))), mul(LB[2], Q(m[2])))
    if 0 < np.linalg.norm(fl(c)) < 2.2 * RT['r']: sites.append(c)
def where(x):   # 'in' (inside some uncut RT), 'on' (on the boundary of the union), 'out' (free)
    best = 'out'
    for c in sites:
        s = max(sgn(dot(n, sub(x, c)) - d) for n, d in RT['H'])
        if s < 0: return 'in'
        if s == 0: best = 'on'
    return best
conv = []
for A in ADP:
    nb = [H for H in A['H'] if axtype(H[0]) == '2']
    for i, j in A['E']:
        p, q = A['V'][i], A['V'][j]
        if axtype(sub(q, p)) != '5': continue
        # a convex 36-degree edge has free space on its outer side: the midpoint pushed out of both faces must be free
        conv.append((p, q))
v = next(x for x in v5); vl2 = dot(v, v)
lens = set(); ends = {}
res = []
for p, q in conv:
    d = sub(q, p); ax = next(a for a in v5 if iszero(cross(d, a))); i = next(k for k in range(3) if ax[k] != Z); L = d[i] / ax[i]; L = L if sgn(L) > 0 else -L
    beyond = [where(add(q, mul(d, Q(Fr(1, 1000))))), where(sub(p, mul(d, Q(Fr(1, 1000)))))]
    mid = mul(add(p, q), Q(Fr(1, 2)))
    res.append((repr(L), tuple(sorted(beyond)), where(mid)))
from collections import Counter
say(f"GBPC five-fold side edges (3 per GBPC, 24 GBPCs): length / |v| and what lies just beyond each end, exact: " +
    '; '.join(f'{k[0]}, beyond ends {k[1]}, midpoint {k[2]}: x{n}' for k, n in sorted(Counter(res).items())))
say(f"lengths: phi/9 = {phi / 9!r}; edge of the small oblate 1/9; big edge lam = phi/9")
# ---- for the 48 convex edges: does the free 36-degree wedge continue past either end? (test points inside the wedge, exact)
P5 = AX['5'] + [neg(x) for x in AX['5']]; P3 = AX['3'] + [neg(x) for x in AX['3']]; P2 = AX['2'] + [neg(x) for x in AX['2']]
W = [add(add(a, b), c) for a in P5 for b in P3 for c in P2]; Wf = np.array([fl(w) for w in W])
Hn = np.array([fl(n) for n, d in RT['H']]); Hd = np.array([d.f() for n, d in RT['H']]); Sf = np.array([fl(c) for c in sites])
def freef(X):   # FLOAT prefilter: points (k,3) strictly outside every RT by a margin
    m = np.min(np.max((X[:, None, :] - Sf[None, :, :]) @ Hn.T - Hd, axis=2), axis=1)
    return m > 1e-9
eps = Q(Fr(1, 10**4))
cont = Counter()
for (p, q), r in zip(conv, res):
    if r[1] != ('on', 'on'): continue
    d = sub(q, p); mid = mul(add(p, q), Q(Fr(1, 2)))
    ok = np.where(freef(fl(mid) + 1e-4 * Wf))[0][:6]
    wedge = [W[i] for i in ok if where(add(mid, mul(W[i], eps))) == 'out']
    beyond = []
    for e, sg in ((q, 1), (p, -1)):
        for dl in (Q(Fr(1, 100)), Q(Fr(1, 1000))):
            x = add(e, mul(d, Q(sg) * dl))
            beyond.append(sum(1 for w in wedge if where(add(x, mul(w, eps * dl))) == 'out'))
    cont[(len(wedge), tuple(beyond))] += 1
say("convex edges: sample directions free in the wedge at the midpoint, and how many stay free just past each end at 1/100 and 1/1000 of the edge (exact, after a FLOAT prefilter): "
    + '; '.join(f'{k[0]} at the middle, {k[1]} past the ends: x{n}' for k, n in sorted(cont.items())))
# ---- Galois count, known case: Ammann-Kramer tiling (bounded lift, A = 0): p sigma(vol P) + o sigma(vol O) = 0
ratio = -sig(dO) / sig(dP)
say(f"Ammann-Kramer check: the count with A = 0 gives prolate/oblate = -sigma(vol O)/sigma(vol P) = {ratio!r}; equals phi: {ratio == phi} (known value phi:1)")
open(os.path.join(STUDY, 'data', 'gbpc-two-size.txt'), 'w').write('\n'.join(out) + '\n')
