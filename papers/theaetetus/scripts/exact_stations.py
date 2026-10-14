# Theaetetus stations, exact (2026-10-15): the pieces inside the dodecahedron are rebuilt exactly from exact corners (the icosidodecahedron's
# and the core's, snapped with small denominators; the core faces' centres computed exactly), not snapped; Dharma's outer pieces are
# snapped (they close exactly in exact.py). Then every volume exact, and the sum against the Hecatodihedron.
import json, itertools, numpy as np
from scipy.spatial import ConvexHull
exec(open('scripts/exact.py').read().split('out = []')[0].replace('qmax=48', 'qmax=12'))
J = json.load(open('data/cleo_heca.json'))
ex = lambda m: [[S(x) for x in v] for v in m['v']]
core = ex(J['core icosahedron'][0]); coref = np.array([[x.f() for x in v] for v in core])
IDf = ConvexHull(np.vstack([np.array(m['v']) for k in ('core icosahedron', 'Cleo-Ico', 'flat pentagonal pyramid', 'X', 'Y') for m in J[k]]))
IDv = [[S(x) for x in IDf.points[i]] for i in IDf.vertices]; IDvf = np.array([[x.f() for x in v] for v in IDv])
F = []
for e in ConvexHull(IDvf).equations:
    idx = tuple(sorted(i for i in range(len(IDv)) if abs(IDvf[i] @ e[:3] + e[3]) < 1e-9))
    if idx not in [f for f, _ in F]: F.append((idx, e[:3]))
tri = [(list(i), n) for i, n in F if len(i) == 3]; pent = [(list(i), n) for i, n in F if len(i) == 5]
CH = ConvexHull(coref)
cface = [list(s) for s in CH.simplices]
cen = lambda pts: [sum((p[i] for p in pts), Q(0)) / len(pts) for i in range(3)]
Dapex = {}   # dodecahedron corners: the tripyr apexes, snapped
for m in J['tripyr (to dodecahedron)']:
    V = ex(m); Vf = np.array(m['v']); c = Vf.mean(0); k = int(np.argmax(np.linalg.norm(Vf, axis=1))); Dapex[tuple(np.round(Vf[k] / np.linalg.norm(Vf[k]), 4))] = V[k]
pieces = {'core icosahedron': [core], 'Aetos (flat pentagonal pyramid)': [], 'Sphen (X)': [], 'Sphenion (Y)': [], 'Atraktos': []}
for idx, n in pent:
    apex = max(core, key=lambda v: np.array([x.f() for x in v]) @ n); pieces['Aetos (flat pentagonal pyramid)'].append([IDv[i] for i in idx] + [apex])
for idx, n in tri:
    T = [IDv[i] for i in idx]; Tf = IDvf[idx]
    s = max(cface, key=lambda s: coref[s].mean(0) @ n); B = [core[i] for i in s]; Bf = coref[s]; b0 = cen(B)
    dk = Dapex[tuple(np.round(n / np.linalg.norm(n), 4))]
    pieces['Atraktos'].append(T + [b0, dk])
    for i, j in itertools.combinations(range(3), 2):
        k = int(np.argmin(np.linalg.norm(Bf - (Tf[i] + Tf[j]) / 2, axis=1))); pieces['Sphen (X)'].append([T[i], T[j], B[k], b0])
    for k, l in itertools.combinations(range(3), 2):
        m = int(np.argmin(np.linalg.norm(Tf - (Bf[k] + Bf[l]) / 2, axis=1))); pieces['Sphenion (Y)'].append([B[k], B[l], T[m], b0])
for k in ('twisted pentagonal frustum', 't1', 'cap (to Hecatodihedron)'): pieces[k] = [ex(m) for m in J[k]]
out = ['== stations (exact)']; total = Q(0); allV = []
for k, L in pieces.items():
    vols = set()
    for V in L:
        Vf = np.array([[x.f() for x in v] for v in V]); v = volume(V, Vf); vols.add(v); total = total + v; allV += [tuple(x) for x in V]
    out.append(f'  {len(L):3d} {k}: volume {" | ".join(map(repr, vols))}  (= {next(iter(vols)).f():.9f})')
uniq = list({tuple((x.a, x.b) for x in v): v for v in allV}.values()); Hf = np.array([[x.f() for x in v] for v in uniq]); h = ConvexHull(Hf)
hv = volume([uniq[i] for i in h.vertices], Hf[h.vertices])
out.append(f'  total {total!r}; Hecatodihedron {hv!r}; difference {total - hv!r}')
idv = volume(IDv, IDvf); inner = sum((volume(V, np.array([[x.f() for x in v] for v in V])) for k in ('core icosahedron', 'Aetos (flat pentagonal pyramid)', 'Sphen (X)', 'Sphenion (Y)') for V in pieces[k]), Q(0))
cleo = sum((volume(V[:3] + [V[3]], np.array([[x.f() for x in v] for v in V[:3] + [V[3]]])) for V in pieces['Atraktos']), Q(0))
out.append(f'  inside the icosidodecahedron: core + Aetos + Sphen + Sphenion + the 20 Cleo-Icos = {inner + cleo!r}; icosidodecahedron {idv!r}')
print('\n'.join(out)); open('data/exact.txt', 'a').write('\n'.join(out) + '\n')
