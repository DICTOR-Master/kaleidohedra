# Six equal circular rings that slot together (DICTO, 2026-10-14). The rings lie in the six planes square to the icosahedron's
# five-fold axes; every two cross at 63.43° along a line through the centre, so each ring has 10 crossings, 36° apart. At each
# crossing one ring is slotted from the outside and the other from the inside (a half-lap joint, as in an egg crate); the slots
# alternate out, in, out, ... round every ring, so all six rings are identical. Writes the 3D model (paper/figures/six-rings.json)
# and the check that the alternation is consistent. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
phi = (1 + 5 ** .5) / 2
ico = np.array([p for s in itertools.product((1, -1), repeat=2) for p in [(0, s[0], s[1] * phi), (s[0], s[1] * phi, 0), (s[1] * phi, 0, s[0])]], float)
N = [v / np.linalg.norm(v) for v in ico if v @ np.array([1e-3, 2e-3, 3e-3]) > 0]
FR = []
for n in N:
    a = np.cross(n, [0.3, 0.5, 0.8]); a /= np.linalg.norm(a); FR.append((a, np.cross(n, a)))
# crossings: for each ring, the 10 directions (unit vectors) where it meets the others, with the partner ring
cr = {i: [] for i in range(6)}
for i, j in itertools.combinations(range(6), 2):
    d = np.cross(N[i], N[j]); d /= np.linalg.norm(d)
    for s in (1, -1): cr[i].append((s * d, j)); cr[j].append((s * d, i))
ang = lambda i, d: math.atan2(d @ FR[i][1], d @ FR[i][0]) % (2 * math.pi)
for i in range(6): cr[i].sort(key=lambda x: ang(i, x[0]))
gaps = sorted({round(math.degrees((ang(i, cr[i][(k + 1) % 10][0]) - ang(i, cr[i][k][0])) % (2 * math.pi)), 4) for i in range(6) for k in range(10)})
# alternation: ring i slot at its k-th crossing is 'out' if (k + s_i) even; need partner opposite at the same point
key = lambda d: tuple(np.round(d, 6))
best = None
for S in itertools.product((0, 1), repeat=6):
    kind = {}
    for i in range(6):
        for k, (d, j) in enumerate(cr[i]): kind[(i, key(d))] = 'out' if (k + S[i]) % 2 == 0 else 'in'
    ok = all(kind[(i, key(d))] != kind[(j, key(d))] for i in range(6) for d, j in cr[i])
    if ok: best = S; break
print('crossings per ring 10, spacing (deg):', gaps, '| consistent alternation:', best)
assert best is not None
# 3D model: band between radii R_IN and R_OUT, split at R_MID; slot = remove the outer or inner half over the slot width
R_OUT, R_IN, T, SEG = 1.0, 0.86, 0.022, 720
R_MID = (R_OUT + R_IN) / 2
W = T / math.sin(math.acos(abs(N[0] @ N[1])))          # slot width along the ring for the other ring at 63.43°
verts, faces, tags = [], [], []
for i, n in enumerate(N):
    a, b = FR[i]
    slots = [(ang(i, d), 'out' if (k + best[i]) % 2 == 0 else 'in') for k, (d, j) in enumerate(cr[i])]
    def cut(t, half):
        for s, kd in slots:
            if kd == half and abs(((t - s + math.pi) % (2 * math.pi)) - math.pi) * R_MID < W / 2 * 1.05: return True
        return False
    for k in range(SEG):
        t0, t1 = 2 * math.pi * k / SEG, 2 * math.pi * (k + 1) / SEG; tm = (t0 + t1) / 2
        for half, (r0, r1) in (('out', (R_MID, R_OUT)), ('in', (R_IN, R_MID))):
            if cut(tm, half): continue
            for side in (1, -1):
                P = [ (a * math.cos(t) + b * math.sin(t)) * r + n * side * T / 2 for t, r in ((t0, r0), (t1, r0), (t1, r1), (t0, r1))]
                base = len(verts); verts += [list(p) for p in P]; faces.append([base, base + 1, base + 2, base + 3]); tags.append(f'w{i}')
json.dump({'six_rings': dict(v=verts, f=faces, t=tags)}, open(os.path.join(ROOT, 'paper', 'figures', 'six-rings.json'), 'w'))
json.dump(dict(rings=6, crossings_per_ring=10, spacing_deg=gaps, alternation=best, plane_angle_deg=math.degrees(math.acos(abs(N[0] @ N[1]))),
               slot_width_over_thickness=1 / math.sin(math.acos(abs(N[0] @ N[1])))), open(os.path.join(ROOT, 'six-rings.json'), 'w'), indent=1)
print('slot width =', round(1 / math.sin(math.acos(abs(N[0] @ N[1]))), 4), 'x thickness; planes meet at', round(math.degrees(math.acos(abs(N[0] @ N[1]))), 3))
