"""Step 8. Strengthens s5 for paper #89: the four 120-cell sections of s5 (Greater and Lesser Golden Cut Tetrahedra,
vertex-first; Greater and Lesser Golden Cut Dodecahedra, cell-first) are proved similar to the cut Platonic solids by an
explicit bijection of corners that scales every squared distance by one factor, checked exactly in Q(sqrt5)
(q5.Q5; floats only propose the bijection). s5 compared sorted distance lists, which is necessary but not by itself
sufficient for congruence. Same method as s7_icosaxes_exact.py.
usage (dicto-big-brother): ~/geom/bin/python s8_sections_bijection.py -> ../data/s8-sections-bijection.json
"""
import sys, os, json, itertools
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
SC = os.path.expanduser('~/kres-tmp/studies/2026-10-27-white-queen-polar/scripts')
sys.path.insert(0, SC); cwd = os.getcwd(); os.chdir(SC)
import atlas120 as A
os.chdir(cwd)
Q5, q5str = A.Q5, A.q5str
sys.setrecursionlimit(10000)
CHECKS = []
def check(name, ok):
    CHECKS.append({'check': name, 'pass': bool(ok)}); print(('PASS ' if ok else 'FAIL ') + name, flush=True)


def d2(p, q):
    s = Q5(0)
    for a, b in zip(p, q):
        s = s + (a - b) * (a - b)
    return s


def parse(s):            # '25/16 + 11/16√5' -> Q5
    s = s.replace(' ', '')
    if '√5' not in s: return Q5(Fr(s))
    body = s.replace('√5', '')
    i = max(body.rfind('+'), body.rfind('-', 1))
    return Q5(Fr(body[:i]), Fr(body[i:].lstrip('+')))


def section(lab, h):
    d = A.DIRS[lab][0]; H = [A.dot(p, d) for p in A.R]
    pts = [p for p, x in zip(A.R, H) if x == h]
    for a, b in A.E:
        ha, hb = H[a], H[b]
        if ((ha - h) * (hb - h)).sign() < 0:
            t = (h - ha) / (hb - ha); pts.append(tuple(x + t * (y - x) for x, y in zip(A.R[a], A.R[b])))
    return list(dict.fromkeys(pts))


G = Q5(Fr(1, 2), Fr(1, 2)); iG = Q5(Fr(-1, 2), Fr(1, 2))
TET = [tuple(Q5(c) for c in v) for v in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1))]
DOD = [tuple(Q5(c) for c in (a, b, c)) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
for a in (1, -1):
    for b in (1, -1):
        DOD += [(Q5(0), a * iG, b * G), (a * iG, b * G, Q5(0)), (b * G, Q5(0), a * iG)]


def cut(P, x):
    D = {(i, j): d2(P[i], P[j]) for i, j in itertools.combinations(range(len(P)), 2)}
    m = min(D.values(), key=float); E = [k for k, v in D.items() if v == m]
    return [tuple(p + x * (q - p) for p, q in zip(P[i], P[j])) for i, j in E] + \
           [tuple(q + x * (p - q) for p, q in zip(P[i], P[j])) for i, j in E]


def match(P, T):
    n = len(P); DP = [[float(d2(P[i], P[j])) for j in range(n)] for i in range(n)]
    DT = [[float(d2(T[i], T[j])) for j in range(n)] for i in range(n)]
    sP = max(max(r) for r in DP); sT = max(max(r) for r in DT); k = sT / sP
    f = [None] * n; used = [False] * n
    def go(i):
        if i == n: return True
        for c in range(n):
            if used[c]: continue
            if all(abs(DT[c][f[j]] - k * DP[i][j]) < 1e-9 * sT for j in range(i)):
                f[i] = c; used[c] = True
                if go(i + 1): return True
                used[c] = False
        return False
    return f if go(0) else None


xs = {'tetrahedron greater': Q5(Fr(3, 2), Fr(-1, 2)), 'tetrahedron lesser': Q5(Fr(1, 2), Fr(-1, 10)),
      'dodecahedron greater': Q5(Fr(1, 3)), 'dodecahedron lesser': Q5(Fr(7, 22), Fr(-1, 22))}
rows = []
for r in json.load(open(os.path.join(DATA, 's5-exact4d.json')))['sections']['120-cell']:
    key = ' '.join(r['solid'].split()[:2]); plat = TET if key.startswith('tetra') else DOD
    h = parse(r['atlas_height']); S = section(r['direction'], h); T = cut(plat, xs[key])
    f = match(S, T) if len(S) == len(T) else None
    ok = f is not None
    if ok:
        lam = d2(T[f[0]], T[f[1]]) / d2(S[0], S[1])
        ok = all(d2(T[f[i]], T[f[j]]) == lam * d2(S[i], S[j]) for i, j in itertools.combinations(range(len(S)), 2))
    check(f'120-cell {r["direction"]} at atlas height {r["atlas_height"]}: {len(S)} corners, bijection to the {key} golden cut '
          f'scaling all {len(S) * (len(S) - 1) // 2} squared distances by one factor (exact)', ok)
    rows.append({'direction': r['direction'], 'atlas_height': r['atlas_height'], 'solid': key + ' golden cut', 'corners': len(S),
                 'similar_exact': bool(ok), 'scale_squared': q5str(lam) if ok else None})
json.dump({'sections': rows, 'checks': CHECKS}, open(os.path.join(DATA, 's8-sections-bijection.json'), 'w'), indent=1)
print(f'{sum(c["pass"] for c in CHECKS)}/{len(CHECKS)} checks passed')
