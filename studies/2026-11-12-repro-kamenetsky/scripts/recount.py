# recount.py, DICTO 12 Nov 2026 (independent reproductions on aiXiv; "we could maybe use our own runs as verifying methods").
# INDEPENDENT recount of the headline numbers of Kamenetsky, "Towards Strongly Aperiodic Monotiles in Higher Dimensions" (aiXiv
# 2610.00139, arXiv 2610.00916), written from the paper's definitions only (none of his code is imported): the chair C3 (7 unit cubes),
# lattice-registered poses (g in B3, integer t; cubes g(2u+1) + 2t), the rep-8 substitution of Theorem 5.1 with the frame assignment
# printed in his README / Figure 2, the hierarchical language P0 = least fixed point of P1 and X(P0), the coarsening closure
# P_{i+1} = P_i + {(G, T/2)} over admissible aligned supertile poses, and the facet triples.
# Paper's numbers to reproduce: 2388 touching poses; |P0| = 30; closure 30 -> 44 -> 44 with no offset pose; |F*| = 135; tight (44).
# Negative control: one child's frame changed (as in our 12 Nov rerun of his code) must NOT close at 44.
import itertools, sys, time
t0 = time.time()
def perms3(): return list(itertools.permutations(range(3)))
B3 = [(p, s) for p in perms3() for s in itertools.product((1, -1), repeat=3)]
def act(g, x): p, s = g; return tuple(s[i] * x[p[i]] for i in range(3))
def mul(g, h):                      # (g h)(x) = g(h(x)); found by acting on the basis (independent of any formula in his code)
    E = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]; img = [act(g, act(h, e)) for e in E]
    p = [None] * 3; s = [None] * 3
    for j, v in enumerate(img):     # column j = image of e_j: v has one nonzero entry at row i, so x_j feeds coordinate i
        i = next(k for k in range(3) if v[k]); p[i] = j; s[i] = v[i]
    return (tuple(p), tuple(s))
def inv(g): return next(h for h in B3 if mul(g, h) == ((0, 1, 2), (1, 1, 1)))
def det(g):
    import numpy as np
    M = np.array([act(g, e) for e in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]]).T; return round(np.linalg.det(M))
ID = ((0, 1, 2), (1, 1, 1))
U = [u for u in itertools.product((0, 1), repeat=3) if u != (1, 1, 1)]
LOC = [tuple(2 * c + 1 for c in u) for u in U]
def cubes(pose): g, t = pose; return frozenset(tuple(a + 2 * b for a, b in zip(act(g, c), t)) for c in LOC)
DIRS = [d for d in itertools.product((-2, 0, 2), repeat=3) if sum(map(abs, d)) == 2]
def touch(A, B):
    if A & B: return False
    return any(tuple(a + b for a, b in zip(c, d)) in B for c in A for d in DIRS)
def rel(A, B):                       # pose of B in A's frame
    gA, tA = A; gB, tB = B; gi = inv(gA); return (mul(gi, gB), act(gi, tuple(b - a for a, b in zip(tA, tB))))
def absolute(A, r): gA, tA = A; g, t = r; return (mul(gA, g), tuple(a + b for a, b in zip(tA, act(gA, t))))
# --- all touching poses (paper: 2388)
def all_touching():
    out = []
    for g in B3:
        for t in itertools.product(range(-4, 6), repeat=3):
            if touch(base, cubes((g, t))): out.append((g, t))
    return out
base = cubes((ID, (0, 0, 0)))
TOUCH = all_touching() if __name__ == '__main__' else []
assert all(-4 < x < 5 for g, t in TOUCH for x in t), 'GUARD: a touching pose on the edge of the search box: widen it'   # once-only guard (12 Nov)
_UNUSED = []
if __name__ == '__main__': print(f'touching lattice-registered poses: {len(TOUCH)} (paper 2388)', flush=True)
# --- substitution (Theorem 5.1): T0 = translate by (1,1,1); T_v = reflection D_s(v) composed with pi_v, placed in block 2v (scale-2 coords: shift 4v)
def children(frames):
    out = [(ID, (1, 1, 1))]
    for v in U:
        D = ((0, 1, 2), tuple(-1 if c else 1 for c in v)); pi = (tuple(frames[v]), (1, 1, 1))
        out.append((mul(D, pi), tuple(4 * c for c in v)))
    return out
def kids(S, CH, lev=1):              # children of a level-1 supertile with pose S (translations of children scale by 2^(lev-1))
    G, T = S; return [(mul(G, h), tuple(a + b for a, b in zip(T, act(G, tuple(2 ** (lev - 1) * x for x in tau))))) for h, tau in CH]
def check_partition(CH):
    allc = [c for k in kids((ID, (0, 0, 0)), CH) for c in cubes(k)]
    big = {tuple(2 * c + 1 for c in u) for u in itertools.product(range(4), repeat=3) if any(c < 2 for c in u)}
    return len(allc) == len(set(allc)) == 56 and set(allc) == big
def contacts(tiles):
    cs = [cubes(t) for t in tiles]; out = set()
    for i in range(len(tiles)):
        for j in range(len(tiles)):
            if i != j and touch(cs[i], cs[j]): out.add(rel(tiles[i], tiles[j]))
    return out
def language(CH):
    S0 = kids((ID, (0, 0, 0)), CH); P1 = contacts(S0); A = set(P1)
    while True:
        B = set(P1)
        for (g, t) in A:
            S1 = kids((g, tuple(2 * x for x in t)), CH); B |= contacts(S0 + S1)   # two supertiles in relative pose (g, 2t)
        if B == A: return A
        A = B
def sigma(P, CH):                     # admissible supertile poses (G, T) touching the reference supertile
    S0 = kids((ID, (0, 0, 0)), CH); C0 = [cubes(k) for k in S0]; out = set()
    inv_child = [(inv(h), tuple(-x for x in act(inv(h), tau))) for h, tau in CH]
    for a in S0:
        for p in P:
            b = absolute(a, p)
            for hi, ti in inv_child:   # b is child k of supertile S: S = b * (child k)^-1
                S = absolute(b, (hi, ti)); K = kids(S, CH); CK = [cubes(k) for k in K]
                ok = all(not (x & y) for x in CK for y in C0)
                if ok:
                    for i, x in enumerate(S0):
                        for j, y in enumerate(K):
                            if touch(C0[i], CK[j]) and rel(x, y) not in P: ok = False; break
                        if not ok: break
                if ok and any(touch(x, y) for x in C0 for y in CK): out.add(S)
    return out
def closure(CH, maxit=6):
    P = language(CH); hist = [len(P)]
    for _ in range(maxit):
        Sg = sigma(P, CH)
        if any(x % 2 for _, T in Sg for x in T): return None, hist + ['offset']
        new = {(G, tuple(x // 2 for x in T)) for G, T in Sg}
        hist.append(len(P | new))
        if new <= P: return P, hist + [f'Sigma = 2P: {new == P}']
        P |= new
    return None, hist + ['no stop']
def facets(P):
    F = set()
    for g, t in P:
        Bc = cubes((g, t)); gi = inv(g)
        for c in LOC:
            for d in DIRS:
                nb = tuple(a + b for a, b in zip(c, d))
                if nb in Bc and nb not in LOC:
                    lc = act(gi, tuple(a - 2 * b for a, b in zip(nb, t))); ld = act(gi, tuple(-x for x in d))
                    F.add(((c, d), (lc, ld), g))
    return F
if __name__ == '__main__':
    FR = {(0, 0, 0): (0, 1, 2), (0, 0, 1): (0, 2, 1), (0, 1, 0): (2, 1, 0), (0, 1, 1): (1, 2, 0), (1, 0, 0): (1, 0, 2), (1, 0, 1): (0, 1, 2), (1, 1, 0): (2, 0, 1)}
    ok = True
    for name, fr in (('certified', FR), ('control: child (1,1,0) changed', {**FR, (1, 1, 0): (1, 0, 2)})):
        CH = children(fr); part = check_partition(CH); homo = all(det(h) == 1 for h, _ in CH)
        P0 = language(CH); Ps, hist = closure(CH)
        line = f'{name}: children partition 2C3 {part}; homochiral {homo}; |P0| {len(P0)}; closure {hist}'
        if Ps is not None:
            F = facets(Ps); PF = [p for p in TOUCH if (lambda tr: tr and tr <= F)(facets({p}))]
            line += f'; |P*| {len(Ps)}; |F*| {len(F)}; tight {set(PF) == Ps} ({len(PF)})'
        print(line, f'({time.time()-t0:.0f}s)', flush=True)
        if name == 'certified': ok &= part and homo and len(TOUCH) == 2388 and len(P0) == 30 and Ps is not None and len(Ps) == 44 and len(F) == 135 and set(PF) == Ps
        else: ok &= Ps is None or len(Ps) != 44
    print('FINAL ok: every number reproduced independently and the wrong marking rejected' if ok else 'FINAL FAIL', flush=True)
