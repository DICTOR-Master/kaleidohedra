"""DICTO 11-08 ('no, the DICTO Yantra I'm talking about': triangles from yellow, red and white parts not possible on other figures).
Test: do any two sides of different triangles lie on ONE straight line in a yantra? Then a longer side made of both exists and new
triangles can form. Lists near-collinear pairs (distance of the line pairs below 1e-6) per yantra, then recounts triangles with
collinear touching/overlapping sides merged."""
import itertools, math
from hidden_triangles import load, huet, segs, meet, cases
def line(s):
    (x1, y1), (x2, y2) = s; a, b = y2 - y1, x1 - x2; n = math.hypot(a, b); c = -(a * x1 + b * y1); return a / n, b / n, c / n
def same(s, t, tol=1e-6):
    A = line(s); B = line(t)
    if A[0] * B[0] + A[1] * B[1] < 0: B = tuple(-v for v in B)
    return max(abs(A[i] - B[i]) for i in range(3)) < tol
def merge(S):
    S = list(S); changed = True
    while changed:
        changed = False
        for i, j in itertools.combinations(range(len(S)), 2):
            if same(S[i], S[j]):
                pts = list(S[i]) + list(S[j]); d = (S[i][1][0] - S[i][0][0], S[i][1][1] - S[i][0][1])
                pr = lambda p: p[0] * d[0] + p[1] * d[1]
                lo1, hi1 = sorted(map(pr, S[i])); lo2, hi2 = sorted(map(pr, S[j]))
                if lo2 <= hi1 + 1e-9 and lo1 <= hi2 + 1e-9:   # touching or overlapping: one longer side
                    S[i] = (min(pts, key=pr), max(pts, key=pr)); del S[j]; changed = True; break
    return S
def tri_count(S):
    M = {}
    for i, j in itertools.combinations(range(len(S)), 2):
        p = meet(S[i], S[j])
        if p: M[i, j] = p
    c = 0
    for i, j, k in itertools.combinations(range(len(S)), 3):
        if (i, j) in M and (i, k) in M and (j, k) in M:
            p, q, r = M[i, j], M[i, k], M[j, k]
            if abs((q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])) > 1e-10: c += 1
    return c
names = {}
for name, (b, w, a) in cases:
    S = segs(b, w, a); lab = [f't{i} {s}' for i in range(1, 10) for s in ('base', 'left leg', 'right leg')]
    pairs = [(lab[i], lab[j]) for i, j in itertools.combinations(range(len(S)), 2) if same(S[i], S[j])]
    print(f'{name:28s} collinear pairs: {len(pairs)} {pairs[:6]}  triangles with joined sides: {tri_count(merge(S))}', flush=True)
print('FINAL ok' if names == {} else 'FINAL FAIL')
