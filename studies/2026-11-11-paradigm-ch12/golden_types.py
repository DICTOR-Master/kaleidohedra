"""Chapter 12: the golden slice of the 4D permutohedron honeycomb, exactly. Every cell is a translate of the permutohedron P of
-2..2 (Voronoi cell of A4*), cut by u.x = c with u = (1, phi, phi^2, phi^3, phi^4). (i) Corner heights u.sigma computed EXACTLY in
Z[phi] (pairs a + b phi; phi^i = F_i phi + F_(i-1)); ties counted. (ii) For each open interval between consecutive distinct heights,
the faces of P that straddle the level (ordered set partitions of the 5 positions whose corners lie on both sides); the section's
combinatorial type = the containment graph of straddling edges, 2-faces and 3-faces (vertices, edges, facets of the section);
iso classes by networkx graph isomorphism. (iii) Controls: a rational direction (1,-1,0,0,0) and a generic one."""
import itertools, sys
import networkx as nx
from fractions import Fraction
def fib(k):
    a, b = 0, 1
    for _ in range(k): a, b = b, a + b
    return a
PHI = ((0, 1), (1, 0))   # unused marker
def zphi_pow(i): return (fib(i - 1) if i >= 1 else 1, fib(i)) if i >= 1 else (1, 0)   # phi^i = F(i-1) + F(i) phi
phi = (1 + 5 ** 0.5) / 2
def val(p): return p[0] + p[1] * phi
VALS = [-2, -1, 0, 1, 2]; n = 5
def faces():
    out = []
    def osp(items):
        if not items: yield []; return
        for k in range(1, len(items) + 1):
            for first in itertools.combinations(items, k):
                rest = [x for x in items if x not in first]
                for tail in osp(rest): yield [first] + tail
    for part in osp(list(range(n))):
        # vertices: positions in block j get the next |B_j| values, in any order within the block
        verts = []
        def assign(j, start, cur):
            if j == len(part): verts.append(tuple(cur)); return
            B = part[j]
            for perm in itertools.permutations(VALS[start:start + len(B)]):
                c = list(cur)
                for p, v in zip(B, perm): c[p] = v
                assign(j + 1, start + len(B), c)
        assign(0, 0, [0] * n); out.append((n - len(part), frozenset(verts)))
    return out
F = faces(); V = sorted({v for d, vs in F if d == 0 for v in vs})
assert len(V) == 120 and sum(1 for d, _ in F if d == 1) == 240 and sum(1 for d, _ in F if d == 2) == 150 and sum(1 for d, _ in F if d == 3) == 30
def run(height, label):
    H = {v: height(v) for v in V}                       # exact keys
    levels = sorted(set(H.values()), key=lambda h: (h[0] + h[1] * phi) if isinstance(h, tuple) else h)
    fl = lambda h: (h[0] + h[1] * phi) if isinstance(h, tuple) else h
    types = []; reps = []
    for a, b in zip(levels, levels[1:]):
        c = (fl(a) + fl(b)) / 2
        S = [(d, vs) for d, vs in F if 1 <= d <= 3 and min(fl(H[v]) for v in vs) < c < max(fl(H[v]) for v in vs)]
        G = nx.Graph()
        for i, (d, vs) in enumerate(S): G.add_node(i, d=d)
        for i, (d1, v1) in enumerate(S):
            for j, (d2, v2) in enumerate(S):
                if d2 == d1 + 1 and v1 <= v2: G.add_edge(i, j)
        for k, R in enumerate(reps):
            if nx.is_isomorphic(G, R, node_match=lambda x, y: x['d'] == y['d']): types.append(k); break
        else: reps.append(G); types.append(len(reps) - 1)
    print(f'{label}: distinct corner heights {len(levels)} of 120 (ties {120 - len(levels)}), open intervals {len(levels) - 1}, combinatorial types {len(reps)}', flush=True)
    return len(levels), len(reps)
u_g = [zphi_pow(i) for i in range(5)]
gold = lambda v: (sum(c * p[0] for c, p in zip(v, u_g)), sum(c * p[1] for c, p in zip(v, u_g)))
r1 = run(lambda v: v[0] - v[1], 'rational (1,-1,0,0,0)')
r2 = run(lambda v: sum(c * w for c, w in zip(v, (0.1123, 0.2711, 0.5807, 0.7319, 1.0))), 'generic')
r3 = run(gold, 'GOLDEN (1, phi, phi^2, phi^3, phi^4)')
print('FINAL ok' if r2[0] == 120 and r3[1] >= 1 else 'FINAL FAIL')
