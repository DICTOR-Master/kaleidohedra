# l = 16, the (6, 6) terms of Theorem B with |P| = 4: where do they cancel? (28 Nov 2026, with Claude (Anthropic))
# Flat model: root honeycomb = (k,.,0) [letter s0] + (k-1,.,1) [letter sm]; far honeycomb = (k,.,1) [s0] + (k+1,.,0) [sp].
# A bond joins a lower-sublayer atom b to an upper-sublayer atom a when (b - a) is a short vector (the orientation fixed by
# the letters). Linkages of 6 edges with 4 ends here are one 2-edge arc and one 4-edge arc, all atoms distinct.
import itertools, sys
from collections import defaultdict
SV = [(1,1),(-2,1),(1,-2),(-1,-1),(2,-1),(-1,2)]
def ok(p, s): return p[0] % 3 == s and p[1] % 3 == s
def nb(a, sa, sb):
    return [(a[0]+d[0], a[1]+d[1]) for d in SV if ok((a[0]+d[0], a[1]+d[1]), sb)]
def arcs2(p, q, sa, sb):   # p - m - q
    return [[p, m, q] for m in nb(p, sa, sb) if q in nb(m, sb, sa) and q != p]
def arcs4(p, q, sa, sb):   # p - m1 - x - m2 - q
    out = []
    for m1 in nb(p, sa, sb):
        for x in nb(m1, sb, sa):
            if x in (p, q): continue
            for m2 in nb(x, sa, sb):
                if m2 != m1 and q in nb(m2, sb, sa): out.append([p, m1, x, m2, q])
    return out
def linkages(P, pairing, sa, sb):
    (a, b), (c, d) = pairing; out = []
    for X, Y in (((a, b), (c, d)), ((c, d), (a, b))):
        for s in arcs2(*X, sa, sb):
            for l in arcs4(*Y, sa, sb):
                atoms = s + l
                if len(set(atoms)) == 8:
                    # A-atoms of type 'a' and B-atoms tagged by position in path: B are odd indices
                    out.append((tuple(s), tuple(l)))
    return out
def matchings(P):
    a, b, c, d = sorted(P)
    return [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]
def run(sm, s0, sp, vtype):
    # v: an end-sublayer root atom (k, v, 0) [vtype 'A'] at a site of letter s0, or a lower root atom (k-1, v, 1) [vtype 'B'] of letter sm
    v = (s0, s0) if vtype == 'A' else (sm, sm)
    c = ((2*s0) % 3, (2*s0) % 3)
    # root linkages of 6 edges through v: enumerate P from arcs near v
    pts = [(x, y) for x in range(-30, 31) for y in range(-30, 31) if ok((x, y), s0)]
    near = [p for p in pts if abs(p[0]-v[0]) + abs(p[1]-v[1]) <= 26]
    W = defaultdict(int)
    # build all root arcs touching or not v; a linkage = short + long arc, v on one of them
    A2 = {}; A4 = {}
    nearset = set(near)
    def close(p, q): return abs(p[0]-q[0]) + abs(p[1]-q[1]) <= 12
    for p, q in itertools.combinations(near, 2):
        if not close(p, q): continue
        a2 = arcs2(p, q, s0, sm); a4 = arcs4(p, q, s0, sm)
        if a2: A2[(p, q)] = a2
        if a4: A4[(p, q)] = a4
    for (p, q), L2 in A2.items():
        for (r, t), L4 in A4.items():
            if len({p, q, r, t}) < 4: continue
            for s in L2:
                for l in L4:
                    atoms = s + l
                    if len(set((i % 2, z) for i, z in enumerate(s)) | set((i % 2, z) for i, z in enumerate(l))) < 8: continue
                    onv = (vtype == 'A' and v in (s[0], s[2], l[0], l[2], l[4])) or (vtype == 'B' and v in (s[1], l[1], l[3]))
                    if not onv: continue
                    P = frozenset((p, q, r, t)); M = frozenset((frozenset((p, q)), frozenset((r, t))))
                    W[(P, M)] += 1
    def Fc(P, N):
        pr = [tuple(sorted(x)) for x in N]
        cnt = 0
        for X, Y in ((pr[0], pr[1]), (pr[1], pr[0])):
            for s in arcs2(*X, s0, sp):
                for l in arcs4(*Y, s0, sp):
                    if len(set((i % 2, z) for i, z in enumerate(s)) | set((i % 2, z) for i, z in enumerate(l))) == 8: cnt += 1
        return cnt
    g = lambda p: (c[0]-p[0], c[1]-p[1])
    S = 0; perPM = defaultdict(int); nz = 0
    for (P, M), w in W.items():
        for N in matchings(P):
            N = frozenset(frozenset(x) for x in N)
            if N == M: continue
            af = Fc(P, N) - Fc(frozenset(map(g, P)), frozenset(frozenset(map(g, x)) for x in N))
            S += w * af; perPM[(P, M)] += w * af
            if af: nz += 1
    bad = sum(1 for x in perPM.values() if x)
    print(f"sm={sm} s0={s0} sp={sp} v={vtype}: (P,M) {len(W)}, nonzero Af {nz}, (P,M) with nonzero sum {bad}, total S = {S}")
    return S
tot = 0
for s0 in [0]:
    for sm in (1, 2):
        for sp in (1, 2):
            for vt in 'AB':
                tot += abs(run(sm, s0, sp, vt))
print('FINAL ok' if tot == 0 else 'FINAL FAIL nonzero total')
