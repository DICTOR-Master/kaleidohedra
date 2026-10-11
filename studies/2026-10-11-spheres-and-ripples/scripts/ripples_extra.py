# Where are the strong ripple points (>= 48 faces) that are not gap-piece corners?
import json, numpy as np, collections
PHI = (1 + 5 ** .5) / 2
P = json.load(open('lotus-pieces.json')); R = json.load(open('ripple-points.json'))
icos = [p for p in P if p['role'] == 'ico']; gaps = [p for p in P if p['role'] != 'ico']
V0 = np.array(icos[0]['vertices']); c0 = V0.mean(0); f0 = icos[0]['faces']
N0 = []
for f in f0:
    a, b, d = V0[f[0]], V0[f[1]], V0[f[2]]; n = np.cross(b - a, d - a); n /= np.linalg.norm(n); N0.append(n if n @ (a - c0) > 0 else -n)
N0 = np.array(N0); rin = abs(N0[0] @ (V0[f0[0][0]] - c0)); cen = np.array([np.mean(p['vertices'], 0) for p in icos])
X = np.array(R['points']); C = {tuple(c) for c in R['corners']}
mult = np.zeros(len(X), int)
for c in cen:
    vals = (X - c) @ N0.T
    for k in (-3, -2, 0, 1): mult += np.sum(np.abs(vals - rin * PHI ** k) < 1e-6, axis=1)
strong = [(tuple(x), m) for x, m in zip(np.round(X, 6), mult) if m >= 48 and tuple(x) not in C]
def planes(p):
    V = np.array(p['vertices']); c = V.mean(0); out = []
    for f in p['faces']:
        a, b, d = V[f[0]], V[f[1]], V[f[2]]; n = np.cross(b - a, d - a); n /= np.linalg.norm(n)
        if n @ (a - c) < 0: n = -n
        out.append((n, n @ a))
    return V, out
SV = {tuple(np.round(v, 6)) for p in icos for v in p['vertices']}
def where(x):
    x = np.array(x)
    if tuple(np.round(x, 6)) in SV: return 'icosahedron corner'
    for p in icos:
        V, Pl = planes(p); s = [d - n @ x for n, d in Pl]
        if min(s) > -1e-6 and sum(abs(t) < 1e-6 for t in s) >= 1: return 'on an icosahedron ' + ('edge' if sum(abs(t) < 1e-6 for t in s) >= 2 else 'face')
    for p in gaps:
        V, Pl = planes(p); s = [d - n @ x for n, d in Pl]
        if min(s) > -1e-6:
            z = sum(abs(t) < 1e-6 for t in s)
            return f"{'inside' if z == 0 else 'on a face of' if z == 1 else 'on an edge of'} {p['role']}"
    return 'elsewhere'
cnt = collections.Counter((where(x), m) for x, m in strong)
for (w, m), n in sorted(cnt.items(), key=lambda t: (-t[1])): print(f'{n:4d}  {w:28s} ({m} ripple faces)')
# barycentric position of the interior strong points in their CLEO / AXE
PH = PHI
def gf(x):
    for den in (1, 2, 4, 5, 8, 10, 20):
        for b in range(-20, 21):
            a = x * den - b * 5 ** .5
            if abs(a - round(a)) < 1e-6: return f'({round(a)}{b:+d}√5)/{den}' if b else f'{round(a)}/{den}'
    return f'{x:.6f}'
per = collections.defaultdict(list)
for x, m in strong:
    x = np.array(x)
    for gi, p in enumerate(gaps):
        if p['role'] not in ('axe', 'cleo'): continue
        V, Pl = planes(p)
        if min(d - n @ x for n, d in Pl) > 1e-6: per[(p['role'], gi)].append(x)
by = collections.Counter((r, len(v)) for (r, g), v in per.items())
print('interior strong points per piece:', dict(by))
for role in ('cleo', 'axe'):
    k = next((key for key in per if key[0] == role), None)
    if not k: continue
    V = np.array(gaps[k[1]]['vertices'])
    for x in per[k][:2]:
        M = np.vstack([V.T, np.ones(4)]); lam = np.linalg.solve(M, np.r_[x, 1])
        print(role, 'barycentric:', [gf(l) for l in lam], ' (edge lengths of piece:', sorted(round(float(np.linalg.norm(V[i] - V[j])), 4) for i in range(4) for j in range(i + 1, 4)), ')')
