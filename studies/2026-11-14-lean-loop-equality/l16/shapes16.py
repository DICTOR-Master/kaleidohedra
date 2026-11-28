# Normalised crossing sets {a,b,e,f} carrying a meeting pair of far arcs (2 + 4 edges), and their half-turn images,
# for the letters c[0..2] of the far half (bilayer 0 = the flipped one). Positions as in the Lean entry: atoms (j, p, u).
# Normalisation as nrm in Regroup.lean: shift = -(sum / 12) coordinatewise (Euclidean division), P + 3*shift.
# With Claude (Anthropic).
import sys, itertools
SV = [(1,1),(-2,1),(1,-2),(-1,-1),(2,-1),(-1,2)]
def site(p, s): return p[0] % 3 == s % 3 and p[1] % 3 == s % 3
def run(letters):
    L = lambda j: letters[j] if 0 <= j < len(letters) else None
    def nbrs(a):
        j, p, u = a; out = []
        out.append((j, p, 1 - u))
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
    def paths(start, n):
        out = []
        def rec(path):
            if len(path) - 1 == n: out.append(list(path)); return
            for b in nbrs(path[-1]):
                if far(b) and b not in path: path.append(b); rec(path); path.pop()
        rec([start]); return out
    endq = lambda a: a[0] == 0 and a[2] == 1
    s0 = letters[0]; b0 = (s0, s0)
    sets = set(); tuples = 0
    for i in (2, 4):
        for A in paths((0, b0, 1), i):
            if not endq(A[-1]): continue
            a = A[-1][1]
            pts = [q for q in itertools.product(range(b0[0]-14, b0[0]+15), range(b0[1]-14, b0[1]+15)) if site(q, s0)]
            for f in pts:
                for B in paths((0, f, 1), 6 - i):
                    if not endq(B[-1]): continue
                    e = B[-1][1]
                    P = {a, b0, e, f}
                    if len(P) < 4 or not set(A) & set(B): continue
                    tuples += 1; sets.add(frozenset(P))
    def nrm(P):
        sx = sum(p[0] for p in P); sy = sum(p[1] for p in P)
        dx, dy = -(sx // 12), -(sy // 12)
        return frozenset((p[0] + 3*dx, p[1] + 3*dy) for p in P)
    c = ((2*s0) % 3, (2*s0) % 3)
    Z = {nrm(P) for P in sets} | {nrm(frozenset((c[0]-p[0], c[1]-p[1]) for p in P)) for P in sets}
    return tuples, len(sets), Z
if __name__ == '__main__':
    tuples, nsets, Z = run([0, 1, 2])
    print('anchored meeting tuples', tuples, 'sets', nsets, 'normalised shapes (with half-turn images)', len(Z))
    with open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/shapes16.txt', 'w') as fh:
        for S in sorted(Z, key=sorted):
            q = sorted(S); fh.write(' '.join(f'{x},{y}' for x, y in q) + '\n')
    good = tuples > 0 and len(Z) > 0 and all(len(S) == 4 for S in Z)
    print('FINAL ok' if good else 'FINAL FAIL (no shapes or a shape without four points)')
