# Self-building kit screen (DICTO 2026-10-11). Can phi^up x T (T = I, AXE, FUJI, CLEO, A, B, C, K) be cut into kit pieces at
# sizes phi^0 .. phi^-K? Necessary: volume and Dehn invariant both balance with whole-number counts. Exact-ish: coordinates
# snapped to Q(sqrt5), everything at 50 digits, Q-bases of angles (mod pi) and lengths found by PSLQ.
# Also: do the Lotus seed's vertices and Danzer's lie in the same 6D lattice shadow (icosahedral module)?
import json, sys, itertools, numpy as np, mpmath as mp
from scipy.optimize import milp, LinearConstraint, Bounds
mp.mp.dps = 50
R5 = mp.sqrt(5); T = (1 + R5) / 2
K = int(sys.argv[2]) if len(sys.argv) > 2 else 4

def snap(x):
    for den in (1, 2, 4, 8, 3, 6, 12, 24):
        for b in range(-200, 201):
            a = x * den - b * float(R5)
            if abs(a - round(a)) < 5e-6: return (round(a) + b * R5) / den
    raise ValueError(x)

L = json.load(open(sys.argv[1]))
def rep(role, big=True):
    for p in L:
        if p['role'] != role: continue
        V = [[snap(c) for c in v] for v in p['vertices']]
        if role == 'ico':
            e = min(mp.norm(mp.matrix(V[0]) - mp.matrix(w)) for w in V[1:])
            if (e > 0.9) != big: continue
        return V, p['faces']
pieces = {k: rep(r) for k, r in (('I', 'ico'), ('AXE', 'axe'), ('FUJI', 'fuji'), ('CLEO', 'cleo'))}
small_i = rep('ico', big=False)[0]
# Danzer's prototiles (Frettloh, Table 1), halved so the frame matches the edge-1 icosahedron (Danzer's is (0,+-1,+-tau))
DZ = {'A': [(0, 0, 0), (T**3, 0, T**2), (T**2, T**2, T**2), (T**2, 1, 0)],
      'B': [(0, 0, 0), (T**3, 0, T**2), (T**2, T**2, T**2), (T**2, T, 1)],
      'C': [(0, 0, 0), (-T, 0, 1), (T**2, T**2, T**2), (0, T**2, 1)],
      'K': [(0, 0, 0), (-1, T, 0), (T, T, T), (mp.mpf(-1) / 2, 1 / (2 * T), T / 2)]}
for k, V in DZ.items(): pieces[k] = ([[mp.mpf(c) / 2 for c in v] for v in V], [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]])
# Kramer's seven (1982) = Mosseri-Sadoc golden tetrahedra t1..t6 (edges 1 and tau; Koca et al. 2020 Table 1) + T2 = t2 u t4
def tet(d):  # d[(i,j)] = edge length; vertex 3 = apex, 0,1,2 = base
    a = d[(0, 1)]; x2 = (d[(0, 2)] ** 2 + a ** 2 - d[(1, 2)] ** 2) / (2 * a); y2 = mp.sqrt(d[(0, 2)] ** 2 - x2 ** 2)
    x3 = (d[(0, 3)] ** 2 + a ** 2 - d[(1, 3)] ** 2) / (2 * a)
    y3 = (d[(0, 3)] ** 2 - d[(2, 3)] ** 2 + x2 ** 2 + y2 ** 2 - 2 * x2 * x3) / (2 * y2)
    return [[0, 0, 0], [a, 0, 0], [x2, y2, 0], [x3, y3, mp.sqrt(d[(0, 3)] ** 2 - x3 ** 2 - y3 ** 2)]]
def golden(longpairs, L=None):
    return {p: (L or {}).get(p, T if p in longpairs else mp.mpf(1)) for p in itertools.combinations(range(4), 2)}
PAIRS = list(itertools.combinations(range(4), 2))
MSDEF = {'t1': golden([(0, 1)]), 't2': golden([(1, 3), (2, 3)]), 't3': golden([(0, 1), (0, 2), (1, 2)]),
         't4': golden([(0, 3), (1, 3), (2, 3)]), 't5': golden([(0, 1), (0, 2), (1, 2), (2, 3)]),
         't6': golden([p for p in PAIRS if p != (0, 1)]),
         'T2': golden([p for p in PAIRS if p not in ((0, 1), (2, 3))], {(2, 3): T ** 2})}  # opposite edges 1 and tau^2
TF = [[0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]]
for k, d in MSDEF.items(): pieces[k] = (tet(d), TF)

def geom(V, F):
    V = [mp.matrix(v) for v in V]; c = sum(V, mp.matrix([0, 0, 0])) / len(V)
    nrm = []
    vol = 0
    for f in F:
        n = cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]); n = n / mp.norm(n)
        if dot(n, V[f[0]] - c) < 0: n = -n
        nrm.append(n)
        for i in range(1, len(f) - 1): vol += abs(dot(V[f[0]] - c, cross(V[f[i]] - c, V[f[i + 1]] - c))) / 6
    E = {}
    for fi, f in enumerate(F):
        for k in range(len(f)):
            a, b = sorted((f[k], f[(k + 1) % len(f)])); E.setdefault((a, b), []).append(fi)
    out = []
    for (a, b), fs in E.items():
        assert len(fs) == 2
        ang = mp.pi - mp.acos(max(-1, min(1, dot(nrm[fs[0]], nrm[fs[1]]))))
        if abs(ang - mp.pi) < mp.mpf(10) ** -30: continue
        out.append((mp.norm(V[a] - V[b]), ang))
    return vol, out
cross = lambda a, b: mp.matrix([a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]])
dot = lambda a, b: sum(a[i] * b[i] for i in range(3))
G = {k: geom(*v) for k, v in pieces.items()}

def qbasis(xs, extra=()):
    """Q-basis of the span of xs (modulo extra, e.g. pi); returns basis and rational coords of each x."""
    basis, coords = [], []
    for x in xs:
        rel = mp.pslq([x] + basis + list(extra), maxcoeff=10 ** 6, maxsteps=10 ** 6, tol=mp.mpf(10) ** -35) if basis or extra else None
        if rel and rel[0] != 0:
            coords.append([mp.mpf(-r) / rel[0] for r in rel[1:1 + len(basis)]])
        else:
            basis.append(x); coords.append(None)
    # recompute coords against the final basis
    out = []
    for x in xs:
        rel = mp.pslq([x] + basis + list(extra), maxcoeff=10 ** 6, maxsteps=10 ** 6, tol=mp.mpf(10) ** -35)
        out.append([mp.mpf(-r) / rel[0] for r in rel[1:1 + len(basis)]])
    return basis, out

# angle basis (mod pi)
angs = []
for k, (v, es) in G.items():
    for _, a in es:
        if all(abs(a - b) > mp.mpf(10) ** -30 for b in angs): angs.append(a)
angs.sort()
abasis, acoord = qbasis(angs, extra=(mp.pi,))
print('dihedral angles (deg) and their coordinates on the angle basis (mod 180):')
for a, c in zip(angs, acoord): print(f'  {float(mp.degrees(a)):10.5f}  ->  {[mp.nstr(x, 6) for x in c]}')
print('angle basis (deg):', [round(float(mp.degrees(b)), 5) for b in abasis])
acoord = {mp.nstr(a, 30): c for a, c in zip(angs, acoord)}

SIZES = list(range(-K, 3))
lens = []
for k, (v, es) in G.items():
    for l, _ in es:
        for s in SIZES:
            x = l * T ** s
            if all(abs(x - y) > mp.mpf(10) ** -30 for y in lens): lens.append(x)
lbasis, lcoord = qbasis(sorted(lens))
print('length basis:', [mp.nstr(b, 8) for b in lbasis], f'({len(lens)} distinct lengths)')
lmap = list(zip(sorted(lens), lcoord))
def lc(x):
    for y, c in lmap:
        if abs(x - y) < mp.mpf(10) ** -30: return c
    raise KeyError(x)

def dehn(k, s):
    D = np.zeros((len(lbasis), len(abasis)))
    for l, a in G[k][1]:
        D += np.outer([float(x) for x in lc(l * T ** s)], [float(x) for x in acoord[mp.nstr(a, 30)]])
    return D.ravel()
print('\nDehn invariant zero? (edge-1 sizes)')
for k in G: print(f'  {k:5s} volume {float(G[k][0]):.6f}   Dehn {"ZERO" if np.abs(dehn(k, 0)).max() < 1e-9 else "nonzero"}')

def screen(target, up, kit, label, sols=3):
    vt = G[target][0] * T ** (3 * up)
    rhs = np.array([float(vt)] + list(dehn(target, up)))
    var = [(p, s) for p in kit for s in range(-K, 1)]
    cols = np.array([[float(G[p][0] * T ** (3 * s))] + list(dehn(p, s)) for p, s in var]).T
    scale = np.maximum(np.abs(cols).max(1), 1e-12); A_ = cols / scale[:, None]; b_ = rhs / scale
    keep = np.abs(A_).max(1) > 1e-12
    A_, b_ = A_[keep], b_[keep]
    found = []
    cons = [LinearConstraint(A_, b_ - 1e-7, b_ + 1e-7)]
    for _ in range(sols):
        res = milp(c=np.ones(len(var)), constraints=cons, integrality=np.ones(len(var)), bounds=Bounds(0, 2000),
                   options={'time_limit': 120})
        if not res.success: break
        x = np.round(res.x).astype(int); found.append({f'{p}@phi^{s}': int(n) for (p, s), n in zip(var, x) if n})
        break                                                    # the fewest-piece recipe only
    print(f'  phi^{up} x {target:4s} from {label}: ' + ('NONE (volume + Dehn have no whole-number solution)' if not found else ''))
    for f in found: print(f'      {sum(f.values())} pieces: {f}')
    return bool(found)

OURS = ['I', 'AXE', 'FUJI', 'CLEO']; DAN = ['A', 'B', 'C', 'K']; MS7 = ['t1', 't2', 't3', 't4', 't5', 't6', 'T2']
print(f'\nScreen: kit sizes phi^0 .. phi^-{K}')
print('volumes (x12):', {k: mp.nstr(G[k][0] * 12, 8) for k in MS7})
print('sanity: phi x t1..t6 from t1..t6 (Mosseri-Sadoc inflation must pass); I from MS at phi^0 (Koca: 7t1+6t2+2t5+t6)')
for t in MS7[:6]: screen(t, 1, MS7[:6], 'MS six', sols=1)
screen('I', 0, MS7[:6], 'MS six (same size)', sols=1) if False else None
for t in OURS: screen(t, 0, MS7, 'Kramer seven, sizes <= own size')
for up in (1, 2):
    print(f'\nup = phi^{up}')
    for t in OURS: screen(t, up, OURS + MS7, 'our kit + Kramer seven')
# 6D shadow check: write each vertex on the 6 five-fold axes of the edge-1 icosahedron, using the Galois star map (tau -> -1/tau)
ax = [(1, T, 0), (-1, T, 0), (0, 1, T), (0, -1, T), (T, 0, 1), (-T, 0, 1)]
def gal(x):  # x = (a + b sqrt5)/den  ->  (a - b sqrt5)/den
    for den in (1, 2, 4, 8, 16, 3, 6, 12, 24):
        for b in range(-400, 401):
            a = x * den - b * R5
            if abs(a - mp.nint(a)) < mp.mpf(10) ** -30: return (mp.nint(a) - b * R5) / den
    raise ValueError(x)
M = mp.matrix(6, 6)
for j, v in enumerate(ax):
    for i in range(3): M[i, j] = mp.mpf(v[i]) / 2; M[i + 3, j] = gal(mp.mpf(v[i]) / 2)
Mi = M ** -1
def lift(p):
    rhs = mp.matrix([p[0], p[1], p[2], gal(p[0]), gal(p[1]), gal(p[2])]); n = Mi * rhs
    return [mp.nstr(mp.nint(4 * x) / 4, 4) if abs(4 * x - mp.nint(4 * x)) < 1e-25 else 'irrational' for x in n]
print('\n6D lift on the edge-1 icosahedron axes (integers = vertex of Z^6 shadow):')
seen = set()
for k in OURS + DAN:
    for v in pieces[k][0]:
        key = tuple(lift(v))
        if key in seen: continue
        seen.add(key)
dens = {}
for k in OURS + DAN + MS7:
    ls = [lift(v) for v in pieces[k][0]]
    kinds = set()
    for l in ls:
        if 'irrational' in l: kinds.add('outside module'); continue
        f = [mp.mpf(x) for x in l]
        if all(x == mp.nint(x) for x in f): kinds.add('integer, sum ' + ('even' if int(sum(f)) % 2 == 0 else 'odd'))
        elif all(2 * x == mp.nint(2 * x) for x in f): kinds.add('half-integer')
        else: kinds.add('quarter')
    print(f'  {k:5s}: {sorted(kinds)}')
ls = [lift(v) for v in small_i]
print('  small i:', sorted({('integer' if all(mp.mpf(x) == mp.nint(mp.mpf(x)) for x in l) else 'fraction') for l in ls}))
