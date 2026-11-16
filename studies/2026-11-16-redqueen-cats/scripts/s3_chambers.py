#!/usr/bin/env python3
"""120-cell survey, part 3 (DICTO 16 Nov 2026): the chambers cut by ALL the walls used by the golden copies in the 120-cell
(1560 walls, Sym(120-cell)-invariant, containing the 60 H4 mirrors). Symmetry reduction as in studies/2026-11-16-queens-chambers:
every chamber lies in one H4 Coxeter chamber C, so #chambers = 14400 x #(regions of C cut by the walls through its interior).
Exact count: Zaslavsky in the open simplex section of C (regions_in_chamber, open_halfplane, nullspace copied from
studies/2026-11-16-queens-chambers/scripts/chambers.py). Float count: direct splitting of the simplex section, wall by wall.
usage: s3_chambers.py OUTDIR [countonly]"""
import os, sys, json, time, pickle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rq_lib import *
from scipy.spatial import ConvexHull
OUT = sys.argv[1]; COUNTONLY = 'countonly' in sys.argv; C = Checks(); T0 = time.time(); out = {}
def say(*a): print(*a, f'({time.time() - T0:.0f}s)', flush=True)
Z0, O1 = Q5(0), Q5(1)
st = pickle.load(open(os.path.join(OUT, 'state.pkl'), 'rb')); gcat = st['gcat']
Wd = World(); PP = Wd.PP
def dvec(k): return tuple(Q5(a, b) for a, b in k)
walls = [dvec(k) for k, v in sorted(st['gid_keys'], key=lambda x: x[1])]
C(len(walls) == 1560, f'walls used by all the copies: {len(walls)}')
on = PP.facets[0][0]; v = [to5(PP.P[i]) for i in on]
RAYS = [v[0], vadd(v[0], v[1]), vadd(vadd(v[0], v[1]), v[2]), vadd(vadd(vadd(v[0], v[1]), v[2]), v[3])]
def sgns(w): return [dot(w, r).sign() for r in RAYS]
mir = [w for w, c in zip(walls, gcat) if c == 'M']
C(all(0 in sgns(w) or len(set(sgns(w))) == 1 for w in mir), 'no mirror meets the open chamber C (C is an H4 Coxeter chamber: corner, edge midpoint, triangle centre, cell centre)')
C(sum(1 for w in mir if sgns(w).count(0) == 3) == 4, 'exactly 4 mirrors carry 3 of its 4 rays (its 4 walls)')
cut = [w for w in walls if 1 in sgns(w) and -1 in sgns(w)]
from collections import Counter
catcut = Counter(c for w, c in zip(walls, gcat) if 1 in sgns(w) and -1 in sgns(w))
out['walls_cutting_C'] = len(cut); out['walls_cutting_C_by_category'] = dict(catcut)
say('walls through the open chamber C:', len(cut), dict(catcut))
if COUNTONLY:
    json.dump(out, open(os.path.join(OUT, 'chambers_count.json'), 'w'), indent=1); C.final(); sys.exit()

def open_halfplane(a):
    if any(x[0].iszero() and x[1].iszero() for x in a): return False
    cands = list(a) + [(-x[1], x[0]) for x in a] + [(x[1], -x[0]) for x in a]
    cands2 = cands + [(p[0] + q[0], p[1] + q[1]) for p, q in itertools.combinations(cands, 2)]
    return any(all((x[0]*s[0] + x[1]*s[1]).sign() > 0 for x in a) for s in cands2)
def nullspace(rows, n=4):
    M = [list(r) for r in rows]; piv = []; r = 0
    for c in range(n):
        p = next((i for i in range(r, len(M)) if not M[i][c].iszero()), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; iv = M[r][c].inv(); M[r] = [x*iv for x in M[r]]
        for i in range(len(M)):
            if i != r and not M[i][c].iszero():
                f = M[i][c]; M[i] = [x - f*y for x, y in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    B = []
    for f in [c for c in range(n) if c not in piv]:
        vv = [Z0]*n; vv[f] = O1
        for i, c in enumerate(piv): vv[c] = -M[i][f]
        B.append(tuple(vv))
    return B
P = [tuple(dot(w, r) for r in RAYS) for w in cut]; n = len(P)
lines = {}; pair_line = {}; npairs = n*(n - 1)//2; done = 0
for k, l in itertools.combinations(range(n), 2):
    done += 1
    if done % 2000 == 0: print(f'PROGRESS {0.3*done/npairs:.3f} pairs', flush=True)
    if (k, l) in pair_line: continue
    U = nullspace([P[k], P[l]])
    if len(U) != 2: continue
    H = frozenset(m for m in range(n) if dot(P[m], U[0]).iszero() and dot(P[m], U[1]).iszero())
    lines[H] = open_halfplane([(U[0][i], U[1][i]) for i in range(4)])
    for p in itertools.combinations(sorted(H), 2): pair_line[p] = H
inside_lines = [H for H, ok in lines.items() if ok]
say('lines', len(lines), 'inside', len(inside_lines))
pts = {}; ntr = n*(n - 1)*(n - 2)//6; done = 0
for k, l, m in itertools.combinations(range(n), 3):
    done += 1
    if done % 20000 == 0: print(f'PROGRESS {0.3 + 0.6*done/ntr:.3f} triples', flush=True)
    if m in pair_line[(k, l)]: continue
    U = nullspace([P[k], P[l], P[m]])
    if len(U) != 1: continue
    u = U[0]; sg = {x.sign() for x in u}
    if sg not in ({1}, {-1}): continue
    H = frozenset(q for q in range(n) if dot(P[q], u).iszero())
    pts[H] = 1
mu_pts = 0
for H in pts:
    Ls = {pair_line[p] for p in itertools.combinations(sorted(H), 2)}
    mu_pts += sum(len(F) - 1 for F in Ls) - len(H) + 1
r = 1 + n + sum(len(F) - 1 for F in inside_lines) + mu_pts
info = {'planes': n, 'lines_inside': len(inside_lines), 'points_inside': len(pts), 'points_multiple': sum(len(H) > 3 for H in pts),
        'lines_multiple': sum(len(F) > 2 for F in inside_lines)}
say('EXACT regions of C:', r, info)
out['regions_in_C_exact'] = r; out['zaslavsky'] = info; out['chambers_total'] = 14400*r
# float splitting of the simplex section in barycentric coordinates t1, t2, t3 (t4 = 1 - t1 - t2 - t3)
def split(regions, a, b, eps=1e-10):
    o = []
    for R in regions:
        s = R @ a + b
        if s.max() <= eps or s.min() >= -eps: o.append(R); continue
        pos, neg_ = R[s > eps], R[s < -eps]; on_ = R[np.abs(s) <= eps]; sp, sn = s[s > eps], s[s < -eps]
        X = np.array([(p*(-q) + nn*pp)/(pp - q) for p, pp in zip(pos, sp) for nn, q in zip(neg_, sn)])
        for side in (pos, neg_):
            Qm = np.vstack([side, on_, X]) if len(on_) else np.vstack([side, X]); h = ConvexHull(Qm); o.append(Qm[h.vertices])
    return o
regs = [np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1.]])]
for t, p in enumerate(P):
    pf = np.array([float(x) for x in p]); regs = split(regs, pf[:3] - pf[3], pf[3])
    if t % 10 == 0: print(f'PROGRESS {0.9 + 0.1*t/n:.3f} float split', flush=True)
vol = sum(ConvexHull(R).volume for R in regs)
C(abs(vol - 1/6) < 1e-9, 'float pieces fill the simplex section (volume sum)')
C(len(regs) == r, f'float splitting gives the exact count ({len(regs)} vs {r})')
nv = Counter(len(R) for R in regs); out['pieces_by_corner_count'] = {int(k): v for k, v in sorted(nv.items())}
say('pieces by corner count of the section piece', dict(nv))
out['seconds'] = time.time() - T0
json.dump(out, open(os.path.join(OUT, 'chambers.json'), 'w'), indent=1)
C.final()
