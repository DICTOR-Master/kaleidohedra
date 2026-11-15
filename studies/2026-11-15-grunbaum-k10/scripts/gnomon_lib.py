#!/usr/bin/env python3
"""Gnomon step on zones (DICTO's tool, read for zones): grow a k = 8 surface into a k = 10 surface by adding one whole zone layer.
The book's gnomon (The Golden Cycle, Ch. 14, after Euclid and Heron) is the shell that, added to a solid, gives the next solid. Here the
shell is a band of golden rhombi along a new axis e_6: cut the k = 8 surface along a closed edge path that uses exactly two edges of
each of the five directions (opposite senses), shift one side by e_6, and close the cut with the ten rhombi (d, 6). Every old zone grows
by 2 faces (8 -> 10) and the new zone has 10 faces, so the result is in class C(6). This is the zonotope step RI -> RT made local.
Sources: all class C(5) surfaces reached from the rhombic icosahedron by exact corner flips up to the given depth (Grunbaum's D1/D2
among them). For every result: class check, Grunbaum's non-coplanar rule, face-pair rank (combinatorial: the same for the golden
embedding and its Galois twin), and an exact embedding check (faces with no common lattice vertex must be strictly apart; faces with a
common vertex are not tested, so 'embedded' here is a necessary check only). Usage: gnomon.py depth5 out.json"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from zsurf import *
t0 = time.time()
DEPTH = 3
G5, G6 = Geo(5), Geo(6); syms5, syms6 = signed_perms(G5), signed_perms(G6)

def bfs5():
    S0 = zonotope(G5); level = {canon(G5, S0, syms5): S0}; seen = set(level); out = []
    for d in range(DEPTH + 1):
        nxt = {}
        for S in level.values():
            info, _ = analyse(G5, S)
            if info is None or not in_class(G5, info): continue
            out.append((d, S))
            if d < DEPTH:
                for kind, T, cell in corner_moves(G5, S, info):
                    kk = canon(G5, T, syms5)
                    if kk not in seen: seen.add(kk); nxt[kk] = T
        level = nxt
    return out

def traverses_forward(f, s, e):
    """does face f (outward side s) run along edge e = (q, d) from q to q + e_d?"""
    p, a, b = f; q, d = e
    if (q, d) == (p, a): fw = True
    elif (q, d) == (vadd(p, unit(5, a)), b): fw = True
    elif (q, d) == (vadd(p, unit(5, b)), a): fw = False
    elif (q, d) == (p, b): fw = False
    else: raise ValueError
    return fw if s > 0 else not fw

def cycles(S):
    """simple closed edge paths with exactly two edges of each direction, of opposite senses (so the path closes)"""
    adj = {}
    for f in S:
        for (q, d) in edges_of(f, 5):
            r = vadd(q, unit(5, d))
            adj.setdefault(q, set()).add((r, (q, d), d, +1)); adj.setdefault(r, set()).add((q, (q, d), d, -1))
    verts = sorted(adj); found = set(); res = []
    for v0 in verts:
        st = [(v0, [v0], [], [0]*5, [0]*5)]
        while st:
            v, path, es, cnt, sgn = st.pop()
            for (w, e, d, sg) in adj[v]:
                if cnt[d] == 2: continue
                if cnt[d] == 1 and sgn[d] == sg: continue
                if w == v0 and len(es) == 9:
                    key = frozenset(es + [e])
                    if key not in found: found.add(key); res.append(es + [e])
                    continue
                if w in path or w < v0: continue
                if len(es) >= 9: continue
                c2 = cnt[:]; c2[d] += 1; s2 = sgn[:]; s2[d] = sg
                st.append((w, path + [w], es + [e], c2, s2))
    return res

def insert(S, cyc, shift_A):
    E = {}
    for f in S:
        for e in edges_of(f, 5): E.setdefault(e, []).append(f)
    cut = set(cyc); f0 = next(iter(S)); A = {f0}; st = [f0]
    while st:
        f = st.pop()
        for e in edges_of(f, 5):
            if e in cut: continue
            for g in E[e]:
                if g not in A: A.add(g); st.append(g)
    if len(A) == len(S): return None
    if not shift_A: A = set(S) - A
    B = set(S) - A; T = {}
    for f, s in S.items():
        p = f[0] + (0,)
        if f in A: p = vadd(p, unit(6, 5))
        T[(p, f[1], f[2])] = s
    for e in cyc:
        q, d = e; h = [g for g in E[e] if g in B][0]
        fw = traverses_forward(h, S[h], e)
        T[(q + (0,), d, 5)] = -1 if fw else 1
    return T

def embedded_partial(G, S):
    fl = list(S); cs = [set(corners(f, G.n)) for f in fl]
    for i in range(len(fl)):
        for j in range(i + 1, len(fl)):
            if cs[i] & cs[j]: continue
            if G.relation(fl[i][0], (fl[i][1], fl[i][2]), fl[j][0], (fl[j][1], fl[j][2])) != 'apart': return False
    return True

