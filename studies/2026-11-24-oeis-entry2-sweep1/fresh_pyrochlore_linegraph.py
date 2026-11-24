"""Sweep 1, fresh second method: closed walks per site of the pyrochlore network, built explicitly as the LINE GRAPH of diamond.
Diamond atoms: integer coordinates (units a/4); sublattice 0 = fcc points (all even, sum = 0 mod 4), sublattice 1 = those + (1,1,1).
Bonds of a sublattice-0 atom p: p + d, d in (1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1); of a sublattice-1 atom: p - d.
Pyrochlore site = a diamond bond {p, q}; two sites are joined iff their bonds share an atom (each site has 3 + 3 = 6 neighbours).
Closed walks counted by dynamic programming over every site within N/2 steps; exact integers. No formula is used."""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
D = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
def sub(p): return 0 if all(c % 2 == 0 for c in p) else 1
def atom_bonds(p):
    s = 1 if sub(p) == 0 else -1
    return [tuple(sorted((p, tuple(a + s * b for a, b in zip(p, d))))) for d in D]
def nbrs(e):
    p, q = e
    return [f for a in (p, q) for f in atom_bonds(a) if f != e]
o = tuple(sorted(((0, 0, 0), (1, 1, 1))))
assert len(nbrs(o)) == 6 and len(set(nbrs(o))) == 6
R = N // 2
dist = {o: 0}; front = [o]
for r in range(1, R + 1):
    nf = []
    for e in front:
        for f in nbrs(e):
            if f not in dist: dist[f] = r; nf.append(f)
    front = nf
NB = {e: [f for f in nbrs(e) if f in dist] for e in dist}
cur = {o: 1}; W = [1]
for n in range(1, N + 1):
    nxt = {}
    for e, c in cur.items():
        for f in NB[e]:
            if dist[f] <= N - n: nxt[f] = nxt.get(f, 0) + c
    cur = nxt; W.append(cur.get(o, 0))
print('sites within', R, 'steps:', len(dist))
print(','.join(map(str, W)))
