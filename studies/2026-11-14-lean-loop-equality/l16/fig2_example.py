# #125 Figure 2 data: a crossing set S paired a b | e f with a meeting pair of far arcs (2 + 4 edges) at S and none at
# its half-turn gS, for diamond's far letters (0, 1). With Claude (Anthropic).
import itertools, json, sys
sys.path.insert(0, '.')
import importlib.util
spec = importlib.util.spec_from_file_location('s18', 'shapes18_size.py'); m = importlib.util.module_from_spec(spec)
SV = [(1,1),(-2,1),(1,-2),(-1,-1),(2,-1),(-1,2)]
letters = [0, 1, 2]
def site(p, s): return p[0] % 3 == s % 3 and p[1] % 3 == s % 3
def nbrs(a):
    j, p, u = a; out = [(j, p, 1 - u)] + [(j+1, (p[0]+d[0], p[1]+d[1]), 0) for d in SV] + [(j-1, (p[0]-d[0], p[1]-d[1]), 1) for d in SV]
    res = []
    for b in out:
        if not (0 <= b[0] < 3 and 0 <= a[0] < 3): continue
        if not (site(a[1], letters[a[0]]) and site(b[1], letters[b[0]])): continue
        jb, pb, ub = b
        if jb == j and pb == p and ub != u: res.append(b)
        elif jb == j+1 and u == 1 and ub == 0 and (pb[0]-p[0], pb[1]-p[1]) in SV: res.append(b)
        elif j == jb+1 and ub == 1 and u == 0 and (p[0]-pb[0], p[1]-pb[1]) in SV: res.append(b)
    return res
far = lambda a: a[0] > 0 or (a[0] == 0 and a[2] == 1)
def arcs(p, q, n):
    out = []
    def rec(path):
        if len(path) - 1 == n:
            if path[-1] == (0, q, 1): out.append(list(path))
            return
        for b in nbrs(path[-1]):
            if far(b) and b not in path: path.append(b); rec(path); path.pop()
    rec([(0, p, 1)]); return out
def meets(a, b, e, f):
    res = []
    for i in (2, 4):
        for A in arcs(a, b, i):
            for B in arcs(e, f, 6 - i):
                if set(A) & set(B): res.append((A, B))
    return res
pts = [(x, y) for x in range(-6, 7, 3) for y in range(-6, 7, 3)]
best = None
for a, b, e, f in itertools.permutations(pts, 4):
    if a > b or e > f or a > e: continue
    M = meets(a, b, e, f)
    if len(M) != 1: continue
    g = lambda p: (-p[0], -p[1])
    if meets(g(a), g(b), g(e), g(f)): continue
    best = dict(a=a, b=b, e=e, f=f, arcs=M[0]); break
json.dump(best, open('fig2_example.json', 'w'))
print(best)
print('FINAL ok' if best else 'FINAL FAIL (no example)')
