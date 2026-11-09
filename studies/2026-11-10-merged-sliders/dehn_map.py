"""Merged sliders (DICTO 10 Nov 2026: 'two of our sliders could be merged ... one slider goes from cube to RD and the other from
cube to octahedron'; chose option A, keys for c/h layering). Step 1, the map. P(lam, mu) = cube {|x_i| <= 1} ∩ lam·RD
{|x_i| + |x_j| <= lam} ∩ octahedron {|x_1|+|x_2|+|x_3| <= mu}, lam in [1, 2] (2: cube, 1: Kepler's RD), mu in [1, 3]
(3: no cut, 1: the octahedron). Every face normal is of type <100>, <110> or <111>, so every dihedral angle is a rational multiple
of pi plus k·theta, theta = arccos(1/sqrt3) (k in {0, ±1, ±2}). The Dehn invariant is L ⊗ theta with L = sum over edges of
length × k; a piece can fill space only where L = 0. Output: the zero curves of L, and the known space-fillers on them.
usage: python dehn_map.py STEP"""
import sys, itertools, math, json
import numpy as np
from scipy.spatial import HalfspaceIntersection, ConvexHull
TH = math.acos(1 / math.sqrt(3))
def normals():
    N = [('c', np.array(v, float)) for v in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]]
    N += [('r', np.array(v, float) / math.sqrt(2)) for v in set(tuple(s*e for s, e in zip(sg, base)) for base in [(1,1,0),(1,0,1),(0,1,1)] for sg in itertools.product((1,-1), repeat=3))]
    N += [('o', np.array(v, float) / math.sqrt(3)) for v in itertools.product((1,-1), repeat=3)]
    return N
NS = normals()
def kcode(alpha):           # dihedral angle -> multiple of theta modulo rational multiples of pi
    table = [(90, 0), (45, 0), (135, 0), (60, 0), (120, 0), (180, 0),
             (math.degrees(TH), 1), (180 - math.degrees(TH), -1), (90 - math.degrees(TH), -1), (90 + math.degrees(TH), 1),
             (2 * (90 - math.degrees(TH)), -2), (180 - 2 * (90 - math.degrees(TH)), 2)]
    d = math.degrees(alpha)
    for a, k in table:
        if abs(d - a) < 1e-6: return k
    raise ValueError(f'unexpected dihedral angle {d}')
def piece(lam, mu):
    H = []
    for kind, n in NS:
        off = {'c': 1.0, 'r': lam / math.sqrt(2), 'o': mu / math.sqrt(3)}[kind]
        H.append(np.append(n, -off))
    hs = HalfspaceIntersection(np.array(H), np.zeros(3)); V = hs.intersections
    V = np.unique(np.round(V, 12), axis=0)
    act = [(kind, n, {'c': 1.0, 'r': lam / math.sqrt(2), 'o': mu / math.sqrt(3)}[kind]) for kind, n in NS]
    faces = []
    for kind, n, off in act:
        on = [i for i, v in enumerate(V) if abs(v @ n - off) < 1e-9]
        if len(on) >= 3: faces.append((kind, n, set(on)))
    L = 0.0; edges = 0
    for (k1, n1, s1), (k2, n2, s2) in itertools.combinations(faces, 2):
        sh = list(s1 & s2)
        if len(sh) < 2: continue
        pts = V[sh]; ln = max(np.linalg.norm(a - b) for a, b in itertools.combinations(pts, 2))
        alpha = math.pi - math.acos(max(-1, min(1, float(n1 @ n2))))
        L += ln * kcode(alpha); edges += 1
    return L, len(faces), edges, ConvexHull(V).volume
step = float(sys.argv[1]); out = []
lams = np.arange(1.0, 2.0 + 1e-9, step); mus = np.arange(1.0, 3.0 + 1e-9, step)
for lam in lams:
    for mu in mus:
        try: L, nf, ne, vol = piece(lam, mu)
        except Exception as e: continue
        out.append((round(lam, 6), round(mu, 6), L, nf, ne))
json.dump(out, open(f'dehn-map-{step}.json', 'w'))
grid = {(a, b): (L, nf) for a, b, L, nf, ne in out}
zero_region = sorted((a, b) for (a, b), (L, nf) in grid.items() if abs(L) < 1e-9)
curves = []
for (a, b), (L, nf) in grid.items():
    if abs(L) < 1e-9: continue
    for da, db in ((step, 0), (0, step)):
        n = (round(a + da, 6), round(b + db, 6))
        if n in grid and abs(grid[n][0]) > 1e-9 and L * grid[n][0] < 0: curves.append((round((a + n[0]) / 2, 4), round((b + n[1]) / 2, 4)))
print('grid points', len(out))
# the zero region: report its extent in mu for each lam
from collections import defaultdict
zr = defaultdict(list)
for a, b in zero_region: zr[a].append(b)
for a in sorted(zr)[::10]: print(f'  L = 0 throughout at lam {a:.2f}: mu from {min(zr[a]):.2f} to {max(zr[a]):.2f} ({len(zr[a])} points)')
cv = defaultdict(list)
for a, b in curves: cv[a].append(b)
print('genuine zero curves (sign changes, L nonzero on both sides):', len(curves), 'cells')
for a in sorted(cv)[::5]: print(f'  lam ~ {a:.3f}: mu ~ {sorted(set(cv[a]))[:6]}')
for lam, mu, label in ((2.0, 3.0, 'cube'), (1.0, 3.0, "Kepler's RD"), (2.0, 2.0, 'cuboctahedron'), (2.0, 1.0, 'octahedron'), (2.0, 1.5, 'truncated octahedron')):
    L, nf, ne, vol = piece(lam, mu); print(f'  {label:20s} lam {lam} mu {mu}: L = {L:+.6f}, faces {nf}')
chk = [abs(piece(2.0, 3.0)[0]) < 1e-9, abs(piece(1.0, 3.0)[0]) < 1e-9, abs(piece(2.0, 1.5)[0]) < 1e-9, abs(piece(2.0, 1.0)[0]) > 1, abs(piece(1.75, 2.25)[0]) < 1e-9]
print('FINAL ok' if all(chk) else 'FINAL FAIL: calibration (cube, RD, TO zero; octahedron nonzero; line point zero) ' + str(chk))
