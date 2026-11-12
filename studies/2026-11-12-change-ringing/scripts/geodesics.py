"""Conjecture 13.1 (Permutohedron Paradigm, Chapter 13): the two halves of the plain hunt are the only shortest ways from rounds to
backrounds in the change graph R_n.  Exact breadth-first search (Python integers), n = 3..NMAX.
DICTO · dictospheres.com - study 2026-11-12-change-ringing, 13 Nov 2026.  Stdlib only.

R_n: rows = permutations of the bells 1..n; a change swaps the bells in a nonempty set of disjoint pairs of neighbouring places.
P_n: one swap per change only (the edges of the permutohedron).
For each n: the number of changes per row (must be F(n+1) - 1), the distance rounds -> backrounds, the number of shortest paths, the
eccentricity of rounds, and (R_n) every shortest path listed and compared with the two halves of the plain hunt (even n: x, 1n, x, ...
or 1n, x, 1n, ...; odd n: n, 1, n, ... or 1, n, 1, ...).  Controls: n = 3..6 as in ring.log (distance n, 2 ways; P_n: C(n,2) steps
with Stanley's 2, 16, 768, 292864 ways), and P_7, P_8 against Stanley's formula C(n,2)! / prod_k (2k-1)^(n-k) (OEIS A005118).
Also checked on every shortest path found: the counting identity of the proof, sum_b r_b + 4u = n (r_b = rests of bell b, u = swaps
that undo an earlier crossing).
Usage: python3 geodesics.py NMAX [P_max]   Prints PROGRESS k/K lines and 'GEO ok' / 'GEO FAIL'."""
import sys, time, itertools
from math import comb, factorial
NMAX = int(sys.argv[1]); PMAX = int(sys.argv[2]) if len(sys.argv) > 2 else NMAX
T0 = time.time(); OK = True
def chk(name, cond, detail=''):
    global OK
    OK = OK and bool(cond); print(('ok   ' if cond else 'FAIL ') + name + (f'  [{detail}]' if detail != '' else ''), flush=True)
SYM = '1234567890ET'
def changes(n, single):
    out = []
    for k in range(1, n):
        for c in itertools.combinations(range(n - 1), k):
            if all(c[j + 1] - c[j] >= 2 for j in range(len(c) - 1)) and (k == 1 or not single): out.append(c)
    return out
def apply(row, ch):
    r = list(row)
    for i in ch: r[i], r[i + 1] = r[i + 1], r[i]
    return tuple(r)
def fib(k):
    a, b = 0, 1
    for _ in range(k): a, b = b, a + b
    return a
def bfs(n, single):
    chs = changes(n, single); start = tuple(range(1, n + 1))
    dist = {start: 0}; ways = {start: 1}; order = [start]
    for v in order:
        dv = dist[v]
        for c in chs:
            w = apply(v, c)
            if w not in dist: dist[w] = dv + 1; ways[w] = 0; order.append(w)
            if dist[w] == dv + 1: ways[w] += ways[v]
    return chs, dist, ways
def all_geodesics(n, chs, dist, target):
    paths = []
    def back(v, tail):
        if dist[v] == 0: paths.append([v] + tail); return
        for c in chs:
            w = apply(v, c)   # changes are involutions: w is a neighbour of v
            if dist.get(w) == dist[v] - 1: back(w, [v] + tail)
    back(target, []); return paths
def plain_hunt_halves(n):
    x = tuple(range(0, n - 1, 2)); y = tuple(range(1, n - 1, 2))   # swap starts: x = places 12, 34, ...; y = 23, 45, ...
    out = []
    for first in (x, y):
        row = tuple(range(1, n + 1)); rows = [row]; c = first
        for _ in range(n): row = apply(row, c); rows.append(row); c = y if c == x else x
        out.append(rows)
    return out
def pn(ch, n):
    fixed = [p for p in range(n) if not any(p in (i, i + 1) for i in ch)]
    return 'x' if not fixed else ''.join(SYM[p] for p in fixed)
def identity_check(n, path):
    """sum_b r_b + 4u = n(L - n + 1) for a path of L changes"""
    L = len(path) - 1; rests = 0; u = 0
    for a, b in zip(path, path[1:]):
        rests += sum(1 for p in range(n) if a[p] == b[p])
        for p in range(n - 1):
            if a[p] == b[p + 1] and a[p + 1] == b[p] and a[p] > a[p + 1]: u += 1   # the swap un-crosses a pair
    return rests + 4 * u == n * (L - n + 1), rests, u
STANLEY = {3: 2, 4: 16, 5: 768, 6: 292864}
def stanley(n):   # reduced words of the longest permutation: C(n,2)! / prod_{k=1}^{n-1} (2k-1)^(n-k)
    den = 1
    for k in range(1, n): den *= (2 * k - 1) ** (n - k)
    return factorial(comb(n, 2)) // den
K = (NMAX - 2) + (PMAX - 2); step = 0; RES = {}
for n in range(3, NMAX + 1):
    chs, dist, ways = bfs(n, False)
    back = tuple(range(n, 0, -1))
    chk(f'R{n}: {len(dist)} = {n}! rows reached; {len(chs)} changes per row = F({n + 1}) - 1 = {fib(n + 1) - 1}', len(dist) == factorial(n) and len(chs) == fib(n + 1) - 1)
    ecc = max(dist.values()); far = [r for r in dist if dist[r] == ecc]
    paths = all_geodesics(n, chs, dist, back)
    ph = plain_hunt_halves(n)
    words = sorted('.'.join(pn(tuple(i for i in range(n - 1) if a[i] == b[i + 1] and a[i + 1] == b[i]), n) for a, b in zip(p, p[1:])) for p in paths)
    print(f'  R{n}: distance rounds -> backrounds {dist[back]}, shortest ways {ways[back]}, eccentricity of rounds {ecc} (farthest rows {len(far)}), ways: {words}', flush=True)
    chk(f'R{n}: rounds -> backrounds is exactly n = {n} changes, and no row is farther from rounds (eccentricity n; {len(far)} rows at distance n)', dist[back] == n and ecc == n)
    chk(f'R{n} (Conjecture 13.1): exactly two shortest ways, and they are the two halves of the plain hunt', ways[back] == 2 and len(paths) == 2 and sorted(paths) == sorted(ph))
    chk(f'R{n}: proof identity sum r_b + 4u = n on both ways (every bell rests once, u = 0)', all(identity_check(n, p)[0] and identity_check(n, p)[1:] == (n, 0) for p in paths))
    RES[f'R{n}'] = dict(distance=dist[back], ways=ways[back], eccentricity=ecc, rows_at_distance_n=len(far), words=words)
    step += 1; print(f'PROGRESS {step}/{K} R{n} done  ({time.time() - T0:.1f} s)', flush=True)
for n in range(3, PMAX + 1):
    chs, dist, ways = bfs(n, True)
    back = tuple(range(n, 0, -1)); want = stanley(n)
    print(f'  P{n}: distance {dist[back]}, shortest paths {ways[back]}', flush=True)
    chk(f'control P{n}: C({n},2) = {comb(n, 2)} steps, {want} shortest paths (Stanley 1984' + (f'; ring.log {STANLEY[n]}' if n in STANLEY else '') + ')',
        dist[back] == comb(n, 2) and ways[back] == want and (n not in STANLEY or STANLEY[n] == want))
    RES[f'P{n}'] = dict(distance=dist[back], ways=ways[back])
    step += 1; print(f'PROGRESS {step}/{K} P{n} done  ({time.time() - T0:.1f} s)', flush=True)
# negative control: a longer way (plain hunt on 5 with a detour: one swap and its undoing inserted at the start, 7 changes) satisfies
# the identity with L = 7 but not the shortest-way pattern (every bell rests once, u = 0)
ph = plain_hunt_halves(5)[0]; det = [ph[0], apply(ph[0], (0,)), ph[0]] + ph[1:]
okid, r_, u_ = identity_check(5, det)
chk(f'negative: a 7-change way rounds -> backrounds (detour) obeys the identity (rests {r_}, u {u_}) but not rests = n, u = 0', okid and det[-1] == (5, 4, 3, 2, 1) and (r_, u_) != (5, 0))
print('result', RES, flush=True)
print(f'total {time.time() - T0:.1f} s', flush=True)
print('GEO ok' if OK else 'GEO FAIL', flush=True); sys.exit(0 if OK else 1)
