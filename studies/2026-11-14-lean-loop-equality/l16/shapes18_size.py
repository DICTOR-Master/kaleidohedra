# l = 18 sizing (28 Nov 2026, with Claude (Anthropic)): anchored meeting pairs of far arcs with s edges in all
# (s = 6 and 8), normalised shapes with half-turn images, for the letters c[0..3] of the far half.
import itertools, time, sys
sys.path.insert(0, '/tmp')
SV = [(1,1),(-2,1),(1,-2),(-1,-1),(2,-1),(-1,2)]
def site(p, s): return p[0] % 3 == s % 3 and p[1] % 3 == s % 3
def run(letters, s):
    L = lambda j: letters[j] if 0 <= j < len(letters) else None
    def nbrs(a):
        j, p, u = a; out = [(j, p, 1 - u)]
        for d in SV:
            out.append((j + 1, (p[0] + d[0], p[1] + d[1]), 0)); out.append((j - 1, (p[0] - d[0], p[1] - d[1]), 1))
        res = []
        for b in out:
            if L(a[0]) is None or L(b[0]) is None: continue
            if not (site(a[1], L(a[0])) and site(b[1], L(b[0]))): continue
            jb, pb, ub = b
            if jb == j and pb == p and ub != u: res.append(b)
            elif jb == j + 1 and u == 1 and ub == 0 and (pb[0]-p[0], pb[1]-p[1]) in SV: res.append(b)
            elif j == jb + 1 and ub == 1 and u == 0 and (p[0]-pb[0], p[1]-pb[1]) in SV: res.append(b)
        return res
    far = lambda a: a[0] > 0 or (a[0] == 0 and a[2] == 1)
    endq = lambda a: a[0] == 0 and a[2] == 1
    cache = {}
    def arcs(start, n):
        key = (start, n)
        if key in cache: return cache[key]
        out = []
        def rec(path):
            if len(path) - 1 == n:
                if endq(path[-1]): out.append(tuple(path))
                return
            for b in nbrs(path[-1]):
                if far(b) and b not in path: path.append(b); rec(path); path.pop()
        rec([start]); cache[key] = out; return out
    s0 = letters[0]; b0 = (s0, s0); R = 2 * s
    tuples = 0; sets = set()
    for i in range(2, s - 1, 2):
        for A in arcs((0, b0, 1), i):
            a = A[-1][1]; Aset = set(A)
            for f in itertools.product(range(b0[0]-R, b0[0]+R+1), range(b0[1]-R, b0[1]+R+1)):
                if not site(f, s0): continue
                for B in arcs((0, f, 1), s - i):
                    e = B[-1][1]
                    P = {a, b0, e, f}
                    if len(P) < 4 or not Aset & set(B): continue
                    tuples += 1; sets.add(frozenset(P))
    def nrm(P):
        sx = sum(p[0] for p in P); sy = sum(p[1] for p in P)
        dx, dy = -(sx // 12), -(sy // 12)
        return frozenset((p[0] + 3*dx, p[1] + 3*dy) for p in P)
    c = ((2*s0) % 3, (2*s0) % 3)
    Z = {nrm(P) for P in sets} | {nrm(frozenset((c[0]-p[0], c[1]-p[1]) for p in P)) for P in sets}
    return tuples, len(sets), len(Z), sum(len(v) for v in cache.values())
res = {}
for s in (6, 8):
    t = time.time()
    res[s] = run([0, 1, 2, 0], s)
    print('s', s, 'letters 0,1,2,0 (tuples, sets, shapes, arcs cached):', res[s], '%.1fs' % (time.time() - t), flush=True)
# control: s = 6 must reproduce the l = 16 numbers (384 anchored meeting pairs, 17 shapes)
print('FINAL ok' if res[6][0] == 384 and res[6][2] == 17 else 'FINAL FAIL (s = 6 control does not reproduce 384 / 17)')
