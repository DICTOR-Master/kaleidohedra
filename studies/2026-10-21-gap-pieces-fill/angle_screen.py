# DICTO 2026-10-21: "how many pieces such as CLEO are space filling as pairs etc, just in our tile kit" -> the gap pieces (AXE, CLEO,
# FUJI; Bodhi B1-B5). Step 1, a necessary test: in a filling of space every edge of every piece is surrounded by pieces whose angles
# at that line add up to 360 deg (or 180 deg where the edge runs across another piece's face). So for each set of pieces (alone, pairs,
# threes) every dihedral angle of every piece must complete to 360 or 180 with angles of pieces in the set. Fail = cannot fill space.
import os, json, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(HERE, '..')
def dihedrals(V, F):
    V = np.array(V, float); c = V.mean(0); out = {}
    N = []
    for f in F:
        n = np.cross(V[f[1]] - V[f[0]], V[f[2]] - V[f[0]]); n /= np.linalg.norm(n); N.append(n if n @ (V[f[0]] - c) > 0 else -n)
    for i, j in itertools.combinations(range(len(F)), 2):
        sh = set(F[i]) & set(F[j])
        if len(sh) == 2:
            a, b = sh; L = round(float(np.linalg.norm(V[a] - V[b])), 4); ang = round(float(180 - np.degrees(np.arccos(np.clip(N[i] @ N[j], -1, 1)))), 4)
            out.setdefault(ang, set()).add(L)
    return out
P = {}
pj = json.load(open(os.path.join(S, '2026-10-14-axe-cleo-fuji/nets/pieces.json')))
for k in ('AXE', 'CLEO', 'FUJI'): P[k] = dihedrals(pj[k]['vertices'], pj[k]['faces'])
for b in range(1, 6):
    d = json.load(open(os.path.join(S, f'2026-10-12-bodhi-pieces/data/bodhi-B{b}-unit.json'))); P[f'B{b}'] = dihedrals(d['vertices'], d['faces'])
for k, v in P.items(): print(k, {a: sorted(l) for a, l in sorted(v.items())})
def completes(theta, angles, tol=1e-3, kmax=14):
    # can theta + nonneg combination of angles reach 360 or 180?
    reach = {0.0}
    for _ in range(kmax):
        reach |= {round(r + a, 4) for r in reach for a in angles if r + a <= 360 + tol}
    return any(abs(theta + r - T) < tol for r in reach for T in (180, 360))
names = list(P); res = {}
for n in (1, 2, 3):
    for S_ in itertools.combinations(names, n):
        angs = sorted({a for k in S_ for a in P[k]})
        bad = [(k, a) for k in S_ for a in P[k] if not completes(a, angs)]
        res[' + '.join(S_)] = bad
        if not bad or n == 1: print(f"{' + '.join(S_):22s}", 'PASSES' if not bad else f'fails at {bad[:3]}')
json.dump({k: [list(x) for x in v] for k, v in res.items()}, open(os.path.join(HERE, 'angle-screen.json'), 'w'), indent=0)
