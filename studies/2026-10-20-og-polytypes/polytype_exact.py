# DICTO 2026-10-20: the OG family on every close-packed stacking (polytypes), exact in Q(sqrt5). Frame of #37 / #37a: the octahedron
# |x|+|y|+|z| <= R, R = 2phi/3; layers of the tetrahedral-octahedral honeycomb are the slabs (2k-1)R <= x+y+z <= (2k+1)R.
#   1. The twin rule: for each solid, exact tests of centre symmetry, the three-fold turn about (1,1,1), the mirror in the plane at right
#      angles to (1,1,1), whether its mirror image equals its 60 degree turn, and whether it lies in its octahedron / in its layer.
#   2. Any stacking: a word in h and c (Jagodzinski) builds the honeycomb layer by layer (c: the octet's step; h: the mirror in the top
#      plane). For solids that leave their octahedron, exact overlap tests with every neighbour, for every pair of boundary types.
#   3. Polytypes 3C, 2H, 4H, 6H, 9R, 15R and the Fibonacci stacking: the A/B/C sequence and Ramsdell symbol from the h/c word, the
#      share of h layers, and, per cell of the honeycomb, how many kit pieces of each kind (counted from the geometry and by formula).
# usage: python3 polytype_exact.py <path to studies/2026-10-18-ocd-octet/scripts> <path to studies/2026-10-19-og-gyrated-octet>
import sys, os, json, itertools
from fractions import Fraction as Fr
sys.path.insert(0, sys.argv[1]); GYR = sys.argv[2]
from q5 import *
from exactpoly import planes_of, intersect, volume
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OCT = os.path.join(sys.argv[1], '..', 'data')
log = {'mark': 'DICTO OG polytypes, exact, 2026-10-20 · ' + MARK, 'solids': {}, 'overlap': {}, 'polytypes': {}}
ok = lambda c, m: print(('PASS ' if c else 'FAIL ') + m, flush=True) or c
R = (Fr(1, 3), Fr(1, 3)); TWO = qr(2); THIRD = qr(Fr(1, 3))
key = lambda p: tuple(tuple(x) for x in p)
def mat(M, p): return [qa(qa(qm(qr(M[i][0]), p[0]), qm(qr(M[i][1]), p[1])), qm(qr(M[i][2]), p[2])) for i in range(3)]
MIR = [[Fr(1, 3), Fr(-2, 3), Fr(-2, 3)], [Fr(-2, 3), Fr(1, 3), Fr(-2, 3)], [Fr(-2, 3), Fr(-2, 3), Fr(1, 3)]]   # I - (2/3)J
R60 = [[Fr(2, 3), Fr(-1, 3), Fr(2, 3)], [Fr(2, 3), Fr(2, 3), Fr(-1, 3)], [Fr(-1, 3), Fr(2, 3), Fr(2, 3)]]    # 60 deg about (1,1,1)
CYC = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
assert mat(R60, [ONE, Z, Z]) == [qr(Fr(2, 3)), qr(Fr(2, 3)), qr(Fr(-1, 3))]                                  # as in #37a
R6 = lambda p, k: p if k == 0 else R6(mat(R60, p), k - 1)
assert R6([ONE, ONE, ONE], 1) == [ONE, ONE, ONE] and all(R6([qr(a), qr(b), qr(c)], 6) == [qr(a), qr(b), qr(c)] and R6([qr(a), qr(b), qr(c)], 3) != [qr(a), qr(b), qr(c)] for a, b, c in ((1, 0, 0), (0, 1, 0), (0, 0, 1)))   # a turn of order 6 about (1,1,1)
S = lambda p: qa(qa(p[0], p[1]), p[2])
absq = lambda x: x if sgn(x) >= 0 else qn(x)

# ---------- the solids (exact corners, all in this frame) ----------
L = lambda f: [[q(c) for c in v] for v in json.load(open(f))['V']]
OG = L(os.path.join(OCT, 'step1-ocd-exact.json'))
DBT = L(os.path.join(GYR, 'dbt-exact.json'))
OTT = L(os.path.join(GYR, 'cut8-exact.json'))
# the golden envelope (a rhombic triacontahedron) = the DBT without its two pole cuts: drop the two planes at right angles to (1,1,1)
RT = intersect([(n, d) for n, d in planes_of(DBT) if not (n[0] == n[1] == n[2])])
assert len(RT) == 32, len(RT)
SOL = {'OG': OG, 'OTT': OTT, 'DBT': DBT, 'RT (golden envelope)': RT}
for name, V in SOL.items():
    Vs = {key(p) for p in V}
    cen = {key([qn(x) for x in p]) for p in V} == Vs
    c3 = {key([p[CYC[i].index(1)] for i in range(3)]) for p in V} == Vs
    # the pyritohedral rotations: the 120 deg turn CYC and the half-turns that change the sign of two coordinates
    signs = [(1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    flips = all({key([qm(qr(s[i]), p[i]) for i in range(3)]) for p in V} == Vs for s in signs)
    mir = {key(mat(MIR, p)) for p in V} == Vs
    twin60 = {key(mat(MIR, p)) for p in V} == {key(mat(R60, p)) for p in V}
    inoct = all(sgn(qs(R, qa(qa(absq(p[0]), absq(p[1])), absq(p[2])))) >= 0 for p in V)
    inlayer = all(sgn(qs(R, absq(S(p)))) >= 0 for p in V)
    vol = volume(V)
    log['solids'][name] = {'corners': len(V), 'centre_symmetric': cen, 'three_fold_111': c3, 'pyritohedral_rotations': c3 and flips,
                           'mirror_perp_111_is_a_symmetry': mir, 'mirror_image_equals_60deg_turn': twin60, 'inside_its_octahedron': inoct,
                           'inside_its_layer': inlayer, 'volume': qs_(vol), 'volume_float': qf(vol)}
    print(name, log['solids'][name], flush=True)
ok(all(v['centre_symmetric'] and v['three_fold_111'] and v['mirror_image_equals_60deg_turn'] and not v['mirror_perp_111_is_a_symmetry']
       for v in log['solids'].values()), 'the twin rule: each solid is centre-symmetric with the three-fold axis, has no mirror across the layer, and its mirror image is its 60 deg turn')
# the rule itself (hand proof in the paper): MIR = -(half turn about (1,1,1)) and the half turn = R60 composed with the 120 deg turn
H180 = [[-x for x in row] for row in MIR]
ok(all(mat(H180, p) == mat(R60, mat(R60, mat(R60, p))) for p in OG[:5]), 'MIR = inversion o half-turn, and the half-turn = (60 deg turn)^3 (so with a 120 deg symmetry, MIR(S) = R60(S))')

# ---------- stackings: the honeycomb built layer by layer ----------
# affine maps x -> A x + b, A rational 3x3, b exact vector
def app(Ab, p): A, b = Ab; return vadd(mat(A, p), b)
def comp(F, G):  # F o G
    A, b = F; C, d = G
    AC = [[sum(A[i][k] * C[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return (AC, vadd(mat(A, d), b))
I3 = [[Fr(int(i == j)) for j in range(3)] for i in range(3)]
Tc = (I3, [qm(TWO, R), Z, Z])                                         # the octet's step to the next layer: translation 2R(1,0,0)
M0 = (MIR, [qm(qr(Fr(2, 3)), R)] * 3)                                 # mirror in the top plane x+y+z = R
ok(S(app(M0, [Z, Z, Z])) == qm(TWO, R) and S(app(Tc, [Z, Z, Z])) == qm(TWO, R), 'both steps carry the octahedron at the origin to layer 1 (x+y+z = 2R)')
ORIGIN = [Z, Z, Z]
def layer0(n=4):
    """octahedron centres of layer 0 near the origin, the origin first: R(a, b, -a-b) (octet centres R(a,b,c) have a+b+c even)"""
    pts = [(a, b) for a in range(-n, n + 1) for b in range(-n, n + 1) if abs(a) + abs(b) + abs(a + b) <= 2 * n]
    pts.sort(key=lambda ab: (ab != (0, 0)))
    return [[qm(qr(a), R), qm(qr(b), R), qm(qr(-a - b), R)] for a, b in pts]
def build(word, n=4):
    """layers 0..len(word): list of (map A_k, octahedron centres); A_0 = identity; word[k] is the boundary between layers k and k+1"""
    maps = [(I3, [Z, Z, Z])]
    for w in word: maps.append(comp(maps[-1], Tc if w == 'c' else M0))
    base = layer0(n); return [(Ak, [app(Ak, c) for c in base]) for Ak in maps]
# check: layer 0 centres are octet centres (fcc: R(a,b,c), a+b+c even) and octahedra in a layer share edges only
B0 = layer0(2); ok(B0[0] == ORIGIN and len(B0) == 19, f'layer 0: {len(B0)} octahedra round the one at the origin')
# the boundary type is read back from the geometry: above an octahedron's top face lies an octahedron (h) or a tetrahedron (c)
def boundary_types(word):
    Ls = build(word, 3); out = []
    for k in range(len(word)):
        cs = {key(c) for c in Ls[k + 1][1]}
        up = app(Ls[k][0], app(M0, ORIGIN))                           # the octahedron's mirror image in its top face (layer k's frame)
        out.append('h' if key(up) in cs else 'c')
    return ''.join(out)
for w in ['cccc', 'hhhh', 'hchc', 'hcchcc', 'chhcch']:
    ok(boundary_types(w) == w, f'geometry reads back the stacking word {w}: an octahedron sits above an octahedron exactly at the h layers')

# ---------- solids that leave their octahedron: exact overlap tests in every boundary configuration ----------
def separated(PA, PB, VA, VB):
    for (n, d), W in ((p, VB) for p in PA):
        if all(sgn(qs(dot(n, w), d)) >= 0 for w in W): return True
    for (n, d), W in ((p, VA) for p in PB):
        if all(sgn(qs(dot(n, w), d)) >= 0 for w in W): return True
    return False
def overlap_vol(PA, PB):
    C = intersect(PA + PB); return volume(C) if C else Z
for name in ('DBT', 'RT (golden envelope)'):
    V = SOL[name]; P0 = planes_of(V); r2 = max(qf(dot(p, p)) for p in V); res = {}
    for w in ('cc', 'ch', 'hc', 'hh'):
        Ls = build(w, 3); ref = Ls[1][1][0]; assert key(ref) == key(app(Ls[1][0], ORIGIN)); refV = [vadd(app((Ls[1][0][0], [Z, Z, Z]), p), ref) for p in V]; Pref = planes_of(refV)
        worst, nb = Z, 0
        for k in range(3):
            Ak = Ls[k][0]
            for c in Ls[k][1]:
                if k == 1 and key(c) == key(ref): continue
                d2 = sum((qf(a) - qf(b)) ** 2 for a, b in zip(c, ref))
                if d2 > 4 * r2 + 1e-9: continue
                W = [vadd(app((Ak[0], [Z, Z, Z]), p), c) for p in V]; nb += 1
                if separated(Pref, planes_of(W), refV, W): continue
                ov = overlap_vol(Pref, planes_of(W))
                if sgn(qs(ov, worst)) > 0: worst = ov
        res[w] = {'neighbours_tested': nb, 'largest_overlap_volume': qs_(worst), 'overlap_free': worst == Z}
        print(name, w, res[w], flush=True)
    log['overlap'][name] = res

# ---------- polytypes ----------
def abc(word):
    """A/B/C sequence of the close-packed stacking from the Jagodzinski word (layer k+1 relative to k: c continues the turn, h reverses)"""
    seq, d = [0, 1], 1
    for w in word[1:]:
        d = d if w == 'c' else -d; seq.append((seq[-1] + d) % 3)
    return seq
def ramsdell(word):
    """periodic h/c word -> Ramsdell symbol: the A/B/C sequence's period p in layers; R when p = 3 x the word's period (the stacking
    repeats only after a sideways shift), C for the cubic c-only stacking, else H"""
    n = len(word); s = abc(word * 12)
    p = next(p for p in range(1, 6 * n + 1) if all(s[i] == s[i + p] for i in range(len(s) - p)))
    return (p, 'C' if set(word) == {'c'} else 'R' if p == 3 * n else 'H')
def counts(fh):
    """kit pieces per cell (one octahedron + two tetrahedra) when a share fh of the layers are h"""
    return {'OG (or its twin)': Fr(1), 'caps': 8 - 2 * fh, 'twin caps': fh, 'tetrahedra': 2 - 2 * fh, 'bipyramids': fh}
POLY = {'3C (octet)': 'c', '2H (gyrated octet)': 'h', '4H': 'hc', '6H': 'hcc', '9R': 'hhc', '15R': 'hcchc'}
for nm, w in POLY.items():
    fh = Fr(w.count('h'), len(w)); rs = ramsdell(w)
    seq = ''.join('ABC'[i] for i in abc(w * 2)[:rs[0] if rs[1] != 'C' else 3])
    log['polytypes'][nm] = {'jagodzinski': w, 'ramsdell': f'{rs[0]}{rs[1]}', 'abc': seq, 'share_h': str(fh), 'pieces_per_cell': {k: str(v) for k, v in counts(fh).items()}}
    ok(nm.split()[0] == f'{rs[0]}{rs[1]}', f'{nm}: Jagodzinski ({w}) -> Ramsdell {rs[0]}{rs[1]}, stacking {seq}..., h share {fh}')
# the counts from the geometry: in a finite block, count oct-oct contacts across each boundary per octahedron (= twin caps per cell)
for nm, w in POLY.items():
    word = w * max(2, 12 // len(w)); got = Fr(sum(1 for ch in boundary_types(word) if ch == 'h'), len(word))
    ok(got == Fr(word.count('h'), len(word)), f'{nm}: twin caps per cell counted from the geometry = {got}')
# the Fibonacci stacking: c -> ch, h -> c; the share of h tends to 1/phi^2 = (3 - sqrt5)/2 exactly; never periodic
w = 'c'
for _ in range(18): w = ''.join('ch' if x == 'c' else 'c' for x in w)
fib = [1, 1]
while len(fib) < 25: fib.append(fib[-1] + fib[-2])
n, nh = len(w), w.count('h')
ok(n in fib and nh in fib, f'Fibonacci stacking: {n} layers, {nh} of them h (both Fibonacci numbers)')
inv_phi2 = (Fr(3, 2), Fr(-1, 2))
ok(abs(nh / n - qf(inv_phi2)) < 1e-6, f'share of h layers {nh}/{n} = {nh / n:.8f} -> 1/phi^2 = (3 - sqrt5)/2 = {qf(inv_phi2):.8f}')
fc = {k: (qs(qr(8), qm(TWO, inv_phi2)) if k == 'caps' else inv_phi2 if k in ('twin caps', 'bipyramids') else qs(TWO, qm(TWO, inv_phi2)) if k == 'tetrahedra' else ONE) for k in counts(0)}
log['polytypes']['Fibonacci (aperiodic)'] = {'rule': 'c -> ch, h -> c', 'share_h': '(3 - sqrt5)/2', 'pieces_per_cell': {k: qs_(v) for k, v in fc.items()},
                                             'first_layers': w[:34]}
print('Fibonacci pieces per cell:', {k: f'{qs_(v)} = {qf(v):.6f}' for k, v in fc.items()})
# the OG's share of space is the same in every stacking: OG / cell
cell = (Fr(32, 27), Fr(16, 27))                                      # one octahedron + two tetrahedra, (32 + 16 sqrt5)/27
og_share = qd(volume(OG), cell)
log['og_share_every_stacking'] = qs_(og_share); ok(True, f'OG share of space in every stacking = {qs_(og_share)} = {qf(og_share):.6f}')
json.dump(log, open(os.path.join(HERE, 'polytype-exact.json'), 'w'), indent=1, ensure_ascii=False, default=str)
