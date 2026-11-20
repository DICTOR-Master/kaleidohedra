# Gaps batch C, item 1 (R14 / L4): the loose step O ⊂ rTI of #35 (Vajrayana). Does any golden-cut station S of #88 / #91 fit
# O ⊂ λS ⊂ rTI for some scale λ? Exact in Q(sqrt5). -> logs/item1.log
import sys, os, json, itertools
sys.path.insert(0, os.path.dirname(__file__))
from q5 import *
import numpy as np
L = []
def log(s=''): print(s); L.append(s)
here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ref = {k: np.array(v) for k, v in json.load(open(os.path.join(here, 'data/ref-floats-35.json'))).items()}
def match(V, R, tol=2e-6):                       # exact corner set V equals float set R (rounded data of #35) corner for corner
    A = fl(V)
    if len(A) != len(R): return False
    return all(np.min(np.linalg.norm(R - a, axis=1)) < tol for a in A) and all(np.min(np.linalg.norm(A - r, axis=1)) < tol for r in R)

# --- base solids in the standard frame
I0 = cyc([(0, PHI, 1)])   # dual orientation of the cube-frame D0 of #91
D0 = uniq([[Q(a), Q(b), Q(c)] for a in (1, -1) for b in (1, -1) for c in (1, -1)] + cyc([(0, 1 / PHI, PHI)]))
assert len(I0) == 12 and len(D0) == 20
FI0 = facets(I0)
assert all(any(dot(cross(n, v), cross(n, v)) == 0 for v in D0) for n, d in FI0), 'D0 is not the dual orientation of I0'
TI0 = trunc(I0, F(1, 3)); rTI0 = rect(TI0); ID0 = rect(I0)
assert (len(TI0), len(rTI0), len(ID0)) == (60, 90, 30)

# --- the Dharma frame of #35 (icosahedron edge 1/φ): TI0 has edge 2/3, so TI = (3/(2φ))·TI0, possibly mirrored x<->z
swap = lambda V: [[v[2], v[1], v[0]] for v in V]
c = 3 / (2 * PHI); cI = 1 / (2 * PHI)
M = None
for nm, f in (('identity', lambda V: V), ('swap x,z', swap)):
    if match([scl(c, v) for v in f(TI0)], ref['TI']): M = f; log(f'Dharma frame: (3/(2φ))·TI0 under {nm} matches #35 TI corner for corner (60/60)')
assert M is not None
dh = lambda V, s: [scl(s, v) for v in M(V)]
TI = dh(TI0, c); rTI = dh(rTI0, c)
ID = dh(ID0, PHI / 2)
assert match(rTI, ref['rTI']) and match(ID, ref['ID']); log('rTI (90) and ID (30) match #35 corner for corner')

# --- O = OG = H(μ_TI) ∩ φ²D* (#91 Theorem 5), built in the cube frame of D0 (R² = 3), then placed in the Dharma frame
FD0 = facets(D0)
D0star = [scl(1 / d, n) for n, d in FD0]          # polar of D0 in the unit sphere (an icosahedron)
def OGlike(mu, lam=PHI * PHI):
    Hv = uniq(D0 + [scl(mu, v) for v in D0star])
    Hs = facets(Hv) + [(v, lam) for v in D0]      # λD0* = {x : v.x <= λ, v corner of D0}
    return vertices_of(Hs)
muTI = (24 + 9 * S5) / 19
OG = OGlike(muTI); FOG = facets(OG)
log(f'OG = Q(μ_TI, φ²): {len(OG)} corners, {len(FOG)} faces')
assert len(OG) == 102 and len(FOG) == 80
ax = [v for v in OG if v[1] == 0 and v[2] == 0 and v[0].sign() > 0][0][0]
O = dh(OG, (PHI * PHI / 2) / ax)
assert match(O, ref['O']); log(f'O = (φ²/2)/({ax!r}) · OG matches #35 O corner for corner (102/102)')

# --- reproduction controls (#35 Table 1)
FO = facets(O); FrTI = facets(rTI); FTI = facets(TI)
s, t = contain(ID, O, FO); log(f'control ID ⊂ O: factor {s!r}, {t} of 30 corners touch   (#35: tight, 30)'); assert s == 1 and t == 30
s, t = contain(O, rTI, FrTI); log(f'control O ⊂ rTI: factor {s!r} = {s.f():.6f}, {t} touch   (#35: loose)'); assert s < 1
s, t = contain(rTI, TI, FTI); log(f'control rTI ⊂ TI: factor {s!r}, {t} of 90 corners touch   (#35: tight, 90)'); assert s == 1 and t == 90
gap = 1 / contain(O, rTI, FrTI)[0]
log(f'room in the step: O may grow by {gap!r} = {gap.f():.6f} before it leaves rTI')

# --- radius bound, valid in every position (any rotation and translation):
# O ⊂ S ⊂ rTI  =>  S holds a ball of radius r_O and lies in the ball of radius R_rTI, so R_S/r_S <= R_rTI/r_O
# (for S with a centre of symmetry or a Platonic point group, the largest inner and smallest outer balls are centred at its centre).
r2 = lambda Fs: min((d * d / dot(n, n) for n, d in Fs), key=lambda z: z.f())
R2 = lambda V: max((dot(v, v) for v in V), key=lambda z: z.f())
bound2 = R2(rTI) / r2(FO)
log(f'bound: (R_rTI/r_O)² = {bound2!r} = {bound2.f():.6f}  (R_rTI/r_O = {bound2.f() ** .5:.6f})')

# --- the stations
C0 = uniq([[Q(a), Q(b), Q(cc)] for a in (1, -1) for b in (1, -1) for cc in (1, -1)])
O8 = cyc([(1, 0, 0)]); T4 = [v for v in C0 if (v[0] * v[1] * v[2]).sign() > 0]
X = {'GGC Dodecahedron': (D0, F(1, 3)), 'LGC Dodecahedron': (D0, (7 - S5) / 22),
     'GGC Icosahedron': (I0, 1 / (PHI * PHI)), 'LGC Icosahedron': (I0, 1 / (PHI * S5)),
     'GGC Tetrahedron': (T4, 1 / (PHI * PHI)), 'LGC Tetrahedron': (T4, 1 / (PHI * S5)),
     'Icosaxes (GGC Octahedron)': (O8, 1 / (PHI * PHI)), 'Unborn Axes (LGC Octahedron)': (O8, 1 / (PHI * S5))}
log('\nStations (GGC/LGC = Greater/Lesser Golden Cut, #88 Table 2; Golden OGs #91 Theorem 5), D·I·C·T·O order:')
rows = []
def station(nm, S, aligned):
    FS = facets(S); ratio = R2(S) / r2(FS); ok_r = ratio <= bound2
    line = f'  {nm:30s} corners {len(S):3d}  (R_S/r_S)² = {ratio.f():.6f}  radius bound {"passes" if ok_r else "FAILS (no position works)"}'
    if aligned and ok_r:
        l1, t1 = contain(O, S, FS); l2i, t2 = contain(S, rTI, FrTI); l2 = 1 / l2i
        fits = l1 <= l2
        line += f'\n      O ⊂ λS needs λ >= {l1!r} = {l1.f():.6f} ({t1} corners of O touch);  λS ⊂ rTI needs λ <= {l2!r} = {l2.f():.6f} ({t2} corners of S touch)'
        line += f'\n      => {"FITS for λ in [%.6f, %.6f]" % (l1.f(), l2.f()) + (" (touches both: closing solid)" if l1 == l2 else "") if fits else "does NOT fit (exact: λ_min > λ_max)"}'
        rows.append((nm, fits, l1, l2))
    elif aligned: rows.append((nm, False, None, None))
    log(line)
for nm in ('GGC Dodecahedron', 'LGC Dodecahedron', 'GGC Icosahedron', 'LGC Icosahedron'):
    V, x = X[nm]; station(nm, M(trunc(V, x)), True)
for nm in ('Lesser Golden OG', 'Greater Golden OG'):
    mu = S5 if nm.startswith('Lesser') else (13 + 6 * S5) / 11
    G = OGlike(mu); assert len(G) == 102; station(nm, M(G), True)
log('  cube cuts (x involves √2, outside Q(√5)) by closed form, see below')
for nm in ('GGC Tetrahedron', 'LGC Tetrahedron', 'Icosaxes (GGC Octahedron)', 'Unborn Axes (LGC Octahedron)'):
    V, x = X[nm]; station(nm, trunc(V, x), False)
# cube cuts: cube [-1,1]^3, edge 2; cut at x: corners (1, 1, 1-2x) etc.; R² = 2 + (1-2x)²; inner radius = min(1, (3-2x)/√3)
import sympy as sp
k = sp.sqrt(2); ph = (1 + sp.sqrt(5)) / 2
for nm, x in (('GGC Cube', ph / (k + 2 * ph)), ('LGC Cube', 1 / (ph * k + 2))):
    R2c = 2 + (1 - 2 * x) ** 2; r2c = sp.Min(1, (3 - 2 * x) ** 2 / 3)
    ratio = sp.nsimplify(R2c / r2c); val = float(sp.N(R2c / r2c, 30))
    passes = sp.N(R2c / r2c - (bound2.a + bound2.b * sp.sqrt(5)), 50) <= 0
    log(f'  {nm:30s} x = {float(x):.6f}  (R_S/r_S)² = {val:.6f}  radius bound {"passes" if passes else "FAILS (no position works)"}')
# controls for the test itself
log('\nControls of the λ test:')
for nm, S, exp in (('O itself (must fit, λ = 1 .. room)', O, True), ('rTI itself (must fit)', rTI, True),
                   ('ID (must fit? O ⊄ λID for λ <= room)', ID, None), ('I (Dharma icosahedron)', dh(I0, cI), None), ('TI', TI, None)):
    FS = facets(S); l1, _ = contain(O, S, FS); l2 = 1 / contain(S, rTI, FrTI)[0]
    log(f'  {nm:40s} λ_min {l1.f():.6f}  λ_max {l2.f():.6f}  fits {l1 <= l2}')
    if exp is not None: assert (l1 <= l2) == exp
fit = [r for r in rows if r[1]]
log('\nVERDICT: ' + ('stations that fit: ' + ', '.join(r[0] for r in fit) if fit else
    'no golden-cut station of #88/#91 fits O ⊂ S ⊂ rTI at any scale (aligned, exact); the cubic cuts fail in every position.'))
log('FINAL ok')
open(os.path.join(here, 'logs/item1.log'), 'w').write('\n'.join(L) + '\n')
