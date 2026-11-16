#!/usr/bin/env python3
"""DICTO (16 Nov 2026): "so cats have one side of a pentagon each?!" For every side (edge) of every one of the 120-cell's 720
pentagons, which KINDS of dual cat (X* = A*, -X*, R* = C3*, F* = B*, -F*) have that side as a TRUE EDGE of one of their copies
(placement I: the polars of the 300 copies of P's 60 S5s)? Also: which have an edge CONTAINING the side (same line, longer).
Exact in Q(sqrt5): float line keys only propose; every hit is re-checked exactly (collinear, endpoints, inclusion).
Kinds: X/-X and F/-F are named within each S5 by carrying the coordinate S5's labels (Silent Running) over by one symmetry h
(h maps the coordinate C3 onto that S5's C3); the A-type / B-type / C3 split is independent of that choice.
usage: s6_pentagon_sides.py OUTDIR"""
import os, sys, json, time, pickle, itertools
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rq_lib import *
OUT = sys.argv[1]; C = Checks(); T0 = time.time(); out = {}
def say(*a): print(*a, f'({time.time() - T0:.0f}s)', flush=True)
st = pickle.load(open(os.path.join(OUT, 'state.pkl'), 'rb'))
Wd = World(); P5, Q5s = Wd.P5, Wd.Q5s; WP = Wd.W[:, :120]; Pk, Qk = Wd.Pk, Wd.Qk; R2Q = Wd.R2Q
KIND = ['X*', '-X*', 'R*', 'F*', '-F*']; TYPE = {0: 'A-type', 1: 'A-type', 2: 'C3', 3: 'B-type', 4: 'B-type'}
Xs = sorted(Pk[vkey(p)] for p in Wd.X); Ys = sorted(Pk[vkey(p)] for p in Wd.Y)
Xm = sorted(int(Wd.antiP[i]) for i in Xs); Ym = sorted(int(Wd.antiP[i]) for i in Ys)
C3s = sorted(set(range(120)) - set(Xs) - set(Xm) - set(Ys) - set(Ym)); BASE = [Xs, Xm, C3s, Ys, Ym]
def hull_facets(pts5):
    poly = Poly([to4(p) for p in pts5]); V = [to5(p) for p in poly.P]; fac = []
    for on, n4, d4 in poly.facets:
        pts = [V[i] for i in on]; b = [0]
        for k in range(1, len(pts)):
            if affdim([pts[j] for j in b + [k]]) == len(b): b.append(k)
            if len(b) == 4: break
        n = cofactor_normal([vsub(pts[j], pts[b[0]]) for j in b[1:]] + [ONE]); d = dot(n, pts[0])
        if d.sign() < 0: n = vneg(n); d = -d
        fac.append((n, d))
    return fac
# base duals: corners and edges (exact), as 5D points
bd = {}
for k, S in enumerate(BASE):
    D = [vscale(R2Q/d, n) for n, d in hull_facets([P5[i] for i in S])]
    Dp = Poly([to4(p) for p in D]); V = [to5(p) for p in Dp.P]
    bd[k] = (V, [tuple(e) for e in Dp.edges])
C([len(bd[k][1]) for k in range(5)] == [30, 30, 70, 80, 80], f'edges of the five duals X*, -X*, R*, F*, -F*: {[len(bd[k][1]) for k in range(5)]}')
# copies (placement I) and their kinds
cop = st['cop']; frame = st['frame']
copies = []
for nm in ('A', 'B', 'C3'):
    for S, g in cop[nm]: copies.append((nm, int(g), frozenset(S)))
c3_of = {}
for t, (nm, g, S) in enumerate(copies):
    if nm == 'C3': c3_of[S] = g
kind = {}
for t, (nm, g, S) in enumerate(copies):
    if nm == 'C3': kind[t] = 2; continue
    # its S5 = the S5 whose C3 is disjoint from S and from -S with the remaining 40 corners being the other A/B pair: find via h
    for S3, h in c3_of.items():
        hh = np.arange(120) if sorted(S3) == C3s else WP[h]
        img = [frozenset(hh[B].tolist()) for B in BASE]
        if S in img: kind.setdefault(t, set()).add(img.index(S))
amb = sum(1 for t in kind if isinstance(kind[t], set) and len(kind[t]) > 1)
C(all(isinstance(kind[t], int) or len(kind[t]) == 1 for t in kind), f'every A- and B-type copy belongs to exactly one S5 and gets one kind ({amb} ambiguous)')
kind = {t: (v if isinstance(v, int) else next(iter(v))) for t, v in kind.items()}
C(Counter(kind.values()) == {0: 60, 1: 60, 2: 60, 3: 60, 4: 60}, f'60 copies of each kind: {dict(Counter(kind.values()))}')
say('kinds assigned')
# transport every copy's dual edges exactly, index by float line key
def gmap(g): return lin_map([P5[f] for f in frame], [P5[WP[g][f]] for f in frame])
def lkey(a, b):
    a, b = flt(a), flt(b); dv = b - a; dv /= np.linalg.norm(dv); i = np.argmax(np.abs(dv) > 1e-9)
    if dv[i] < 0: dv = -dv
    foot = a - (a @ dv)*dv; return tuple(np.round(np.r_[dv, foot], 5) + 0.0)
lines = {}
for t, (nm, g, S) in enumerate(copies):
    L = gmap(g); k = kind[t]; base = 0 if nm == 'A' else 3 if nm == 'B' else 2
    V, Ed = bd[base]; Vt = [L(p) for p in V]
    for a, b in Ed: lines.setdefault(lkey(Vt[a], Vt[b]), []).append((t, Vt[a], Vt[b]))
    if t % 50 == 0: print(f'PROGRESS {0.1 + 0.6*t/len(copies):.2f} transport', flush=True)
say('copy edges transported', sum(len(v) for v in lines.values()))
# the 120-cell's pentagons and their sides
QQ = Poly(Wd.Q4); QF = faces_of(QQ); C(len(QF) == 720, '720 pentagons')
def on_segment(p, a, b):
    """exact: p lies on the closed segment ab"""
    ab = vsub(b, a); ap = vsub(p, a); i = next(j for j in range(5) if not ab[j].iszero()); lam = ap[i]/ab[i]
    return vkey(vscale(lam, ab)) == vkey(ap) and lam.sign() >= 0 and (lam - Q5(1)).sign() <= 0
side_true = {}; side_cont = {}
for kp, F in enumerate(QF):
    pts = F['pts']
    for s in range(5):
        a, b = pts[s], pts[(s + 1) % 5]; key = frozenset((vkey(a), vkey(b)))
        if key in side_true: continue
        tr, co = set(), set()
        for t, u, v in lines.get(lkey(a, b), []):
            if on_segment(a, u, v) and on_segment(b, u, v):
                co.add(t)
                if {vkey(u), vkey(v)} == {vkey(a), vkey(b)}: tr.add(t)
        side_true[key] = tr; side_cont[key] = co
    if kp % 72 == 0: print(f'PROGRESS {0.7 + 0.25*kp/720:.2f} sides', flush=True)
C(len(side_true) == 1200, 'the 720 pentagons have 1200 distinct sides (the edges of the 120-cell)')
def table(D):
    kc = Counter(); tc = Counter(); pat = Counter()
    for key, ts in D.items():
        ks = sorted({kind[t] for t in ts}); pat[' '.join(KIND[k] for k in ks) or 'none'] += 1
        for k in ks: kc[KIND[k]] += 1
        tc[tuple(sorted(Counter(TYPE[kind[t]] for t in ts).items()))] += 1
    return {'sides with each kind (of 1200)': dict(kc), 'kind sets per side': dict(pat), 'copies per side by type': {str(k): v for k, v in tc.items()}}
out['true_edges'] = table(side_true); out['containing_edges'] = table(side_cont)
say('TRUE EDGES', out['true_edges']); say('CONTAINING EDGES', out['containing_edges'])
# matchings: for each pentagon, number of ways to give its 5 sides to the 5 kinds, one each
def matchings(D):
    cnt = Counter()
    for F in QF:
        pts = F['pts']; sk = [{kind[t] for t in D[frozenset((vkey(pts[s]), vkey(pts[(s + 1) % 5])))]} for s in range(5)]
        cnt[sum(all(p[s] in sk[s] for s in range(5)) for p in itertools.permutations(range(5)))] += 1
    return dict(cnt)
out['matchings_true'] = matchings(side_true); out['matchings_containing'] = matchings(side_cont)
say('MATCHINGS per pentagon (true edges)', out['matchings_true'], '(containing edges)', out['matchings_containing'])
mt, mc = out['matchings_true'], out['matchings_containing']
forced = all(len(v) == 1 for v in side_true.values()) and mt == {1: 720}
verdict = 'i' if forced else ('ii' if 0 not in mt else 'iii')
out['verdict_true_edges'] = verdict
out['verdict_containing_edges'] = 'i' if (all(len({kind[t] for t in v}) == 1 for v in side_cont.values()) and mc == {1: 720}) else ('ii' if 0 not in mc else 'iii')
print('VERDICT true edges:', verdict, '| containing edges:', out['verdict_containing_edges'], flush=True)
# controls: the 120-cell's own edges are edges of Q (positive), a dual copy's own edges are found as true edges of that copy (positive)
t0 = 0; V, Ed = bd[0]; L = gmap(copies[t0][1]); a, b = L(V[Ed[0][0]]), L(V[Ed[0][1]])
hit = [t for t, u, v in lines.get(lkey(a, b), []) if {vkey(u), vkey(v)} == {vkey(a), vkey(b)}]
C(t0 in hit, 'positive control: an edge of a dual copy is found as a true edge of that copy by the same search')
C(sum(len(v) for v in side_cont.values()) >= sum(len(v) for v in side_true.values()), 'containing edges include the true edges')
out['seconds'] = time.time() - T0
json.dump(out, open(os.path.join(OUT, 'pentagon_sides.json'), 'w'), indent=1, default=str)
C.final()
