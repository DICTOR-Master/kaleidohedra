"""Step 5. Exact check (Q(sqrt5), sympy) of the section matches of step 4 that #88 did not state.
(a) Tesseract, vertex-first (direction (1,1,1,1)): the hyperplane x1+x2+x3+x4 = 2h for 0 < h < 1 cuts the 12 edges
    joining the 6 corners with coordinate sum 0 to the 4 with sum 2; the section is the tetrahedron x_i <= 1 cut at its
    corners by x_i >= -1, i.e. a truncated tetrahedron with cut x = (1-h)/(2-h) of its edge.
(b) 120-cell: vertex-first sections matching the Greater and Lesser Golden Cut Tetrahedra, and cell-first sections
    matching the Greater and Lesser Golden Cut Dodecahedra; exact slices from the #65 atlas code (atlas120.py cut()),
    heights identified from the float match and confirmed by exact scale-free congruence (all pairwise squared distances
    over their sum, sorted, equal in Q(sqrt5)), as #88's exact_cmp.py.
usage (compute-host): python s5_exact4d.py -> ../data/s5-exact4d.json
"""
import sys, os, json, itertools
import sympy as sp
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
s5 = sp.sqrt(5); G = (1 + s5) / 2
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def invariant(P):
    P = [sp.Matrix(p) for p in P]; c = sum(P, sp.zeros(len(P[0]), 1)) / len(P); P = [p - c for p in P]
    d2 = [sp.expand((a - b).dot(a - b)) for a, b in itertools.combinations(P, 2)]; tot = sp.expand(sum(d2))
    return sorted((sp.radsimp(x / tot) for x in d2), key=lambda e: float(e))


def same(a, b):
    return len(a) == len(b) and all(abs(sp.N(x - y, 50)) < 1e-40 and sp.simplify(sp.radsimp(x - y)) == 0 for x, y in zip(a, b))


def cut_platonic(P, x):
    P = [sp.Matrix(p) for p in P]
    d = [sp.expand((P[i] - P[j]).dot(P[i] - P[j])) for i, j in itertools.combinations(range(len(P)), 2)]
    m = min(d, key=lambda e: float(e))
    E = [(i, j) for i, j in itertools.combinations(range(len(P)), 2) if sp.simplify(sp.expand((P[i] - P[j]).dot(P[i] - P[j])) - m) == 0]
    return [list(P[i] + x * (P[j] - P[i])) for i, j in E] + [list(P[j] + x * (P[i] - P[j])) for i, j in E]


TET = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
DOD = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
for a in (1, -1):
    for b in (1, -1):
        DOD += [(0, a / G, b * G), (a / G, b * G, 0), (b * G, 0, a / G)]
xG = {'tetrahedron': 1 / G ** 2, 'dodecahedron': sp.Rational(1, 3)}
xL = {'tetrahedron': 1 / (G * s5), 'dodecahedron': (7 - s5) / 22}
out = {}

# (a) tesseract
V8 = [sp.Matrix(v) for v in itertools.product([1, -1], repeat=4)]
B = sp.Matrix([[1, -1, 0, 0], [1, 1, -2, 0], [1, 1, 1, -3]]).T     # orthogonal basis of the hyperplane direction space
def tess_section(h):
    pts = []
    for i, j in itertools.combinations(range(16), 2):
        if sum(abs(V8[i][k] - V8[j][k]) for k in range(4)) != 2: continue
        a, b = sum(V8[i]) - 2 * h, sum(V8[j]) - 2 * h
        if sp.N(a * b) < 0:
            t = a / (a - b); p = V8[i] + t * (V8[j] - V8[i])
            pts.append([sp.radsimp(p.dot(B[:, k]) / sp.sqrt(B[:, k].dot(B[:, k]))) for k in range(3)])
    return pts
rows = []
for h, x, lab in ((1 / G ** 2, xG['tetrahedron'], 'Greater Golden Cut Tetrahedron'), (sp.Rational(1, 2), sp.Rational(1, 3), 'Archimedean truncated tetrahedron'),
                  (1 / G, xL['tetrahedron'], 'Lesser Golden Cut Tetrahedron')):
    S = tess_section(h); ok = same(invariant(S), invariant(cut_platonic(TET, x)))
    check(f'tesseract vertex-first, h = {sp.nsimplify(h)} (layers at 0 and 1; x = (1-h)/(2-h) = {sp.nsimplify(sp.radsimp((1 - h) / (2 - h)))}): {len(S)} corners, exactly {lab}', ok and sp.simplify((1 - h) / (2 - h) - x) == 0)
    rows.append({'polytope': '8-cell', 'direction': 'vertex-first', 'height': str(sp.nsimplify(h)), 'height_note': 'x1+x2+x3+x4 = 2h; corner layers at h = 0 (6 corners) and h = 1 (4 corners); tip h = 2',
                 'solid': lab, 'exact': bool(ok)})
out['tesseract'] = rows

# (b) 120-cell via the #65 atlas
SC = os.path.expanduser('~/work/studies/2026-10-27-white-queen-polar/scripts')
sys.path.insert(0, SC); cwd = os.getcwd(); os.chdir(SC)
import atlas120 as A
os.chdir(cwd)
def q2s(q): return sp.nsimplify(A.q5str(q).replace('√5', '*sqrt(5)').replace(' ', ''))
def slice_exact(lab, h):
    # 4D points (the atlas's 3D slice coordinates use an orthogonal but not normalised basis, which is fine for
    # faces but not for distances off the coordinate axes; distances are taken in 4D)
    d = A.DIRS[lab][0]; H = [A.dot(p, d) for p in A.R]; pts = []
    for p, x in zip(A.R, H):
        if x == h: pts.append(p)
    for a, b in A.E:
        ha, hb = H[a], H[b]
        if ((ha - h) * (hb - h)).sign() < 0:
            t = (h - ha) / (hb - ha); pts.append(tuple(x + t * (y - x) for x, y in zip(A.R[a], A.R[b])))
    # keep hull corners only (drop crossing points that are not corners: none expected for these slices)
    return [[q2s(c) for c in v] for v in pts]
m4 = json.load(open(os.path.join(DATA, 's4-sections4d.json')))['matches']
rows = []
for m in m4:
    if m['polytope'] != '120-cell': continue
    name = m['solid']
    plat = 'tetrahedron' if name.startswith('tetrahedron') else 'dodecahedron' if name.startswith('dodecahedron') else None
    if plat is None: continue
    lab = m['direction']; d = A.DIRS[lab][0]
    tip = max((A.dot(p, d) for p in A.R), key=float)
    hf = m['height_over_top'] * float(tip)
    hs = sp.nsimplify(hf, [s5], tolerance=1e-7)
    a_, b_ = sp.Rational(hs.subs(s5, 0)), sp.Rational(sp.expand((hs - hs.subs(s5, 0)) / s5))
    h = A.Q5(Fr(a_.p, a_.q), Fr(b_.p, b_.q))
    layers = sorted(set(A.dot(p, d) for p in A.R), key=float)
    lo = max((x for x in layers if float(x) <= float(h)), key=float); hi = min((x for x in layers if float(x) >= float(h)), key=float)
    S = slice_exact(lab, h)
    x = xG[plat] if 'greater' in name else xL[plat]
    ok = same(invariant(S), invariant(cut_platonic(TET if plat == 'tetrahedron' else DOD, x)))
    frac = sp.radsimp((q2s(h) - q2s(lo)) / (q2s(hi) - q2s(lo))) if hi != lo else None
    check(f'120-cell {lab}, atlas height {A.q5str(h)} (h/tip {float(h) / float(tip):.8f}; in the gap {A.q5str(lo)} .. {A.q5str(hi)}, fraction {sp.nsimplify(frac, [s5]) if frac is not None else "-"}): {len(S)} points, exactly {name}', ok)
    rows.append({'polytope': '120-cell', 'direction': lab, 'atlas_height': A.q5str(h), 'h_over_tip': float(h) / float(tip),
                 'gap': [A.q5str(lo), A.q5str(hi)], 'fraction_in_gap_from_lower_layer': str(sp.nsimplify(frac, [s5])) if frac is not None else None,
                 'solid': name, 'exact': bool(ok)})
out['120-cell'] = rows
json.dump({'sections': out, 'checks': CHECKS}, open(os.path.join(DATA, 's5-exact4d.json'), 'w'), indent=1)
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
