#!/usr/bin/env python3
"""120-cell survey, part 2 (DICTO 16 Nov 2026). (a) Do the Vacuus fins of the golden shapes form the Queens' skeletons?
A fin = the cone from the centre over one 2-face. 'finite' = that cone cut off at the face (the literal fin); 'radial' = the same
cone carried on outward (the plate's reach). Coverage of the 600-cell's 1200 triangles / 720 edges and of the 120-cell's 720
pentagons / 1200 edges, exact in Q(sqrt5). (b) heart / inherited heart (DICTO's name) / non-heart for every Vacuus met, and the
tentative conjecture 'inherited heart exactly when the walls are inherited from a heart parent but the central symmetry is lost'.
usage: s2_skeleton_kinds.py OUTDIR   (reads OUTDIR/state.pkl from s1_core.py)"""
import os, sys, json, time, pickle, random
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rq_lib import *
OUT = sys.argv[1]; C = Checks(); T0 = time.time(); out = {}
def say(*a): print(*a, f'({time.time() - T0:.0f}s)', flush=True)
st = pickle.load(open(os.path.join(OUT, 'state.pkl'), 'rb'))
Wd = World(); P5, Q5s, W = Wd.P5, Wd.Q5s, Wd.W; WP = W[:, :120]; WQ = W[:, 120:] - 120; Pk = Wd.Pk
perm_i = [np.array(p) for p in st['perm_i']]; gcat = st['gcat']; gM, gX = st['gM'], st['gX']
gid = dict(st['gid_keys']); gdir = {v: k for k, v in gid.items()}
def dvec(k): return tuple(Q5(a, b) for a, b in k)
PPf = faces_of(Wd.PP); C(len(PPf) == 1200, '600-cell: 1200 triangles')
def tri_ok(fs): return all(len(f['pts']) == 3 for f in fs)
say('setup')

# ---------------- (a1) the 600-cell and the five pieces of the coordinate S5 ----------------
Xs = frozenset(Pk[vkey(x)] for x in Wd.X); Ys = frozenset(Pk[vkey(y)] for y in Wd.Y)
Xm = frozenset(int(Wd.antiP[i]) for i in Xs); Ym = frozenset(int(Wd.antiP[i]) for i in Ys)
C3s = frozenset(range(120)) - Xs - Xm - Ys - Ym
pieces = {'A': Xs, '-A': Xm, 'C3': C3s, 'B': Ys, '-B': Ym}
pf = {k: faces_of(Poly([Wd.P4[i] for i in sorted(S)])) for k, S in pieces.items()}
def bydir(fs):
    d = {}
    for f in fs: d.setdefault(f['dir'], []).append(f)
    return d
def tri_cov(Fs, fins_by_dir, finite):
    res = []
    for F in Fs:
        fr, used, unc = coverage(F['pts'], fins_by_dir.get(F['dir'], []), finite); res.append(fr)
    return res
def summarize(fr):
    c = Counter(str(x) for x in fr); tot = sum(fr, Q5())/len(fr)
    return {'mean_fraction': str(tot), 'mean_float': float(tot), 'full': sum(1 for x in fr if x == Q5(1)), 'zero': sum(1 for x in fr if x.iszero()),
            'distribution': dict(c)}
five = [f for k in pf for f in pf[k]]; fiveD = bydir(five)
res = {}
for finite in (True, False):
    nm = 'finite' if finite else 'radial'
    fr = tri_cov(PPf, fiveD, finite); res[f'600_triangles_{nm}'] = summarize(fr)
    say('600-cell triangles by the five pieces,', nm, res[f'600_triangles_{nm}'])
# edges
PE = [(to5(Wd.PP.P[a]), to5(Wd.PP.P[b])) for a, b in (tuple(e) for e in Wd.PP.edges)]
C(len(PE) == 720, '600-cell: 720 edges')
def edge_sum(E, fins, finite):
    fr = [edge_coverage(a, b, fins, finite)[0] for a, b in E]; return fr
for finite in (True, False):
    nm = 'finite' if finite else 'radial'
    fr = edge_sum(PE, five, finite); res[f'600_edges_{nm}'] = summarize(fr)
    say('600-cell edges by the five pieces,', nm, res[f'600_edges_{nm}'])
# controls: the 600-cell's own fins cover its triangles and edges completely; non-golden orbits do not
own = bydir(PPf)
frc = tri_cov(PPf, own, True); C(all(x == Q5(1) for x in frc), "positive control: the 600-cell's own fins cover all 1200 of its triangles")
fre = edge_sum(PE, PPf, True); C(all(x == Q5(1) for x in fre), "positive control: the 600-cell's own fins cover all 720 of its edges")
def cen(v): m = sum(v, Q5())/5; return tuple(x - m for x in v)
P2 = PHI*PHI
ng = []
for t in [(P2, P2, P2, Q5(Fr(3, 2)), Q5(0)), (P2, P2, Q5(Fr(6, 5)), Q5(Fr(6, 5)), Q5(0))]:
    O = uniq([cen(p) for p in itertools.permutations(t)])
    for sgn in (1, -1):
        ng += faces_of(Poly([to4(vscale(Q5(sgn), p)) for p in O]))
ng += pf['C3']
ngD = bydir(ng)
frn = tri_cov(PPf, ngD, False); res['control_nongolden_triangles_radial'] = summarize(frn)
fen = edge_sum(PE, ng, False); res['control_nongolden_edges_radial'] = summarize(fen)
C(sum(frn, Q5()) < Q5(1200) and sum(fen, Q5()) < Q5(720), f"negative control: non-golden orbits (t = 3/2, 6/5, both signs) + C3 do not cover the skeleton (triangles {float(sum(frn, Q5())/1200):.4f}, edges {float(sum(fen, Q5())/720):.4f})")
# inner fins inside the 600-cell's own cones? (is the 600-cell's Vacuus exactly the union of the pieces' fins)
inner = []
for f in five:
    if f['dir'] in own:
        fr, used, unc = coverage(f['pts'], own[f['dir']], False); inner.append(fr)
res['five_fins_on_mirrors_inside_600_cones'] = summarize(inner) if inner else None
res['five_fins_off_mirrors'] = sum(1 for f in five if f['dir'] not in own)
say('inner fins on mirrors inside the triangle cones:', res['five_fins_on_mirrors_inside_600_cones'], 'fins off the mirrors', res['five_fins_off_mirrors'])

# ---------------- (a2) all golden copies in the 600-cell (all 60 S5s): one triangle and one edge suffice (W(H4)-invariant) ----------------
def pfaces(nm, g):
    for vidx, w in st['bfaces'][nm]:
        yield tuple(int(WP[g][v]) for v in vidx), w
allP = []
for nm in ('A', 'B', 'C3'):
    for S, g in st['cop'][nm]:
        for vidx, w in pfaces(nm, g): allP.append((nm, vidx))
def mkface(pts):
    n = cofactor_normal([pts[0], pts[1], pts[2], ONE]); return {'pts': pts, 'n': n, 'dir': canon_dir(n)}
T = PPf[0]
finsT = {k: [] for k in ('AB', 'ABC3')}
for nm, vidx in allP:
    f = None
    pts = [P5[v] for v in vidx]
    if not dot(T['n'], pts[0]).iszero() or not dot(T['n'], pts[1]).iszero() or not dot(T['n'], pts[2]).iszero(): continue
    f = mkface(pts)
    if f['dir'] != T['dir']: continue
    finsT['ABC3'].append(f)
    if nm != 'C3': finsT['AB'].append(f)
for k in finsT:
    for finite in (True, False):
        fr, used, unc = coverage(T['pts'], finsT[k], finite)
        res[f'600_triangle_allcopies_{k}_{"finite" if finite else "radial"}'] = {'fraction': str(fr), 'float': float(fr), 'fins_in_plane': len(finsT[k]), 'fins_used': used, 'uncovered_pieces': len(unc)}
e0, e1 = PE[0]
finsE = []
for nm, vidx in allP:
    pts = [P5[v] for v in vidx]; f = mkface(pts)
    if dot(f['n'], e0).iszero() and dot(f['n'], e1).iszero(): finsE.append((nm, f))
for k, sel in (('AB', ('A', 'B')), ('ABC3', ('A', 'B', 'C3'))):
    for finite in (True, False):
        L, nint = edge_coverage(e0, e1, [f for nm, f in finsE if nm in sel], finite)
        res[f'600_edge_allcopies_{k}_{"finite" if finite else "radial"}'] = {'fraction': str(L), 'float': float(L), 'intervals': nint}
say('600-cell, all copies:', {k: v for k, v in res.items() if 'allcopies' in k})

# ---------------- (a3) the 120-cell: all golden copies of the 10 inscribed 600-cells ----------------
QQ = Poly(Wd.Q4, '120-cell'); QF = faces_of(QQ); C(len(QF) == 720 and all(len(f['pts']) == 5 for f in QF), '120-cell: 720 pentagons')
QE = [(to5(QQ.P[a]), to5(QQ.P[b])) for a, b in (tuple(e) for e in QQ.edges)]; C(len(QE) == 1200, '120-cell: 1200 edges')
Pent = QF[0]; pg = gid[Pent['dir']]
C(gcat[pg] == 'M', "the 120-cell's pentagons lie on its mirrors (wall category M)")
def qfaces(c):
    nm = c['type']; g = c['g']; i = c['i']
    for vidx, w in st['bfaces'][nm]:
        t, a = w; wa = (t, int(Wd.axP[WP[g][a]])) if t == 'M' else (t, int(Wd.axQ[WQ[g][a]]))
        yield tuple(int(perm_i[i][WP[g][v]]) for v in vidx), (gM[i][wa[1]] if wa[0] == 'M' else gX[i][wa[1]])
finsP = {'AB': [], 'ABC3': []}
wallsE = {w for w in range(len(gcat)) if dot(dvec(gdir[w]), QE[0][0]).iszero() and dot(dvec(gdir[w]), QE[0][1]).iszero()}
finsQE = []
for c in st['copies']:
    for vidx, w in qfaces(c):
        if w == pg:
            f = mkface([Q5s[v] for v in vidx]); assert f['dir'] == Pent['dir']
            finsP['ABC3'].append(f)
            if c['type'] != 'C3': finsP['AB'].append(f)
        if w in wallsE: finsQE.append((c['type'], mkface([Q5s[v] for v in vidx])))
for k in finsP:
    for finite in (True, False):
        fr, used, unc = coverage(Pent['pts'], finsP[k], finite)
        res[f'120_pentagon_{k}_{"finite" if finite else "radial"}'] = {'fraction': str(fr), 'float': float(fr), 'fins_in_plane': len(finsP[k]), 'fins_used': used, 'uncovered_pieces': len(unc)}
for k, sel in (('AB', ('A', 'B')), ('ABC3', ('A', 'B', 'C3'))):
    for finite in (True, False):
        L, nint = edge_coverage(QE[0][0], QE[0][1], [f for nm, f in finsQE if nm in sel], finite)
        res[f'120_edge_{k}_{"finite" if finite else "radial"}'] = {'fraction': str(L), 'float': float(L), 'intervals': nint, 'walls_through_edge': len(wallsE)}
ownQ = bydir(QF)
fq, _, _ = coverage(Pent['pts'], ownQ[Pent['dir']], True); C(fq == Q5(1), "positive control: the 120-cell's own fins cover its pentagon")
inQ = [coverage(f['pts'], ownQ[Pent['dir']], False)[0] for f in finsP['ABC3']]
res['120_copy_fins_on_pentagon_mirror_inside_120_cones'] = summarize(inQ) if inQ else None
say('120-cell:', {k: v for k, v in res.items() if k.startswith('120')})
out['skeleton'] = res

# ---------------- (b) heart / inherited heart / non-heart ----------------
W360 = set(Wd.Mdir) | set(Wd.Xdir)
rows = []
def classify(name, pts4, parent_walls=W360, parent='600-cell/120-cell (360 walls)'):
    poly = Poly(pts4); info, cnt, fs = kind_of(poly)
    inh = all(d in parent_walls for d in cnt)
    pred = 'heart' if info['central_symmetry'] else ('inherited heart' if inh else 'non-heart')
    row = {'shape': name, **info, 'plates_on_parent_walls': sum(1 for d in cnt if d in parent_walls), 'inherits_walls': inh, 'parent': parent,
           'conjecture_predicts': pred, 'agrees': pred == info['kind']}
    rows.append(row); print('KIND', json.dumps(row), flush=True); return row
classify('600-cell', Wd.P4); classify('120-cell', Wd.Q4)
F600 = st['F600']; classify('600-cell inscribed in the 120-cell', [Wd.Q4[i] for i in F600[0]])
S1, S2 = st['states']; T24 = sorted(set(F600[S1[0]]) & set(F600[S2[0]])); classify('24-cell (shared by two inscribed 600-cells)', [Wd.Q4[i] for i in T24])
inv0 = {q: p for p, q in enumerate(perm_i[S1[0]])}; T24P = [inv0[q] for q in T24]
classify('snub 24-cell (600-cell minus an inscribed 24-cell)', [Wd.P4[i] for i in range(120) if i not in T24P])
adjP = {i: set() for i in range(120)}
for a, b in (tuple(e) for e in Wd.PP.edges): adjP[Pk[vkey(to5(Wd.PP.P[a]))]].add(Pk[vkey(to5(Wd.PP.P[b]))]); adjP[Pk[vkey(to5(Wd.PP.P[b]))]].add(Pk[vkey(to5(Wd.PP.P[a]))])
C(all(len(v) == 12 for v in adjP.values()), '600-cell corner graph: 12 neighbours each')
def indep(R): return all(not (adjP[a] & set(R)) for a in R)
dims = {'1 corner': [0]}
far = next(j for j in range(1, 120) if j not in adjP[0] and j != int(Wd.antiP[0])); dims['2 corners, not opposite'] = [0, far]
dims['an opposite pair'] = [0, int(Wd.antiP[0])]
rnd = random.Random(16)
for size in (6, 12, 18):
    while True:
        order = list(range(120)); rnd.shuffle(order); R = []
        for v in order:
            if len(R) < size and not (adjP[v] & set(R)) and v not in R: R.append(v)
        if len(R) == size: break
    dims[f'{size} corners (random independent set, seed 16)'] = R
anti = []
for v in range(120):
    if len(anti) >= 12: break
    if v in anti: continue
    cand = anti + [v, int(Wd.antiP[v])]
    if indep(cand): anti = cand
dims[f'{len(anti)} corners, centrally symmetric independent set'] = anti
for nm, R in dims.items():
    C(indep(R), f'diminishing set "{nm}" is independent')
    classify(f'diminished 600-cell: {nm} removed', [Wd.P4[i] for i in range(120) if i not in R])
for k, S in pieces.items(): classify(f'{k} (in the 600-cell)', [Wd.P4[i] for i in sorted(S)])
cA = next(c for c in st['copies'] if c['type'] == 'A'); cB = next(c for c in st['copies'] if c['type'] == 'B')
for c in (cA, cB):
    i = c['i']; ownw = {gdir[w] for w in set(gM[i].values()) | set(gX[i].values())}
    classify(f"{c['type']} copy in the 120-cell (inscribed 600-cell {i})", [Wd.Q4[j] for j in c['Q']], ownw, f'its inscribed 600-cell (360 walls of its own)')
orbsQ, seen = [], set()
for i, q in enumerate(Q5s):
    if i in seen: continue
    o = sorted({Wd.Qk[vkey(tuple(q[s] for s in sg))] for sg in itertools.permutations(range(5))}); seen |= set(o); orbsQ.append(o)
for o in sorted(orbsQ, key=lambda o: (len(o), o)):
    xs, blocks, gaps = orbit_pattern(Q5s[o[0]])
    classify(f'120-cell S5 orbit of {len(o)} ({A4NAME.get(tuple(blocks), "?")})', [Wd.Q4[i] for i in o])
for t, lab in (((P2, P2, P2, Q5(Fr(3, 2)), Q5(0)), 'non-golden orbit (phi^2,phi^2,phi^2,3/2,0)'), ((P2, P2, Q5(Fr(6, 5)), Q5(Fr(6, 5)), Q5(0)), 'non-golden orbit (phi^2,phi^2,6/5,6/5,0)')):
    classify(lab, [to4(cen(p)) for p in uniq(list(itertools.permutations(t)))])
out['kinds'] = rows
C(all(r['kind'] == 'heart' for r in rows if r['central_symmetry']), 'lemma check: every centrally symmetric shape met is heart kind (at least 2 faces on every plate)')
C(all(r['faces_per_plate_min'] >= 2 for r in rows if r['central_symmetry']), 'lemma check: min faces per plate >= 2 for every centrally symmetric shape')
exc = [r['shape'] for r in rows if not r['agrees']]; out['conjecture_exceptions'] = exc
say('kinds done; conjecture exceptions:', exc)
out['seconds'] = time.time() - T0
json.dump(out, open(os.path.join(OUT, 'skeleton_kinds.json'), 'w'), indent=1, default=str)
C.final()
