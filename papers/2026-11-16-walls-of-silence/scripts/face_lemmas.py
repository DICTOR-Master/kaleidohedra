#!/usr/bin/env python3
"""Walls of Silence: checks for Lemma 3 (the face lemmas) and for the 24-cell reading of the cross walls.
Floating point (tolerance 1e-9 on unit vectors); the 600-cell as the 120 unit icosians (2I), W(H4) as the 14400 maps
x -> a x b and x -> a conj(x) b (a, b in 2I). Prints CHECK lines and FINAL ok/FAIL."""
import itertools, numpy as np
phi = (1 + 5 ** .5) / 2
ok = True
def C(c, m):
    global ok; ok &= bool(c); print(('CHECK ok   ' if c else 'CHECK FAIL ') + m)
def qmul(p, q):
    a1, b1, c1, d1 = p; a2, b2, c2, d2 = q
    return np.array([a1*a2-b1*b2-c1*c2-d1*d2, a1*b2+b1*a2+c1*d2-d1*c2, a1*c2-b1*d2+c1*a2+d1*b2, a1*d2+b1*c2-c1*b2+d1*a2])
def conj(q): return q * np.array([1, -1, -1, -1])
V = []
for i in range(4):
    for s in (1, -1):
        v = np.zeros(4); v[i] = s; V.append(v)
for s in itertools.product((1, -1), repeat=4): V.append(np.array(s) / 2)
ev = [p for p in itertools.permutations(range(4)) if sum(1 for i in range(4) for j in range(i+1, 4) if p[i] > p[j]) % 2 == 0]
for s in itertools.product((1, -1), repeat=3):
    base = [0, s[0]*1, s[1]/phi, s[2]*phi]
    for p in ev:
        V.append(np.array([base[p[k]] for k in range(4)]) / 2)
V = np.array(V); C(len(V) == 120 and np.allclose(np.linalg.norm(V, axis=1), 1), '120 unit icosians')
key = lambda x: tuple(np.round(x, 7))
idx = {key(v): i for i, v in enumerate(V)}
G = V @ V.T
E = [(i, j) for i in range(120) for j in range(i+1, 120) if abs(G[i, j] - phi/2) < 1e-9]
C(len(E) == 720, '720 edges (inner product phi/2)')
def normal(pts):
    _, _, vt = np.linalg.svd(np.array(pts)); n = vt[-1]; return n / np.linalg.norm(n)
def canon(n):
    n = np.asarray(n, float); n = n / np.linalg.norm(n)
    k = np.argmax(np.abs(n) > 1e-9); return key(n if n[k] > 0 else -n)
# walls: mirrors = corners; cells = 4-cliques of edges; cross walls = cell centres
adj = {i: set() for i in range(120)}
for i, j in E: adj[i].add(j); adj[j].add(i)
tri = [t for t in itertools.combinations(range(120), 3) if t[1] in adj[t[0]] and t[2] in adj[t[0]] and t[2] in adj[t[1]]]
cells = [c for c in itertools.combinations(range(120), 4) if all(b in adj[a] for a, b in itertools.combinations(c, 2))]
C(len(tri) == 1200 and len(cells) == 600, '1200 triangles, 600 cells')
mir = {canon(v) for v in V}; cro = {canon(V[list(c)].sum(0)) for c in cells}
C(len(mir) == 60 and len(cro) == 300 and not (mir & cro), '60 mirror walls, 300 cross walls, disjoint')
def classify(faces, name):
    cnt = {}
    for f in faces:
        n = canon(normal(V[list(f)]))
        cnt[n] = cnt.get(n, 0) + 1
    m = sum(1 for n in cnt if n in mir); c = sum(1 for n in cnt if n in cro); o = len(cnt) - m - c
    per = sorted(set(cnt.values()))
    print(f'  {name}: {len(faces)} faces on {len(cnt)} plates: {m} mirror, {c} cross, {o} none; faces per plate {per}')
    return len(faces), m, c, o, per
# radius triangles: pairwise inner product 1/2
rt = [t for t in itertools.combinations(range(120), 3) if all(abs(G[a, b] - .5) < 1e-9 for a, b in itertools.combinations(t, 2))]
# golden rectangles edge x radius: u, v edge; w, x with u.x and v.w ... found as 4-sets with distances {e, R, diagonal}
e2 = 2 - phi  # squared edge length at radius 1: 2 - 2*phi/2
rect = []
for i, j in E:
    for k in range(120):
        if abs(G[j, k] - .5) < 1e-9 and abs(G[i, k] - .5) > 1e-9:
            l = V[i] + V[k] - V[j]
            if key(l) in idx:
                L = idx[key(l)]
                if abs(G[i, L] - .5) < 1e-9 and abs(G[k, L] - phi/2) < 1e-9 and abs(np.dot(V[j]-V[i], V[k]-V[j])) < 1e-9:
                    rect.append(tuple(sorted((i, j, k, L))))
rect = sorted(set(rect))
r1 = classify(tri, 'edge triangles'); r2 = classify(rect, 'golden rectangles (edge x radius)'); r3 = classify(rt, 'radius triangles')
C(r1 == (1200, 60, 0, 0, [20]), 'edge triangles: 20 on each of the 60 mirrors')
C(r2 == (1800, 60, 0, 0, [30]), 'golden rectangles: 1800, 30 on each of the 60 mirrors')
C(r3 == (2400, 0, 300, 0, [8]), 'radius triangles: 2400, 8 on each of the 300 cross walls')
# W(H4) transitivity on each class
maps = []
for a in V:
    for b in V:
        maps.append((a, b, False)); maps.append((a, b, True))
def img(f, m):
    a, b, c = m
    return tuple(sorted(idx[key(qmul(qmul(a, conj(V[i]) if c else V[i]), b))] for i in f))
def orbit_count(faces):
    fs = set(faces); seen = set(); orbits = 0
    for f in faces:
        if f in seen: continue
        orbits += 1
        for m in maps: seen.add(img(f, m))
    return orbits
C(len({img((0,), m) for m in maps}) == 120, 'W(H4) maps (14400 = 2 x 120 x 120 / 2) permute the corners')
for faces, name in ((tri, 'edge triangles'), (rect, 'golden rectangles'), (rt, 'radius triangles')):
    C(orbit_count(faces) == 1, f'W(H4) transitive on the {name}')
# one face of each class by hand: the radius triangle 1, (1,1,1,1)/2, (1,1,1,-1)/2 has normal (0,1,-1,0)/sqrt2, a cell centre direction
n = canon(normal([[1,0,0,0],[.5,.5,.5,.5],[.5,.5,.5,-.5]]))
C(n == canon(np.array([0, 1, -1, 0])) and n in cro, 'radius triangle {1, (1,1,1,1)/2, (1,1,1,-1)/2}: normal (0,1,-1,0) is a cross wall')
f0 = rect[0]; print('  a golden rectangle:', [list(np.round(V[i], 4)) for i in f0], 'normal', np.round(normal(V[list(f0)]), 4))
# 24-cells: cosets g*T of the five conjugate binary tetrahedral subgroups
T0 = {i for i, v in enumerate(V) if np.allclose(np.abs(v) * 2 % 1, 0)}  # the 24 Hurwitz units
C(len(T0) == 24, 'the 24 Hurwitz units form a 24-cell T0 in the 600-cell')
subs = {frozenset(idx[key(qmul(qmul(g, V[i]), conj(g)))] for i in T0) for g in V}
C(len(subs) == 5, 'five conjugate 24-cell subgroups')
c24 = {frozenset(idx[key(qmul(V[g], V[i]))] for i in T) for T in subs for g in range(120)}
C(len(c24) == 25, '25 inscribed 24-cells (left cosets)')
# for each 24-cell, its 24 cell-centre directions (12 axes): sums of the 6 corners of each octahedral cell
secs = {}
for S in c24:
    S = sorted(S); g = V[S] @ V[S].T
    # octahedral cells of a 24-cell: 6 corners pairwise at 60 or 90 degrees, centre = mean; find via each corner's 8 neighbours
    cents = set()
    # cell centres of a 24-cell: sums of the 6 corners of an octahedral cell (pairwise inner products 1/2, three opposite pairs at 0)
    for six in itertools.combinations(S, 6):
        sub = V[list(six)] @ V[list(six)].T
        off = sub[~np.eye(6, dtype=bool)]
        if np.all((np.abs(off - .5) < 1e-9) | (np.abs(off) < 1e-9)) and np.sum(np.abs(off) < 1e-9) == 6:
            cents.add(canon(V[list(six)].sum(0)))
    secs[frozenset(S)] = cents
allsec = [c for v in secs.values() for c in v]
C(all(len(v) == 12 for v in secs.values()), 'each 24-cell has 12 cell axes (24 octahedral cells)')
from collections import Counter
mult = Counter(allsec)
print(f'  sections: {len(allsec)} in all, {len(set(allsec))} distinct, {len(set(allsec) & cro)} cross walls, {len(set(allsec) & mir)} mirrors, multiplicities {sorted(Counter(mult.values()).items())}')
C(len(allsec) == 300 and set(allsec) == cro, 'the 25 x 12 middle sections across the 24-cells\' cell axes are exactly the 300 cross walls, each once')
# corners on a cross wall
n = np.array(list(cro)[0]); n = n / np.linalg.norm(n); on = [i for i in range(120) if abs(np.dot(V[i], n)) < 1e-6]
print('  corners on one cross wall:', len(on), ' on one mirror:', sum(1 for i in range(120) if abs(np.dot(V[i], V[0])) < 1e-9))
C(len(on) == 12, 'each cross wall holds 12 corners of the 600-cell (checked on one; all walls are one orbit)')
print('FINAL ' + ('ok' if ok else 'FAIL'))
