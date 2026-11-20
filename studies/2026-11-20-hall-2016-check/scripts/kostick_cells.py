#!/usr/bin/env python3
"""Read Kostick's arrays as rhombic triacontahedra T with some 3-valent corners dimpled.
For every translate T + t that some scene panel fixes (a panel equal to a face of T, or to one of the three inward faces of a
dimple at a 3-valent corner), each of the 20 3-valent corners is read as: plain (its 3 faces of T shown), dimpled (its 3 inward
faces shown), or not shown. The 12 5-valent corners: faces of T not at any 3-valent corner do not exist (every rhombus of T
has two 3-valent corners), so the reading is complete for corner dimples of T.
Also: how the GET A / GET B / candidate 2 surfaces relate to T (faces of T kept; corners dimpled; nested indentations).
Usage: kostick_cells.py <grunbaum-k10 dir> <out json> <shapes.json>..."""
import sys, json, os, itertools, functools, importlib.util
from collections import Counter
here = os.path.dirname(os.path.abspath(__file__))
def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(here, name + '.py')); m = importlib.util.module_from_spec(spec)
    sys_argv = sys.argv; sys.argv = [sys.argv[0], sys.argv[1], '/dev/null']; spec.loader.exec_module(m); sys.argv = sys_argv; return m
hc = load('hall_check')
K10, OUT, FILES = sys.argv[1], sys.argv[2], sys.argv[3:]
PHI = (1 + 5 ** 0.5) / 2
from fractions import Fraction as Fr
def snap(x):
    best = None
    for b in range(-400, 401):
        a = round(2 * x - b * PHI); e = abs((a + b * PHI) / 2 - x)
        if best is None or e < best[0]: best = (e, a, b)
    return (Fr(best[1], 2), Fr(best[2], 2))

T = hc.tri_T(); VT = hc.verts_of(T)
val = {v: sum(1 for f in T if v in f) for v in VT}
three = [v for v in VT if val[v] == 3]
dimple = {}
for v in three:
    F2, vp = hc.remove_rhombohedron(T, v)
    dimple[v] = [frozenset(f) for f in F2 if v not in f and frozenset(f) not in {frozenset(g) for g in T}]
    assert len(dimple[v]) == 3
plain = {v: [frozenset(f) for f in T if v in f] for v in three}
Tfaces = [frozenset(f) for f in T]
c0 = hc.vscale(hc.q(Fr(1, 2)), tuple(hc.add(hc.add(hc.add(hc.add(hc.add(hc.AX[0][i], hc.AX[1][i]), hc.AX[2][i]), hc.AX[3][i]), hc.AX[4][i]), hc.AX[5][i]) for i in range(3)))
d2 = lambda a, b: hc.dot(hc.vsub(a, b), hc.vsub(a, b))

X3 = [hc.AX[0], hc.AX[2], hc.AX[4]]
G0 = [[hc.dot(a, b) for b in X3] for a in X3]
Xi = hc.matinv([list(r) for r in X3])
signed = [hc.vscale(hc.q(s_), a) for a in hc.AX for s_ in (1, -1)]
GROUP = []
for y in itertools.permutations(signed, 3):
    if any(hc.dot(y[i], y[j]) != G0[i][j] for i in range(3) for j in range(3)): continue
    M = [[hc.Z]*3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            acc = hc.Z
            for i in range(3): acc = hc.add(acc, hc.mul(y[i][r], Xi[c][i]))
            M[r][c] = acc
    if not all(hc.dot([M[k][a] for k in range(3)], [M[k][b] for k in range(3)]) == (hc.ONE if a == b else hc.Z) for a in range(3) for b in range(3)): continue
    if {tuple(hc.dot(M[r], a) for r in range(3)) for a in signed} != set(signed): continue
    dt = hc.det3(*[[M[k][c] for k in range(3)] for c in range(3)])
    GROUP.append((M, 1 if dt == hc.ONE else -1))
assert len(GROUP) == 120
def gmap(M, v):   # about T's centre c0
    w = hc.vsub(v, c0); return hc.vadd(c0, tuple(hc.dot(M[r], w) for r in range(3)))
def same_set(A, B):
    """det signs of the symmetries of T taking corner set A onto B"""
    B = set(B); return [dt for M, dt in GROUP if {gmap(M, v) for v in A} == B]

def pattern_class(S):
    """dimpled corner set S (subset of three): its pairwise squared distances multiset, as a coarse invariant + exact class
    by the 120 symmetries fixing T's centre"""
    return sorted(str(hc.sub(d2(a, b), (0, 0))) for a, b in itertools.combinations(S, 2))

out = {'candidates_vs_T': {}, 'files': {}}
SQUARE = None
CAND_DIMS = {}
data = json.load(open(K10 + '/data/search6.json'))
for nm, c in zip(['GET A', 'GET B', 'candidate 2'], data['candidates_rank_le_3'][:3]):
    F = [frozenset(f) for f in hc.cand_faces(c)]
    # translate so that it shares the most faces with T
    best = None
    for f in F:
        for g in Tfaces:
            mf = min(f, key=lambda p: tuple(hc.zf(x) for x in p)) if hasattr(hc, 'zf') else None
            break
        break
    kept = sum(1 for f in F if f in set(Tfaces))
    dims = [v for v in three if all(x in set(F) for x in dimple[v])]
    CAND_DIMS[nm] = dims
    out['candidates_vs_T'][nm] = {'faces_of_T_kept': kept, 'T_corners_dimpled': len(dims),
                                  'all_faces_explained_by_T_plus_corner_dimples': kept + 3 * len(dims) == 30}
    print(nm, out['candidates_vs_T'][nm], flush=True)

zf = lambda u: float(u[0]) + float(u[1]) * PHI
def cmpv(a, b):
    for x, y in zip(a, b):
        s = hc.sgn(hc.sub(x, y))
        if s: return s
    return 0
kmin = lambda F: min(F, key=functools.cmp_to_key(cmpv))

for fn in FILES:
    d = json.load(open(fn)); sh = {s['id']: s for s in d['shapes']}
    panels = []
    for inst in d['instances']:
        s = sh[inst['shape']]
        if len(s['vertices']) != 4: continue
        p = inst['position']
        panels.append([tuple(snap(x) for x in (v['y'] + p['y'], v['x'] + p['x'], v['z'] + p['z'])) for v in s['vertices']])
    # scale: first panel edge = lam * axis
    e0 = hc.vsub(panels[0][1], panels[0][0]); lam = None
    for a in hc.AX:
        for sgn_ in (1, -1):
            a2 = hc.vscale(hc.q(sgn_), a); nz = [i for i in range(3) if a2[i] != hc.Z]
            l = hc.mul(e0[nz[0]], hc.inv(a2[nz[0]]))
            if all(hc.mul(l, a2[i]) == e0[i] for i in range(3)): lam = l
    li = hc.inv(lam)
    pset = {frozenset(tuple(hc.mul(li, c) for c in v) for v in P) for P in panels}
    refs = Tfaces + [f for v in three for f in dimple[v]]
    shapes = {}
    for P in pset:
        mP = kmin(P); dP = {hc.vsub(v, mP) for v in P}
        shapes.setdefault(frozenset(dP), []).append(mP)
    trans = set()
    for f in refs:
        mf = kmin(f); df = frozenset(hc.vsub(v, mf) for v in f)
        for mP in shapes.get(df, []): trans.add(hc.vsub(mP, mf))
    rows = []
    for t in trans:
        sh_ = lambda f: frozenset(hc.vadd(v, t) for v in f)
        pl = [v for v in three if all(sh_(f) in pset for f in plain[v])]
        dm = [v for v in three if all(sh_(f) in pset for f in dimple[v])]
        shown = sum(1 for f in Tfaces if sh_(f) in pset) + sum(1 for v in three for f in dimple[v] if sh_(f) in pset)
        notd = [v for v in three if any(sh_(f) in pset for f in plain[v])]
        rows.append((shown, len(pl), len(dm), t, dm, len(notd), notd))
    rows.sort(key=lambda r: -r[0])
    summ = Counter((r[1], r[2]) for r in rows if r[0] >= 12)
    # classify dimple sets with >= 2 dimples by pairwise distance pattern
    pats = Counter((r[2], tuple(pattern_class(r[4]))) for r in rows if r[0] >= 12 and r[2] >= 1)
    ident = Counter()
    for r in rows:
        if r[0] < 12 or r[2] == 0: continue
        dm0 = list(r[4])   # already corners of T (the translate was applied to the faces)
        lab = []
        for nm, D in CAND_DIMS.items():
            m = same_set(dm0, D)
            if m: lab.append(nm + (' (same hand)' if 1 in m else ' (mirror only)'))
        ident[(r[2], r[2] + r[5] == 20, ', '.join(lab) or 'none of the three')] += 1
    # consistency: could a cell be a copy of a candidate whose dimples are partly not shown?
    cons = Counter(); relsets = Counter()
    for r in rows:
        if r[0] < 12: continue
        dm0 = set(r[4]); nd0 = set(r[6])
        relsets[frozenset(dm0)] += 1
        for nm, D in CAND_DIMS.items():
            ok = any(dm0 <= {gmap(M, v) for v in D} and not (nd0 & {gmap(M, v) for v in D}) for M, dt in GROUP)
            cons[(nm, ok)] += 1
    res = {'cells_identified_(n_dimpled, all_20_corners_decided, matches)': {str(k): v for k, v in ident.items()},
           'cells_(>=12_faces)_consistent_with_candidate': {str(k): v for k, v in cons.items()},
           'distinct_dimple_sets_up_to_translation': len(relsets),
           'distinct_panels': len(pset), 'translates_tested': len(trans),
           'translates_with_>=12_faces_shown': sum(1 for r in rows if r[0] >= 12),
           'counts_(plain_corners,dimpled_corners)': {str(k): v for k, v in summ.items()},
           'dimple_patterns_(n,pairwise_sq_dist)': {str(k): v for k, v in pats.items()},
           'top10_(faces_shown,plain,dimpled)': [(r[0], r[1], r[2]) for r in rows[:10]]}
    def signs(v):
        w = hc.vsub(v, c0); return ''.join('+' if hc.sgn(x) > 0 else ('-' if hc.sgn(x) < 0 else '0') for x in w)
    res['dimple_sets_as_corner_signs'] = {str(sorted(signs(v) for v in k)): n for k, n in Counter({k: relsets[k] for k in relsets if k}).items()}
    if os.path.basename(fn).startswith('concavo'):
        SQUARE = [list(k) for k in relsets if len(k) == 4]
        # lattice of the cells: every difference of translates against GET A's lattice, carried by the symmetry that maps
        # GET A's dimples onto the cells' dimples
        from math import gcd
        D = set(SQUARE[0]); cells_t = [r[3] for r in rows if r[0] >= 12]
        basis = data['candidates_rank_le_3'][0]['test']['basis']
        def coords(z):
            P = (hc.Z, hc.Z, hc.Z)
            for i, m in enumerate(z): P = hc.vadd(P, hc.vscale(hc.q(m), hc.AX[i]))
            return P
        latt = {}
        for M, dt in GROUP:
            if {gmap(M, v) for v in CAND_DIMS['GET A']} != D: continue
            B = [tuple(hc.dot(M[r], coords(b)) for r in range(3)) for b in basis]
            Bi = hc.matinv([list(x) for x in B])     # rows b_k; t = sum c_k b_k  ->  c = t B^{-1}
            coef = []
            allint = True
            for t in cells_t:
                dlt = hc.vsub(t, cells_t[0])
                c = [hc.Z]*3
                for k in range(3):
                    acc = hc.Z
                    for r in range(3): acc = hc.add(acc, hc.mul(dlt[r], Bi[r][k]))
                    c[k] = acc
                if any(x[1] != 0 or x[0].denominator != 1 for x in c): allint = False
                else: coef.append([int(x[0]) for x in c])
            g = 0
            if allint:
                for a3, b3, c3 in itertools.combinations(coef, 3):
                    det = a3[0]*(b3[1]*c3[2]-b3[2]*c3[1]) - a3[1]*(b3[0]*c3[2]-b3[2]*c3[0]) + a3[2]*(b3[0]*c3[1]-b3[1]*c3[0])
                    g = gcd(g, abs(det))
            latt[str(dt)] = {'all_cell_differences_in_GET_A_lattice': allint, 'index_of_generated_sublattice': g}
        res['concavo_lattice_vs_GET_A'] = latt; print('lattice', latt, flush=True)
    out['files'][os.path.basename(fn)] = res
    print(os.path.basename(fn), json.dumps(res), flush=True)
json.dump(out, open(OUT, 'w'), indent=1)
# the concavo-convex cell: T with Kostick's four corners dimpled; compare with all eight rank-3 candidates of search6
if SQUARE:
    D = SQUARE[0]; F = T
    for v in D: F, _ = hc.remove_rhombohedron(F, v)
    cF = hc.centred(F)
    sym = hc.congruences(cF, cF)
    # coplanar adjacent faces: two faces sharing an edge with parallel planes
    def nrm(f): return hc.cross(hc.vsub(f[1], f[0]), hc.vsub(f[3], f[0]))
    cop = 0
    for f, g in itertools.combinations(F, 2):
        if len(set(f) & set(g)) == 2 and hc.cross(nrm(f), nrm(g)) == (hc.Z, hc.Z, hc.Z): cop += 1
    allc = data['candidates_rank_le_3']
    cong = {i: hc.congruences(cF, hc.centred(hc.cand_faces(c))) for i, c in enumerate(allc)}
    sq = {'dimple_set_is_square_of_inscribed_cube': sorted(str(hc.sub(d2(a, b), (0, 0))) for a, b in itertools.combinations(D, 2)),
          'FVE': hc.euler(F), 'symmetries_proper': sym.count(1), 'symmetries_improper': sym.count(-1),
          'coplanar_adjacent_face_pairs': cop,
          'congruent_to_search6_rank3_candidate': {i: len(m) for i, m in cong.items()}}
    out['concavo_cell'] = sq; print('concavo cell', json.dumps(sq))
    json.dump(out, open(OUT, 'w'), indent=1)
cv = out['files'].get('concavo.shapes.json', {})
ok = (cv.get('cells_identified_(n_dimpled, all_20_corners_decided, matches)') == {"(4, False, 'GET A (same hand)')": 19}
      and all(v == {'all_cell_differences_in_GET_A_lattice': True, 'index_of_generated_sublattice': 1} for v in cv.get('concavo_lattice_vs_GET_A', {'x': None}).values())
      and out.get('concavo_cell', {}).get('congruent_to_search6_rank3_candidate', {}).get(0) == 4
      and all(v == 0 for k, v in out.get('concavo_cell', {}).get('congruent_to_search6_rank3_candidate', {}).items() if k != 0))
print('FINAL ok' if ok else 'FINAL FAIL: the concavo cells are not read as GET A on its lattice')
