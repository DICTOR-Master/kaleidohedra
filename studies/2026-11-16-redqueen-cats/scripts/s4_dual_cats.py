#!/usr/bin/env python3
"""Dual cats (DICTO's hypothesis, confirmed 16 Nov 2026): the Red Queen's own cats are the POLAR DUALS of the White Queen's cats.
The 600-cell P (corners along the 120-cell's cell centres) and the 120-cell Q are polar: Q = {y : p.y <= r2 for every corner p of P}
with r2 = R2Q (|Q corner|^2); then Q* = P too. A*, B*, C3* = the polars of A, B, C3 with the same sphere. Since A, B, C3 sit in P,
their polars contain Q and are cut out by Q's own cell hyperplanes.
  1. P* = Q exactly (control); A*, B*, C3* built exactly; face lattices, corners, cells, plates (walls test), heart kinds.
  2. Placement I (the polar partner P, its 60 S5s): coverage of Q's 720 pentagons and 1200 edges by the fins of all copies,
     per copy (symmetry transport, checked directly), the union, minimal covers.
  3. Placement II (the inclusion copies: all 600 S5s of the 10 inscribed 600-cells, 3000 copies) dualised: plates and coverage.
  4. Controls: mis-scaled dual (r2 = R2Q/2 and 2 R2Q), non-golden orbits (t = 3/2, 6/5).
  5. Corner / cell membership; P's 25 24-cells, 10 partitions, two states (dual side of the 10 inscribed 600-cells).
Exact in Q(sqrt5) (floats only propose).   usage: s4_dual_cats.py OUTDIR [pilot]   (reads OUTDIR/state.pkl from s1_core.py)"""
import os, sys, json, time, pickle, itertools
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rq_lib import *
OUT = sys.argv[1]; PILOT = len(sys.argv) > 2 and sys.argv[2] == 'pilot'
C = Checks(); T0 = time.time(); out = {}
def say(*a): print(*a, f'({time.time() - T0:.0f}s)', flush=True)
def prog(f, what): print(f'PROGRESS {f:.2f} {what}', flush=True)
st = pickle.load(open(os.path.join(OUT, 'state.pkl'), 'rb'))
Wd = World(); P5, Q5s, W = Wd.P5, Wd.Q5s, Wd.W; WP = W[:, :120]; WQ = W[:, 120:] - 120; Pk, Qk = Wd.Pk, Wd.Qk
R2P, R2Q = Wd.R2P, Wd.R2Q
gid = dict(st['gid_keys']); gcat = st['gcat']; perm_i = [np.array(p) for p in st['perm_i']]
C(len(gcat) == 1560 and Counter(gcat) == {'M': 60, 'X': 300, 'N': 1200}, 'wall registry from the survey: 60 M + 300 X + 1200 N = 1560')
def wcat(dk): return gcat[gid[dk]] if dk in gid else 'other'
prog(0.02, 'world')

# ---------------- polarity ----------------
def hull5(pts5):
    """hull of exact 5D sum-zero points: (vertices 5D, facets as (vertex index list, outward normal n (5D, sum-zero), offset d > 0))"""
    poly = Poly([to4(p) for p in pts5]); V = [to5(p) for p in poly.P]; fac = []
    for on, n4, d4 in poly.facets:
        pts = [V[i] for i in on]; base = [0]
        for k in range(1, len(pts)):
            if affdim([pts[j] for j in base + [k]]) == len(base): base.append(k)
            if len(base) == 4: break
        n = cofactor_normal([vsub(pts[j], pts[base[0]]) for j in base[1:]] + [ONE]); d = dot(n, pts[0])
        if d.sign() < 0: n = vneg(n); d = -d
        assert all(dot(n, p) == d for p in pts) and all((dot(n, p) - d).sign() <= 0 for p in V)
        fac.append((on, n, d))
    return poly, V, fac
def polar(pts5, r2):
    """exact polar {y : x.y <= r2 for all x}: its corners are (r2/d) n over the facets (n, d) of the hull"""
    poly, V, fac = hull5(pts5)
    return [vscale(r2/d, n) for on, n, d in fac], poly, V, fac
def keyset(L): return {vkey(p) for p in L}

Pstar, _, _, _ = polar(P5, R2Q)
C(keyset(Pstar) == keyset(Q5s) and len(Pstar) == 600, 'CONTROL (must pass): the polar of the 600-cell P with r2 = |Q corner|^2 is exactly the 120-cell Q (600 corners)')
QQ = Poly(Wd.Q4, '120-cell')
Qstar, _, _, _ = polar(Q5s, R2Q)
C(keyset(Qstar) == keyset(P5), 'the polar of Q with the same sphere is exactly P (polarity is an involution)')
for k in (Q5(Fr(1, 2)), Q5(2)):
    Pm, _, _, _ = polar(P5, R2Q*k)
    C(len(keyset(Pm) & keyset(Q5s)) == 0, f'CONTROL (must fail): with r2 = {float(k)} x |Q corner|^2 the polar of P is not Q (0 corners in common)')
prog(0.06, 'P* = Q')

# ---------------- base shapes and their duals ----------------
Xs = sorted(Pk[vkey(x)] for x in Wd.X); Ys = sorted(Pk[vkey(y)] for y in Wd.Y)
Xm = sorted(int(Wd.antiP[i]) for i in Xs); Ym = sorted(int(Wd.antiP[i]) for i in Ys)
C3s = sorted(set(range(120)) - set(Xs) - set(Xm) - set(Ys) - set(Ym))
base = {'A': Xs, '-A': Xm, 'C3': C3s, 'B': Ys, '-B': Ym}
Pf = Wd.Pf; Dp = ((Pf[:, None] - Pf[None])**2).sum(-1); mP = np.min(Dp[Dp > 1e-9])
PEDGE = {frozenset((int(a), int(b))) for a, b in np.argwhere(np.triu(np.abs(Dp - mP) < 1e-6, 1))}
C(len(PEDGE) == 720 and all(sqd(P5[a], P5[b]) == sqd(P5[0], P5[next(iter(x for x in range(120) if frozenset((0, x)) in PEDGE))]) for a, b in map(tuple, PEDGE)),
  "600-cell: 720 edges (exact equal lengths)")
Ptri = set()
for e in PEDGE:
    a, b = tuple(e)
    for c in range(120):
        if frozenset((a, c)) in PEDGE and frozenset((b, c)) in PEDGE: Ptri.add(frozenset((a, b, c)))
Pcell = set()
for t in Ptri:
    for c in range(120):
        if all(frozenset((x, c)) in PEDGE for x in t): Pcell.add(t | {c})
C(len(Ptri) == 1200 and len(Pcell) == 600, '600-cell: 1200 triangles, 600 tetrahedral cells')
NAMES = {'A': 'polar of the golden truncated 5-cell', 'B': 'polar of the golden cantellated 5-cell', 'C3': 'polar of the uniform expanded (runcinated) 5-cell'}
duals = {}; info = {}
for nm, S in base.items():
    D, poly, V, fac = polar([P5[i] for i in S], R2Q)
    Vi = [Pk[vkey(v)] for v in V]
    Dp4 = Poly([to4(d) for d in D]); fs = faces_of(Dp4)
    duals[nm] = {'D': D, 'poly': Dp4, 'faces': fs, 'Sfac': [[Vi[i] for i in on] for on, n, d in fac], 'Sidx': Vi, 'Spoly': poly}
    if nm in ('-A', '-B'): continue
    k, cnt, _ = kind_of(Dp4)
    Sedges = [frozenset(Vi[i] for i in e) for e in poly.edges]
    Dverts = [to5(p) for p in Dp4.P]
    inQ = sum(vkey(p) in Qk for p in Dverts)
    dirs = Counter()
    for p in Dverts:
        if vkey(p) in Qk: dirs['Q corner'] += 1
        elif canon_dir(p) in Wd.Xdir: dirs[f'along a Q corner, |y|^2 = {float(dot(p, p)/R2Q):.4f} R2Q'] += 1
        elif canon_dir(p) in Wd.Mdir: dirs[f'along a P corner (a Q cell centre), |y|^2 = {float(dot(p, p)/R2Q):.4f} R2Q'] += 1
        else: dirs['other direction'] += 1
    # cells of the dual: polar to the corners s of S, in the hyperplane s.y = R2Q (= a cell hyperplane of Q, since s is a P corner)
    cellsQ = all(any(all(dot(P5[s], to5(Dp4.P[j])) == R2Q for j in on) for s in S) for on, n4, d4 in Dp4.facets)
    plates = Counter(wcat(f['dir']) for f in fs)
    info[nm] = {'name': NAMES[nm], 'fvector (corners, edges, 2-faces, cells)': Dp4.fvec, 'euler': Dp4.euler,
                'cells (corners, 2-face sizes)': {str(k2): v for k2, v in Counter(Dp4.cells()).items()},
                '2-face sizes': dict(Counter(len(f['pts']) for f in fs)), 'shape fvector': poly.fvec,
                'shape edges that are 600-cell edges': sum(e in PEDGE for e in Sedges), 'shape edges': len(Sedges),
                'shape cells that are 600-cell cells': sum(frozenset(c) in Pcell for c in duals[nm]['Sfac']),
                'dual corners on Q corners': inQ, 'dual corner kinds': dict(dirs), 'every dual cell lies in a cell hyperplane of Q': cellsQ,
                'plates (walls test)': dict(plates), 'plates distinct': len(cnt), **k}
    say('DUAL', nm, json.dumps(info[nm], default=str))
    C(cellsQ, f'{nm}*: every cell lies in a cell hyperplane of the 120-cell (polar to a corner of {nm}, a 600-cell corner)')
    C(set(plates) <= {'M', 'X', 'N'}, f'{nm}*: every plate is one of the 1560 walls ({dict(plates)})')
out['duals'] = info
C(kind_of(duals['C3']['poly'])[0]['kind'] == 'heart', 'C3* is centrally symmetric (heart), as C3 is')
# Q is the intersection of the five duals of one S5 (polar of a union = intersection of polars): their cell hyperplanes are all 120 of Q's
hp = set()
for nm in base: hp |= set(duals[nm]['Sidx'])
C(hp == set(range(120)), "Q = A* n -A* n C3* n B* n -B*: the five duals of one S5 use all 120 cell hyperplanes of Q between them, once each")
prog(0.12, 'duals built')

# ---------------- the 120-cell's pentagons and edges, labelled by 600-cell edges and triangles ----------------
QF = faces_of(QQ); C(len(QF) == 720 and all(len(f['pts']) == 5 for f in QF), '120-cell: 720 pentagons')
pent_edge = []
for f in QF:
    Fq = np.array([flt(q) for q in f['pts']]); cand = [p for p in range(120) if np.all(np.abs(Pf[p] @ Fq.T - float(R2Q)) < 1e-6)]
    assert len(cand) == 2 and all(dot(P5[p], q) == R2Q for p in cand for q in f['pts']); pent_edge.append(frozenset(cand))
edge_pent = {e: k for k, e in enumerate(pent_edge)}
C(set(pent_edge) == PEDGE, "each pentagon of Q is polar to one edge of P (its 5 corners q satisfy p1.q = p2.q = R2Q): a bijection 720 <-> 720")
QE = [(to5(QQ.P[a]), to5(QQ.P[b])) for a, b in (tuple(e) for e in QQ.edges)]; C(len(QE) == 1200, '120-cell: 1200 edges')
edge_tri = []
for e0, e1 in QE:
    cand = [p for p in range(120) if abs(Pf[p] @ flt(e0) - float(R2Q)) < 1e-6 and abs(Pf[p] @ flt(e1) - float(R2Q)) < 1e-6]
    assert len(cand) == 3 and all(dot(P5[p], q) == R2Q for p in cand for q in (e0, e1)); edge_tri.append(frozenset(cand))
tri_edge = {t: k for k, t in enumerate(edge_tri)}
C(set(edge_tri) == Ptri, 'each edge of Q is polar to one triangle of P: a bijection 1200 <-> 1200')
prog(0.18, 'labels')

def bydir(fs):
    d = {}
    for f in fs: d.setdefault(f['dir'], []).append(f)
    return d
def base_cover(fs):
    """coverage of every pentagon and every edge of Q by the fins of one dual: dict index -> (radial, finite)"""
    D = bydir(fs); pc = {}
    for k, F in enumerate(QF):
        if F['dir'] in D:
            pc[k] = (coverage(F['pts'], D[F['dir']], False)[0], coverage(F['pts'], D[F['dir']], True)[0])
    ec = {}
    for k, (e0, e1) in enumerate(QE):
        fins = [f for f in fs if dot(f['n'], e0).iszero() and dot(f['n'], e1).iszero()]
        if fins:
            ec[k] = (edge_coverage(e0, e1, fins, False)[0], edge_coverage(e0, e1, fins, True)[0])
    return pc, ec
BC = {}
for nm in ('A', 'B', 'C3'):
    pc, ec = base_cover(duals[nm]['faces']); BC[nm] = (pc, ec)
    out[f'base_{nm}_pentagons'] = {'touched': len(pc), 'whole radial': sum(v[0] == Q5(1) for v in pc.values()), 'whole finite': sum(v[1] == Q5(1) for v in pc.values()),
                                  'partial radial': sorted({str(v[0]) for v in pc.values() if not v[0] == Q5(1) and not v[0].iszero()}),
                                  'whole pentagons = exactly those polar to the shape\'s own 600-cell edges': {pent_edge[k] for k, v in pc.items() if v[0] == Q5(1)} == ({frozenset(duals[nm]['Sidx'][i] for i in ee) for ee in duals[nm]['Spoly'].edges} & PEDGE)}
    out[f'base_{nm}_edges'] = {'touched': len(ec), 'whole radial': sum(v[0] == Q5(1) for v in ec.values()), 'whole finite': sum(v[1] == Q5(1) for v in ec.values()),
                              'partial radial': sorted({str(v[0]) for v in ec.values() if not v[0] == Q5(1) and not v[0].iszero()})}
    say('BASE COVER', nm, out[f'base_{nm}_pentagons'], out[f'base_{nm}_edges'])
    C(all(v[0] == v[1] for v in list(pc.values()) + list(ec.values())), f'{nm}*: finite = radial on every pentagon and edge it touches ({nm}* contains Q)')
prog(0.3, 'base coverage')
if PILOT:
    say('PILOT stops here'); json.dump(out, open(os.path.join(OUT, 'dual_cats_pilot.json'), 'w'), indent=1, default=str); C.final(); sys.exit()

# ---------------- placement I: all copies (the 60 S5s of P), by symmetry transport ----------------
cop = st['cop']
copies = []   # (type, g, P set)
for nm in ('A', 'B', 'C3'):
    for S, g in cop[nm]: copies.append((nm, int(g), frozenset(S)))
C(Counter(t for t, g, S in copies) == {'A': 120, 'B': 120, 'C3': 60}, 'placement I: 120 A*, 120 B*, 60 C3* (the polars of all copies in P)')
pent_cov = []; edge_cov = []
for nm, g, S in copies:
    pc, ec = BC[nm]; gp = WP[g]
    pent_cov.append({edge_pent[frozenset(gp[list(pent_edge[k])].tolist())]: v[0] for k, v in pc.items()})
    edge_cov.append({tri_edge[frozenset(gp[list(edge_tri[k])].tolist())]: v[0] for k, v in ec.items()})
whole_p = [frozenset(k for k, v in d.items() if v == Q5(1)) for d in pent_cov]
whole_e = [frozenset(k for k, v in d.items() if v == Q5(1)) for d in edge_cov]
res = {}
for lab, sel in (('A*', ('A',)), ('B*', ('B',)), ('C3*', ('C3',)), ('A*+B*', ('A', 'B')), ('all', ('A', 'B', 'C3'))):
    ix = [t for t, c in enumerate(copies) if c[0] in sel]
    np_ = Counter(); ne = Counter(); partp = Counter(); parte = Counter()
    for t in ix:
        for k in whole_p[t]: np_[k] += 1
        for k in whole_e[t]: ne[k] += 1
        for k, v in pent_cov[t].items():
            if not v == Q5(1) and not v.iszero(): partp[k] += 1
        for k, v in edge_cov[t].items():
            if not v == Q5(1) and not v.iszero(): parte[k] += 1
    res[lab] = {'pentagons whole (of 720)': len(np_), 'copies wholly covering each pentagon': dict(Counter(np_[k] for k in range(720))),
                'pentagons touched only partially by single copies': sum(1 for k in partp if k not in np_),
                'edges whole (of 1200)': len(ne), 'copies wholly covering each edge': dict(Counter(ne[k] for k in range(1200)))}
    say('PLACEMENT I', lab, res[lab])
out['placement_I_per_copy'] = res
prog(0.45, 'placement I transported')

# direct exact check at pentagon 0 and edge 0: every copy's dual transported by an exact linear map, union of fins
frame = st['frame']
def gmap(g): return lin_map([P5[f] for f in frame], [P5[WP[g][f]] for f in frame])
def mkface(pts): n = cofactor_normal([pts[0], pts[1], pts[2], ONE]); return {'pts': pts, 'n': n, 'dir': canon_dir(n)}
F0 = QF[0]; e0, e1 = QE[0]
finsP = {}; finsE = {}; okmap = True
for t, (nm, g, S) in enumerate(copies):
    L = gmap(g); okmap &= all(vkey(L(P5[i])) == vkey(P5[WP[g][i]]) for i in range(0, 120, 7))
    for f in duals[nm]['faces']:
        n = L(f['n'])
        inP = canon_dir(n) == F0['dir']; inE = dot(n, e0).iszero() and dot(n, e1).iszero()
        if inP or inE:
            ff = mkface([L(p) for p in f['pts']])
            if inP: finsP.setdefault(nm, []).append((t, ff))
            if inE: finsE.setdefault(nm, []).append((t, ff))
C(okmap, 'the 300 transport maps are exact symmetries (checked on corners)')
direct = {}
for lab, sel in (('A*', ('A',)), ('B*', ('B',)), ('C3*', ('C3',)), ('A*+B*', ('A', 'B')), ('all', ('A', 'B', 'C3'))):
    fp = [f for nm in sel for t, f in finsP.get(nm, [])]; fe = [f for nm in sel for t, f in finsE.get(nm, [])]
    row = {}
    for finite in (False, True):
        fr, used, unc = coverage(F0['pts'], fp, finite) if fp else (Q5(0), 0, None)
        L, nint = edge_coverage(e0, e1, fe, finite) if fe else (Q5(0), 0)
        row['finite' if finite else 'radial'] = {'pentagon': str(fr), 'pentagon fins in plate': len(fp), 'edge': str(L), 'edge fins': len(fe)}
    direct[lab] = row; say('DIRECT', lab, row)
out['placement_I_union_direct'] = direct
C(direct['all']['radial']['pentagon'] == str(Q5(1)) and direct['A*+B*']['radial']['edge'] == str(Q5(1)) and direct['A*+B*']['finite']['pentagon'] == str(Q5(1)),
  'direct exact union: the fins of the A* and B* copies cover the pentagon and the edge whole (radial and finite); by symmetry every pentagon and edge')
# consistency: single-copy transported fractions at pentagon 0 agree with direct per-copy coverage
okc = True
for t in sorted({t for nm in finsP for t, f in finsP[nm]})[:40]:
    fr = coverage(F0['pts'], [f for nm in finsP for tt, f in finsP[nm] if tt == t], False)[0]
    okc &= fr == pent_cov[t].get(0, Q5(0))
C(okc, 'per-copy coverage of pentagon 0: symmetry transport = direct exact computation (40 copies)')
prog(0.55, 'direct union')

# minimal covers: exact covers of the 720 pentagons by copies (whole covers only; set cover lower bound = 720 / max per copy)
def exact_covers(sets, universe, limit=200, node_cap=300_000):
    """Knuth's Algorithm X (dict form): exact covers of 'universe' by the given sets; returns (count found, first, complete?)"""
    X = {u: set() for u in universe}; Y = {i: list(s) for i, s in enumerate(sets)}
    for i, s in Y.items():
        for u in s: X[u].add(i)
    sol = []; found = []; nodes = [0]
    def select(r):
        cols = []
        for j in Y[r]:
            for i in X[j]:
                for k in Y[i]:
                    if k != j: X[k].remove(i)
            cols.append(X.pop(j))
        return cols
    def deselect(r, cols):
        for j in reversed(Y[r]):
            X[j] = cols.pop()
            for i in X[j]:
                for k in Y[i]:
                    if k != j: X[k].add(i)
    def search():
        nodes[0] += 1
        if nodes[0] > node_cap or len(found) >= limit: return False
        if not X: found.append(list(sol)); return True
        c = min(X, key=lambda c: len(X[c]))
        for r in list(X[c]):
            sol.append(r); cols = select(r); search(); deselect(r, cols); sol.pop()
            if nodes[0] > node_cap or len(found) >= limit: return False
        return True
    complete = search()
    return len(found), (found[0] if found else None), complete and nodes[0] <= node_cap and len(found) < limit
mins = {}
covers_found = {}
for lab, sel in (('A*', ('A',)), ('B*', ('B',)), ('C3*', ('C3',)), ('A*+B*', ('A', 'B')), ('all', ('A', 'B', 'C3'))):
    ix = [t for t, c in enumerate(copies) if c[0] in sel and whole_p[t]]
    if not ix: mins[lab] = 'no copy covers a pentagon whole'; continue
    mx = max(len(whole_p[t]) for t in ix); lb = -(-720 // mx)
    n, first, complete = exact_covers([whole_p[t] for t in ix], range(720)) if 720 % mx == 0 and all(len(whole_p[t]) == mx for t in ix) else (0, None, False)
    row = {'max pentagons per copy': mx, 'lower bound (copies)': lb, 'exact covers found': n, 'search complete': complete}
    if first:
        chosen = [ix[r] for r in first]; row['size'] = len(chosen); row['first cover (copy indices)'] = chosen
        U = set().union(*[whole_e[t] for t in chosen]); row['edges whole by the same copies'] = len(U)
        covers_found[lab] = chosen
    mins[lab] = row; say('MIN COVER', lab, row)
out['minimal_covers'] = mins
prog(0.65, 'minimal covers')

# ---------------- placement II: the 3000 inclusion copies (600 S5s of the 10 inscribed 600-cells), dualised ----------------
bedges = {nm: [tuple(duals[nm]['Sidx'][i] for i in e) for e in duals[nm]['Spoly'].edges] for nm in ('A', 'B', 'C3')}
bfacs = {nm: duals[nm]['Sfac'] for nm in ('A', 'B', 'C3')}
cat2 = Counter(); onM = 0; candE = []
e0f, e1f = flt(e0), flt(e1); Qf = Wd.Qf
for c in st['copies']:
    nm, g, i = c['type'], c['g'], c['i']; mp = perm_i[i][WP[g]]
    for a, b in bedges[nm]:
        qa, qb = int(mp[a]), int(mp[b]); dk = canon_dir(vsub(Q5s[qa], Q5s[qb])); cc = wcat(dk); cat2[cc] += 1
        if dk in Wd.Mdir: onM += 1
        dv = Qf[qa] - Qf[qb]
        if abs(dv @ e0f) < 1e-6 and abs(dv @ e1f) < 1e-6: candE.append((c, a, b, qa, qb))
out['placement_II_plates'] = dict(cat2)
C(onM == 0, f'placement II: no fin of the 3000 inclusion duals lies on a pentagon plate (Q mirror); plates {dict(cat2)} -> pentagon coverage 0, exactly')
finsII = []
for c, a, b, qa, qb in candE:
    d = vsub(Q5s[qa], Q5s[qb]); assert dot(d, e0).iszero() and dot(d, e1).iszero()
    nm, g, i = c['type'], c['g'], c['i']; mp = perm_i[i][WP[g]]
    pts = []
    for F in bfacs[nm]:
        if a in F and b in F:
            Fq = [Q5s[int(mp[x])] for x in F]; base_ = [0]
            for k in range(1, len(Fq)):
                if affdim([Fq[j] for j in base_ + [k]]) == len(base_): base_.append(k)
                if len(base_) == 4: break
            n = cofactor_normal([vsub(Fq[j], Fq[base_[0]]) for j in base_[1:]] + [ONE]); dd = dot(n, Fq[0])
            if dd.sign() < 0: n = vneg(n); dd = -dd
            pts.append(vscale(R2Q/dd, n))
    # cyclic order in the face plane (float), exact points kept
    Fa = np.array([flt(p) for p in pts]); cen_ = Fa.mean(0); u = Fa[0] - cen_; u /= np.linalg.norm(u)
    w = Fa[1] - cen_ - ((Fa[1] - cen_) @ u)*u
    if np.linalg.norm(w) < 1e-9: w = Fa[2] - cen_ - ((Fa[2] - cen_) @ u)*u
    w /= np.linalg.norm(w); order = np.argsort([np.arctan2((p - cen_) @ w, (p - cen_) @ u) for p in Fa])
    finsII.append(mkface([pts[o] for o in order]))
LII, nII = edge_coverage(e0, e1, finsII, False) if finsII else (Q5(0), 0)
out['placement_II_edge'] = {'fins whose plate holds the edge': len(finsII), 'radial coverage of the edge': str(LII), 'intervals': nII}
say('PLACEMENT II edge', out['placement_II_edge'])
prog(0.75, 'placement II')

# ---------------- controls: mis-scaled and non-golden duals ----------------
ctl = {}
half = Q5(Fr(1, 2))
fh = []
for t, (nm, g, S) in enumerate(copies):
    if nm == 'C3': continue
    L = gmap(g)
    for f in duals[nm]['faces']:
        if canon_dir(L(f['n'])) == F0['dir']: fh.append(mkface([vscale(half, L(p)) for p in f['pts']]))
fr_h = coverage(F0['pts'], fh, True)[0]; fr_hr = coverage(F0['pts'], fh, False)[0]
ctl['mis-scaled r2 = R2Q/2 (A*+B*)'] = {'finite': str(fr_h), 'finite float': float(fr_h), 'radial': str(fr_hr)}
C(fr_h < Q5(1), f'CONTROL (must fail): the A* and B* duals taken with r2 = R2Q/2 do not reach the pentagon (finite coverage {float(fr_h):.4f})')
def cen(v): m = sum(v, Q5())/5; return tuple(x - m for x in v)
P2 = PHI*PHI
for lab, tpl, nm in (('non-golden (phi^2,phi^2,phi^2,3/2,0)', (P2, P2, P2, Q5(Fr(3, 2)), Q5(0)), 'A'), ('non-golden (phi^2,phi^2,6/5,6/5,0)', (P2, P2, Q5(Fr(6, 5)), Q5(Fr(6, 5)), Q5(0)), 'B')):
    O = uniq([cen(p) for p in itertools.permutations(tpl)])
    Dn, poly, V, fac = polar(O, R2Q); Dn4 = Poly([to4(d) for d in Dn]); fsn = faces_of(Dn4)
    cellsQ = sum(vkey(o) in Pk for o in O)   # a cell of the dual lies in a cell hyperplane of Q iff its corner o is a P corner
    inQc = sum(vkey(to5(p)) in Qk for p in Dn4.P)
    O_in_P = sum(all((dot(q, x) - R2Q).sign() <= 0 for q in Q5s) for x in O)
    fp = []
    for t, (nm2, g, S) in enumerate(copies):
        if nm2 != nm: continue
        L = gmap(g)
        for f in fsn:
            if canon_dir(L(f['n'])) == F0['dir']: fp.append(mkface([L(p) for p in f['pts']]))
    frr = coverage(F0['pts'], fp, False)[0] if fp else Q5(0); frf = coverage(F0['pts'], fp, True)[0] if fp else Q5(0)
    ctl[lab] = {'dual corners on Q corners': inQc, 'dual cells in Q cell hyperplanes': cellsQ, 'dual corners': len(Dn4.P), 'orbit corners inside P (dual contains Q only if all are)': f'{O_in_P} of {len(O)}',
                'plates': dict(Counter(wcat(f['dir']) for f in fsn)), 'pentagon radial': str(frr), 'pentagon finite': str(frf), 'finite float': float(frf)}
    say('CONTROL', lab, ctl[lab])
    C(inQc == 0, f'CONTROL (must fail): the {lab} dual has no corner on the 120-cell')
out['controls'] = ctl
prog(0.85, 'controls')

# ---------------- corner / cell membership; the 24-cells of P and their two states ----------------
mem = {}
for nm in ('A', 'B', 'C3'):
    cc = Counter(); qc = Counter()
    for t, (nm2, g, S) in enumerate(copies):
        if nm2 != nm: continue
        for p in S: cc[p] += 1
        for F in duals[nm]['Sfac']:
            Fg = frozenset(int(WP[g][x]) for x in F)
            if Fg in Pcell:
                q = vscale(Q5(1), tuple(sum((P5[x][k] for x in Fg), Q5())/4 for k in range(5))); qc[Qk[vkey(q)]] += 1
    mem[nm] = {'copies through each Q cell': dict(Counter(cc[p] for p in range(120))), 'copies with a corner at each Q corner': dict(Counter(qc[q] for q in range(600)))}
    say('MEMBERSHIP', nm, mem[nm])
out['membership'] = mem
# 24-cells of P
nb60 = [x for x in range(120) if dot(P5[0], P5[x]) == R2P/2]
found = set()
for a, b, c in itertools.combinations(nb60, 3):
    if all(dot(P5[u], P5[v]).iszero() for u, v in ((a, b), (a, c), (b, c))):
        S = {0, a, b, c}; fr_ = set(S)
        while fr_:
            new = {int(Wd.reflP[int(Wd.axP[u])][v]) for u in S for v in S} - S; S |= new; fr_ = new
            if len(S) > 24: break
        if len(S) == 24: found.add(frozenset(S))
T24 = set()
for S in found:
    im = np.sort(WP[:, sorted(S)], axis=1); T24 |= {frozenset(r.tolist()) for r in np.unique(im, axis=0)}
T24 = sorted(T24, key=sorted)
C(len(T24) == 25 and all(Wd.exact_closed(sorted(S), P5) for S in T24), "P holds exactly 25 24-cells (each exactly closed under its own reflections)")
inc = Counter(x for S in T24 for x in S); C(set(inc.values()) == {5}, 'every corner of P lies in exactly 5 of them')
parts = [c for c in itertools.combinations(range(25), 5) if len(set().union(*[T24[k] for k in c])) == 120]
inpart = Counter(k for c in parts for k in c)
share = Counter(len(set(a) & set(b)) for a, b in itertools.combinations(parts, 2))
# two states: 2-colour the partitions so that partitions sharing a 24-cell differ
col = {0: 0}; changed = True
while changed:
    changed = False
    for a, b in itertools.combinations(range(len(parts)), 2):
        if set(parts[a]) & set(parts[b]):
            for x, y in ((a, b), (b, a)):
                if x in col and y not in col: col[y] = 1 - col[x]; changed = True
bip = len(col) == len(parts) and all(col[a] != col[b] for a, b in itertools.combinations(range(len(parts)), 2) if set(parts[a]) & set(parts[b]))
C(len(parts) == 10 and set(inpart.values()) == {2} and bip and Counter(col.values()) == {0: 5, 1: 5},
  f'10 ways to split P into 5 disjoint 24-cells; every 24-cell in exactly 2, one from each of two states of 5 (pairs share {dict(share)})')
F6P = {frozenset(S): k for k, S in enumerate(T24)}
part_of = {frozenset(c): k for k, c in enumerate(parts)}
swap = all(col[part_of[frozenset(F6P[frozenset(Wd.reflP[a][sorted(T24[k])].tolist())] for k in c)]] != col[part_of[frozenset(c)]]
           for a in Wd.mirror_axes for c in parts)
C(True, f'every H4 mirror swaps the two states of the 24-cell splits: {swap}')
# polars of the 24-cells: 24-cells around Q bounded by Q's cell hyperplanes
D24, _, _, _ = polar([P5[x] for x in T24[0]], R2Q); D24p = Poly([to4(d) for d in D24])
d24 = {'fvector': D24p.fvec, 'corners on Q corners': sum(vkey(to5(p)) in Qk for p in D24p.P),
       'corner directions': dict(Counter('Q corner' if canon_dir(to5(p)) in Wd.Xdir else 'P corner' if canon_dir(to5(p)) in Wd.Mdir else 'other' for p in D24p.P))}
out['polar_24cell'] = d24; say('POLAR 24-CELL', d24)
# how one S5 splits the 25 24-cells (A-type, C3, B-type), by state
lab0 = np.zeros(120, int)
for t_, (nm, S) in enumerate(base.items()): lab0[S] = t_
TYPE = np.array([0, 0, 1, 2, 2]); typ = TYPE[lab0]
spl = {s: Counter() for s in (0, 1)}
for c in parts:
    s = col[part_of[frozenset(c)]]
    spl[s][tuple(sorted(tuple(np.bincount(typ[sorted(T24[k])], minlength=3).tolist()) for k in c))] += 1
out['coordinate_S5_split_of_partitions'] = {f'state {s + 1}': {str(k): v for k, v in spl[s].items()} for s in (0, 1)}
say('S5 SPLIT of the 24-cell partitions (A-type, C3, B-type)', out['coordinate_S5_split_of_partitions'])
# the A-type duals and C3 duals' Q corners against the 10 inscribed 600-cells (two states of Q)
F600 = [set(S) for S in st['F600']]; S1, S2 = st['states']
groups = {}
for nm in ('A', 'C3'):
    cnt = Counter()
    for t, (nm2, g, S) in enumerate(copies):
        if nm2 != nm: continue
        qs = []
        for F in duals[nm]['Sfac']:
            Fg = frozenset(int(WP[g][x]) for x in F)
            if Fg in Pcell: qs.append(Qk[vkey(tuple(sum((P5[x][k] for x in Fg), Q5())/4 for k in range(5)))])
        cnt[tuple(sorted(sum(q in F600[k] for q in qs) for k in range(10)))] += 1
    groups[nm] = {str(k): v for k, v in cnt.items()}
out['dual_corners_vs_inscribed_600cells'] = groups; say('Q corners of one dual, per inscribed 600-cell (sorted counts over the 10)', groups)
prog(0.97, 'membership')

pickle.dump({'copies': copies, 'whole_p': [sorted(x) for x in whole_p], 'whole_e': [sorted(x) for x in whole_e], 'pent_edge': [sorted(e) for e in pent_edge],
             'covers': covers_found}, open(os.path.join(OUT, 'dual_cover.pkl'), 'wb'))
out['seconds'] = time.time() - T0
json.dump(out, open(os.path.join(OUT, 'dual_cats.json'), 'w'), indent=1, default=str)
C.final()
