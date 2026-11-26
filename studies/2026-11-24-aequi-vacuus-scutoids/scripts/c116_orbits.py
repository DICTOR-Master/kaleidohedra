"""C116 (T_h) face orbits (26 Nov 2026). With Claude (Anthropic). Reads fullgen's planar code (data/c116/Full_codes_116_Th),
finds the faces, all map automorphisms (rotations and reflections: the image of one directed edge plus a choice of orientation fixes
an automorphism), and the face orbits with their face sizes. Pass: group order 24 (T_h). Compared with Minana #377's face orbits under
T_h: 12 heptagons, 12 squares, 12 hexagons, 24 hexagons (12 + 12 + 12 + 24)."""
import os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
raw = open(os.path.join(HERE, '../data/c116/Full_codes_116_Th'), 'rb').read()
assert raw.startswith(b'>>planar_code'), raw[:20]
i = raw.index(b'<<') + 2; data = raw[i:]
n = data[0]; adj = []; p = 1
for v in range(n):
    nb = []
    while data[p] != 0: nb.append(data[p] - 1); p += 1
    p += 1; adj.append(nb)
assert n == 116 and all(len(a) == 3 for a in adj)
def nxt(u, v, o):   # next edge round the face to the left (o=+1) or right (o=-1): at v, turn from u
    a = adj[v]; k = a.index(u); return v, a[(k + o) % 3]
def face(u, v, o=1):
    f = [u]; e = (u, v)
    while True:
        e = nxt(e[0], e[1], o)
        if e[0] == u and e[1] == v: break
        f.append(e[0])
    return f
faces, seen = [], set()
for u in range(n):
    for v in adj[u]:
        if (u, v) in seen: continue
        f = face(u, v)
        for a, b in zip(f, f[1:] + f[:1]): seen.add((a, b))
        faces.append(f)
print('faces', len(faces), Counter(len(f) for f in faces))
assert len(faces) == 60
def build_map(u0, v0, u1, v1, o):
    m = {u0: u1}; q = [(u0, v0, u1, v1)]; seen = set()
    while q:
        a, b, c, d = q.pop()
        if (a, b) in seen: continue
        seen.add((a, b))
        if m.setdefault(b, d) != d: return None
        kb, kd = adj[b].index(a), adj[d].index(c)
        for t in (1, 2):
            x, y = adj[b][(kb + t) % 3], adj[d][(kd + o * t) % 3]
            if m.setdefault(x, y) != y: return None
            q.append((b, x, d, y))
    return m if len(m) == n and len(set(m.values())) == n else None
u0, v0 = 0, adj[0][0]; G = []
for u1 in range(n):
    for v1 in adj[u1]:
        for o in (1, -1):
            m = build_map(u0, v0, u1, v1, o)
            if m and all(sorted(m[x] for x in adj[y]) == sorted(adj[m[y]]) for y in range(n)): G.append(m)
print('automorphisms', len(G))
fkey = {frozenset(f): k for k, f in enumerate(faces)}
orb, done = [], set()
for k, f in enumerate(faces):
    if k in done: continue
    o = {fkey[frozenset(m[x] for x in f)] for m in G}; done |= o; orb.append((len(o), len(f)))
orb.sort()
print('face orbits (orbit size, face size):', orb)
print('Minana #377 face orbits (orbit size, face size): [(12, 4), (12, 6), (12, 7), (24, 6)]')
match = sorted(s for s, _ in orb) == [12, 12, 12, 24]
print('orbit sizes match Minana (12+12+12+24):', match)
print('FINAL ok' if len(G) == 24 else 'FINAL FAIL (group order is not 24)')
