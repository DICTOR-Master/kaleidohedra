# DICTO's ring ball (2026-10-14): "just two more circles than the cube octahedron", "eight compass directions". Model: the
# cuboctahedron's four great circles (planes square to the four three-fold axes) plus two upright circles in the planes x = 0 and
# y = 0. From above, the six rings' traces point to the eight compass directions. Reports each ring's crossings and the angles
# between rings, and renders flat bands. DICTO · dictospheres.com
import itertools, json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
N = [np.array(v, float) / np.linalg.norm(v) for v in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (-1, 1, 1), (1, 0, 0), (0, 1, 0)]]
names = ['cubo 1', 'cubo 2', 'cubo 3', 'cubo 4', 'upright N-S', 'upright E-W']
FR = []
for n in N:
    a = np.cross(n, [0.3, 0.5, 0.8]); a /= np.linalg.norm(a); FR.append((a, np.cross(n, a)))
ang = lambda i, d: math.atan2(d @ FR[i][1], d @ FR[i][0]) % (2 * math.pi)
lines = {}
for i, j in itertools.combinations(range(6), 2):
    d = np.cross(N[i], N[j]); d /= np.linalg.norm(d); lines.setdefault(tuple(np.round(np.abs(d) * np.sign(d[np.argmax(np.abs(d))]), 6)), []).append((i, j))
report = {}
for i in range(6):
    pts = sorted({round(math.degrees(ang(i, s * np.cross(N[i], N[j]) / np.linalg.norm(np.cross(N[i], N[j])))), 2) for j in range(6) if j != i for s in (1, -1)})
    gaps = sorted({round((pts[(k + 1) % len(pts)] - pts[k]) % 360, 2) for k in range(len(pts))})
    report[names[i]] = dict(crossing_points=len(pts), spacings_deg=gaps)
angles = sorted({round(math.degrees(math.acos(abs(N[i] @ N[j]))), 3) for i, j in itertools.combinations(range(6), 2)})
multi = {k: v for k, v in lines.items() if len(v) > 1}
out = dict(rings=names, ring_crossings=report, angles_between_rings_deg=angles, lines_where_three_or_more_rings_meet=len(multi),
           traces_from_above=sorted({round(math.degrees(math.atan2(*(np.cross(n, [0, 0, 1])[[1, 0]]))) % 180, 1) for n in N}))
json.dump(out, open(os.path.join(ROOT, 'cubo-plus-2.json'), 'w'), indent=1); print(json.dumps(out, indent=1))
R_OUT, R_IN, T, SEG = 1.0, 0.88, 0.02, 360
verts, faces, tags = [], [], []
for i, n in enumerate(N):
    a, b = FR[i]
    for k in range(SEG):
        t0, t1 = 2 * math.pi * k / SEG, 2 * math.pi * (k + 1) / SEG
        for side in (1, -1):
            P = [(a * math.cos(t) + b * math.sin(t)) * r + n * side * T / 2 for t, r in ((t0, R_IN), (t1, R_IN), (t1, R_OUT), (t0, R_OUT))]
            base = len(verts); verts += [list(p) for p in P]; faces.append([base, base + 1, base + 2, base + 3]); tags.append(f'w{i}')
json.dump({'cubo_plus2': dict(v=verts, f=faces, t=tags)}, open(os.path.join(ROOT, 'paper', 'figures', 'cubo-plus-2.json'), 'w'))
