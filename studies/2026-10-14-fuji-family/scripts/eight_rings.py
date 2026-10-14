# Eight flat circular rings through one centre (DICTO, 2026-10-14: his DeltaZip build had eight wheels, all through the centre,
# all flat). Eight planes cannot share one symmetric pattern as six can, so we spread them as evenly as possible: the eight plane
# normals are placed to make the smallest angle between any two planes as large as possible (a line-packing problem). Reports that
# angle, each ring's 14 crossings (7 partners, two points each) and how evenly they fall round the ring, and whether alternating
# slots are consistent. Writes eight-rings.json and paper/figures/eight-rings.json (3D, slotted). DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
from scipy.optimize import minimize
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def unit(x): x = x.reshape(-1, 3); return x / np.linalg.norm(x, axis=1)[:, None]
def min_angle(x):
    n = unit(x); c = np.abs(n @ n.T); np.fill_diagonal(c, 0); return math.degrees(math.acos(c.max()))
def soft(x, p=40):
    n = unit(x); c = np.abs(n @ n.T); iu = np.triu_indices(8, 1); return np.log(np.sum(np.exp(p * c[iu]))) / p
rng = np.random.default_rng(2); best = None
for _ in range(300):
    x0 = rng.normal(size=24)
    for p in (20, 60, 200, 800):
        x0 = minimize(soft, x0, args=(p,), method='L-BFGS-B').x
    a = min_angle(x0)
    if best is None or a > best[0]: best = (a, unit(x0))
ang_min, N = best
pairs = [(i, j, math.degrees(math.acos(abs(N[i] @ N[j])))) for i, j in itertools.combinations(range(8), 2)]
FR = []
for n in N:
    a = np.cross(n, [0.3, 0.5, 0.8]); a /= np.linalg.norm(a); FR.append((a, np.cross(n, a)))
cr = {i: [] for i in range(8)}
for i, j in itertools.combinations(range(8), 2):
    d = np.cross(N[i], N[j]); d /= np.linalg.norm(d)
    for s in (1, -1): cr[i].append((s * d, j)); cr[j].append((s * d, i))
ang = lambda i, d: math.atan2(d @ FR[i][1], d @ FR[i][0]) % (2 * math.pi)
for i in range(8): cr[i].sort(key=lambda x: ang(i, x[0]))
spacing = [sorted(round(math.degrees((ang(i, cr[i][(k + 1) % 14][0]) - ang(i, cr[i][k][0])) % (2 * math.pi)), 1) for k in range(14)) for i in range(8)]
key = lambda d: tuple(np.round(d, 6)); alt = None
for S in itertools.product((0, 1), repeat=8):
    kind = {(i, key(d)): ('out' if (k + S[i]) % 2 == 0 else 'in') for i in range(8) for k, (d, j) in enumerate(cr[i])}
    if all(kind[(i, key(d))] != kind[(j, key(d))] for i in range(8) for d, j in cr[i]): alt = S; break
out = dict(smallest_plane_angle=round(ang_min, 4), plane_angles=sorted(round(p[2], 2) for p in pairs), crossing_spacing_per_ring=spacing,
           alternating_slots_consistent=alt is not None, normals=N.round(6).tolist())
json.dump(out, open(os.path.join(ROOT, 'eight-rings.json'), 'w'), indent=1)
print('smallest angle between planes', round(ang_min, 3)); print('plane angles', out['plane_angles'][:6], '...', out['plane_angles'][-6:])
for s in spacing: print('ring spacing', s)
print('alternating slots consistent:', alt)
# 3D slotted model (same construction as the six rings; slot widths from each crossing's own angle)
R_OUT, R_IN, T, SEG = 1.0, 0.86, 0.022, 720; R_MID = (R_OUT + R_IN) / 2
verts, faces, tags = [], [], []
for i, n in enumerate(N):
    a, b = FR[i]
    slots = []
    for k, (d, j) in enumerate(cr[i]):
        th = math.acos(abs(N[i] @ N[j])); kd = 'out' if alt is None or (k + alt[i]) % 2 == 0 else 'in'
        slots.append((ang(i, d), kd, T / math.sin(th)))
    for k in range(SEG):
        t0, t1 = 2 * math.pi * k / SEG, 2 * math.pi * (k + 1) / SEG; tm = (t0 + t1) / 2
        for half, (r0, r1) in (('out', (R_MID, R_OUT)), ('in', (R_IN, R_MID))):
            if any(kd == half and abs(((tm - s + math.pi) % (2 * math.pi)) - math.pi) * R_MID < w / 2 * 1.05 for s, kd, w in slots): continue
            for side in (1, -1):
                P = [(a * math.cos(t) + b * math.sin(t)) * r + n * side * T / 2 for t, r in ((t0, r0), (t1, r0), (t1, r1), (t0, r1))]
                base = len(verts); verts += [list(p) for p in P]; faces.append([base, base + 1, base + 2, base + 3]); tags.append(f'w{i % 6}' if i < 6 else ('w6' if i == 6 else 'w7'))
json.dump({'eight_rings': dict(v=verts, f=faces, t=tags)}, open(os.path.join(ROOT, 'paper', 'figures', 'eight-rings.json'), 'w'))
