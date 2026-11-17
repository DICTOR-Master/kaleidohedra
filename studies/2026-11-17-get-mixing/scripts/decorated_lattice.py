#!/usr/bin/env python3
"""Q3/Q4 beyond layers: the decorated lattice.
S = the shapes (Y, g, w) (Y in A, B, C; g a symmetry; w in Z^6) reachable from A at the origin by the exact layer swaps of layers.py,
each with face-to-face lattice exactly L (GET's lattice). A configuration puts one shape of S at every point t of L (tile s + t).
Every shape has volume = covolume(L) exactly, so a PERIODIC configuration with no two overlapping tiles has density 1 and is a
tiling. (For a non-periodic configuration this shortcut fails: holes of density zero can remain; decorated_sft.py adds the exact
local face condition.) The forbidden pairs (s at 0, s' at lambda overlap) are computed EXACTLY here for all lambda that can
matter (bounding spheres), and every allowed contact is checked to be face to face. Then:
  - the forbidden-pair table,
  - exact counts of all configurations periodic under n*L-type sublattices (SAT enumeration with pysat; tori L/(n1 b1 + n2 b2 + n3 b3)),
    which show how the freedom grows (layers: 2^n-type; bulk: 2^(c n^3)-type).
Usage: decorated_lattice.py <k10 dir> <inchbald json> <layers json> <out json>"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from mixlib import *
from fractions import Fraction as Fr
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
t0 = time.time()
sol = load_solids(sys.argv[1], sys.argv[2]); LY = json.load(open(sys.argv[3]))
BL = sol['A']['basis']; Bm = np.array(BL)
EF = np.array([[zfloat(c) for c in e] for e in G.E]); Bf = Bm.astype(float) @ EF
def coords_L(v):
    c, *_ = np.linalg.lstsq(Bm.T.astype(float), np.array(v, float), rcond=None); r = np.round(c).astype(int)
    return r if (r @ Bm == np.array(v)).all() else None
def lattice_of(Y, g):
    F = tfaces(sol[Y]['faces'], g, (0,)*6); byp = {}
    for f, s in F.items(): byp.setdefault((f[1], f[2]), []).append(f)
    lam = [tuple(a - b for a, b in zip(*[x[0] for x in sorted(byp[pr], key=lambda f: -F[f])])) for pr in byp]
    return int_rank_basis([list(v) for v in lam])
def same_L(B):
    return all(coords_L(v) is not None for v in B) and all(
        np.linalg.matrix_rank(np.array(B)) == 3 and np.linalg.lstsq(np.array(B, float).T, np.array(v, float), rcond=None) is not None
        and _inmod(B, v) for v in BL)
def _inmod(B, v):
    c, *_ = np.linalg.lstsq(np.array(B, float).T, np.array(v, float), rcond=None); r = np.round(c).astype(int)
    return (r @ np.array(B) == np.array(v)).all()
LT = LY['layer_types']
# closure from A g0 at w = 0
start = ('A', IDENT, (0,)*6)
key = lambda Y, g: (Y, canon_t(tfaces(sol[Y]['faces'], g, (0,)*6)))
types_by_key = {}
for k, L in enumerate(LT): types_by_key.setdefault(key(L['Y'], L['g']), []).append(k)
def equal_mod_L(Y, g, w, Y2, g2, w2):
    if key(Y, g) != key(Y2, g2): return False
    F1 = tfaces(sol[Y]['faces'], g, w); F2 = tfaces(sol[Y2]['faces'], g2, w2)
    m1 = tuple(min(f[0][i] for f in F1) for i in range(6)); m2 = tuple(min(f[0][i] for f in F2) for i in range(6))
    return coords_L(tuple(a - b for a, b in zip(m1, m2))) is not None
S = [start]
# direct swaps of the layer types of A (identity image, offset 0), any plane
for sw in LY['swaps']:
    for a, b, sgn in ((sw['U'], sw['V'], 1), (sw['V'], sw['U'], -1)):
        U, V = LT[a], LT[b]
        if not (U['Y'] == 'A' and U['g'] == IDENT): continue
        new = (V['Y'], V['g'], tuple(sgn*x for x in sw['w']))
        if not same_L(lattice_of(new[0], new[1])): continue
        if any(equal_mod_L(*new, *s_) for s_ in S): continue
        S.append(new)
print('shapes in S (reachable by swaps, lattice L):', len(S), [(s[0], s[1], s[2]) for s in S], flush=True)
# exact forbidden table
cent = []; rad = []
for Y, g, w in S:
    F = tfaces(sol[Y]['faces'], g, w); P = np.array([np.array(v, float) @ EF for f in F for v in corners(f, 6)])
    cent.append(P.mean(0)); rad.append(np.linalg.norm(P - P.mean(0), axis=1).max())
dual = np.linalg.inv(Bf).T; Rm = max(rad); spread = max(np.linalg.norm(np.array(cent) - c, axis=1).max() for c in cent)
bound = [int((2*Rm + spread)*np.linalg.norm(dual[k])) + 1 for k in range(3)]   # covers every lambda with |c_j + lambda - c_i| <= r_i + r_j
print('coefficient bounds', bound, flush=True)
forb = []; allowed = []; nonftf = []; checked = 0
def ftf_contact(F1, F2):
    """exact: every pair of coplanar faces of the two surfaces whose interiors overlap is one shared face (zsurf.coplanar_overlap:
    in-plane coordinates of the offset both of size < 1). Faces with the same plane pair and offset in the plane only."""
    for f in F1:
        for g in F2:
            if f[1:] != g[1:] or f == g: continue
            if coplanar_overlap(G, None, {'perpair': {(f[1], f[2]): [f, g]}}): return False
    return True
for i, (Y1, g1, w1) in enumerate(S):
    C1 = [(tcell(c, g1, w1), s) for c, s in sol[Y1]['cells']]
    for j, (Y2, g2, w2) in enumerate(S):
        for co in itertools.product(*[range(-b, b + 1) for b in bound]):
            if co == (0, 0, 0): continue
            lam = tuple(int(x) for x in np.array(co) @ Bm)
            c2 = cent[j] + np.array(co, float) @ Bf
            if np.linalg.norm(c2 - cent[i]) > rad[i] + rad[j] + 1e-6: continue
            checked += 1
            C2 = [(tcell(c, g2, tuple(a + b for a, b in zip(w2, lam))), s) for c, s in sol[Y2]['cells']]
            if overlaps(C1, C2): forb.append((i, j, list(co)))
            else:
                allowed.append((i, j, list(co)))
                if not ftf_contact(tfaces(sol[Y1]['faces'], g1, w1), tfaces(sol[Y2]['faces'], g2, tuple(a + b for a, b in zip(w2, lam)))):
                    nonftf.append((i, j, list(co)))
print('pairs (s, s\', lambda) checked exactly:', checked, 'forbidden:', len(forb), f't={time.time()-t0:.0f}s', flush=True)
fset = {(i, j, tuple(c)) for i, j, c in forb}
# self-consistency: each shape alone (its lattice tiling) must have no forbidden self pair
selfbad = [f for f in forb if f[0] == f[1]]
print('allowed pairs whose contact is not face to face:', len(nonftf))
for i, j, c in nonftf: print('   not face to face: shape', i, 'at 0, shape', j, 'at', c)
print('forbidden self pairs (must be 0, each shape tiles by L):', len(selfbad))
for i in range(len(S)):
    for j in range(len(S)):
        if i == j: continue
        fl = sorted(tuple(c) for a, b, c in forb if a == i and b == j)
        if fl: print(f'   shape {i} at 0 forbids shape {j} at', fl)
# torus counts
def count_torus(n, cap=20000):
    pts = list(itertools.product(range(n[0]), range(n[1]), range(n[2]))); idx = {p: k for k, p in enumerate(pts)}; m = len(S)
    var = lambda p, s: idx[p]*m + s + 1
    cl = []; top = len(pts)*m
    for p in pts:
        enc = CardEnc.equals(lits=[var(p, s) for s in range(m)], bound=1, top_id=top, encoding=EncType.pairwise); cl += enc.clauses
    for p in pts:
        for i, j, co in fset:
            q = tuple((p[k] + co[k]) % n[k] for k in range(3))
            if q == p and i != j: continue      # aliasing onto itself with a different shape: impossible anyway (one shape per point)
            if q == p and i == j: cl.append([-var(p, i)]); continue
            cl.append([-var(p, i), -var(q, j)])
    cnt = 0; kinds = {}
    with Cadical153(bootstrap_with=cl) as Sv:
        while cnt < cap and Sv.solve():
            md = Sv.get_model(); ch = tuple(s for p in pts for s in range(m) if md[var(p, s) - 1] > 0)
            cnt += 1; kinds[tuple(sorted(set(ch)))] = kinds.get(tuple(sorted(set(ch))), 0) + 1
            Sv.add_clause([-var(p, s) for p, s in zip(pts, ch)])
    return cnt, cnt < cap, kinds
tor = {}
fset_all = set(fset); fset_ftf = fset | {(i, j, tuple(c)) for i, j, c in nonftf}
subs = {'all': list(range(len(S)))}
for Y in 'ABC': subs[Y + ' only'] = [k for k, s_ in enumerate(S) if s_[0] == Y]
subs['A, B (identity images)'] = [k for k, s_ in enumerate(S) if s_[1] == IDENT]
for nm, sub in subs.items():
    for mode, FS in (('tiling', fset_all), ('face-to-face tiling', fset_ftf)):
        for nn in ((2, 2, 2), (3, 3, 3)):
            fset = {(i, j, c) for i, j, c in FS if i in sub and j in sub}
            Ssave = S; idxmap = {k: q for q, k in enumerate(sub)}
            fset = {(idxmap[i], idxmap[j], c) for i, j, c in fset}
            S = [Ssave[k] for k in sub]
            c, comp, kinds = count_torus(nn)
            S = Ssave
            tor[f'{nm} | {mode} | {nn}'] = {'count': c, 'complete': comp, 'mixed': sum(v for k, v in kinds.items() if len(k) > 1)}
            print(f'torus {nn} {nm:24s} {mode:20s} configurations {c}{"" if comp else " (capped)"}, using more than one shape: {sum(v for k, v in kinds.items() if len(k) > 1)}', flush=True)
json.dump({'S': [list(map(lambda x: list(x) if isinstance(x, tuple) else x, s)) for s in S], 'forbidden': forb, 'allowed': allowed, 'not_face_to_face': nonftf,
           'torus_counts': tor}, open(sys.argv[4], 'w'))
print('FINAL ok' if not selfbad and len(S) >= 1 else 'FINAL FAIL: a shape forbids its own lattice tiling')
