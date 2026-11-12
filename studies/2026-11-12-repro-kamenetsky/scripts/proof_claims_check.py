# proof_claims_check.py (12 Nov 2026): exact checks of the computable parts of Kamenetsky 2610.00139 beyond Theorems A and B.
# Lemma 4.2: Vol(C_N) = 2^N - 1; boundary = N 2^N unit panels; 3N maximal flat facets (panels grouped by hyperplane, then by
#   connectivity through shared (N-2)-faces); star-shaped about every point of [0,1]^N (checked on a grid: no cube of (1,2]^N is
#   reached on a segment from a kernel point to a cube centre of C_N; proof in PROOF_CHECK.md).
# Theorem 5.1: 2C_N = T_0 u U_v T_v with the paper's explicit children, disjoint interiors (unit-cube sets), N = 2..7.
# Used in our check of Proposition 7.1's proof: the central child T_0 shares a panel with every other child (N = 2..7).
# Controls: a wrong child (T_v without the reflection) must fail the dissection; a cube set with a hole must fail the panel count.
import itertools, sys
from collections import defaultdict
ok = True
def check(name, c):
    global ok; ok &= bool(c); print(('ok   ' if c else 'FAIL ') + name, flush=True)
def chair(N): return {u for u in itertools.product((0, 1), repeat=N) if not all(u)}          # unit cubes by min corner
def panels(cubes, N):
    P = set()
    for c in cubes:
        for i in range(N):
            for s in (0, 1):
                nb = list(c); nb[i] += 1 if s else -1
                if tuple(nb) not in cubes: P.add((c, i, s))
    return P
def facets(P, N):
    planes = defaultdict(list)
    for (c, i, s) in P: planes[(i, s, c[i] + s)].append(c)
    n = 0
    for (i, s, h), cs in planes.items():
        cs = set(cs); seen = set()
        for c0 in cs:
            if c0 in seen: continue
            n += 1; st = [c0]; seen.add(c0)
            while st:
                c = st.pop()
                for j in range(N):
                    if j == i: continue
                    for dlt in (-1, 1):
                        d = list(c); d[j] += dlt; d = tuple(d)
                        if d in cs and d not in seen: seen.add(d); st.append(d)
    return n
def children(N, reflect=True):
    C = chair(N); kids = [{tuple(x + 1 for x in u) for u in C}]                                # T_0 = C_N + (1,...,1)
    for v in itertools.product((0, 1), repeat=N):
        if all(v): continue
        T = set()
        for u in C:
            # cube [u, u+1] -> D_s(v) then + c(v) + 2v: coordinate i with v_i = 1 maps [u_i, u_i+1] to [2-u_i-1, 2-u_i] + 2
            T.add(tuple((2 * v[i] + (1 - u[i] if (reflect and v[i]) else u[i])) for i in range(N)))
        kids.append(T)
    return kids
for N in range(2, 8):
    C = chair(N); P = panels(C, N)
    check(f'N={N} Lemma 4.2 (1): volume {len(C)} = 2^N - 1', len(C) == 2 ** N - 1)
    check(f'N={N} Lemma 4.2 (3): {len(P)} panels = N 2^N, {facets(P, N)} maximal flat facets = 3N', len(P) == N * 2 ** N and facets(P, N) == 3 * N)
    # star-shaped about kernel points: sample kernel points p in [0,1]^N and every cube centre x; segment must avoid (1,2]^N interior
    bad = 0
    for p in [(0.0,) * N, (0.5,) * N, tuple(0.9 if i % 2 else 0.1 for i in range(N))]:
        for u in C:
            x = [ui + 0.5 for ui in u]
            for t in [k / 64 for k in range(65)]:
                y = [p[i] + t * (x[i] - p[i]) for i in range(N)]
                if all(yi > 1 for yi in y): bad += 1
    check(f'N={N} Lemma 4.2 (2): segments from kernel points to every cube centre avoid (1,2]^N (sampled)', bad == 0)
    K = children(N); big = {u for u in itertools.product(range(4), repeat=N) if not all(x >= 2 for x in u)}
    allc = [c for k in K for c in k]
    check(f'N={N} Theorem 5.1: {len(K)} children = 2^N, disjoint ({len(allc)} cubes, {len(set(allc))} distinct), union = 2C_N ({len(big)} cubes)',
          len(K) == 2 ** N and len(allc) == len(set(allc)) and set(allc) == big)
    shapes_ok = all(len(k) == 2 ** N - 1 for k in K)
    check(f'N={N} Theorem 5.1: every child has 2^N - 1 cubes', shapes_ok)
    T0 = K[0]; P0 = panels(T0, N)
    def shares_panel(A, B):
        return any(tuple(c[j] + (1 if (j == i and s) else (-1 if j == i else 0)) for j in range(N)) in B for (c, i, s) in panels(A, N))
    check(f'N={N} (used for Prop. 7.1): central child shares a panel with every other child', all(shares_panel(T0, k) for k in K[1:]))
# controls
Kbad = children(3, reflect=False); allb = [c for k in Kbad for c in k]
check('control: children without the reflection do NOT dissect 2C_3', len(allb) != len(set(allb)))
hole = chair(3) - {(1, 1, 0)}                                    # a cube with only two neighbours
check('control: a cube set missing a cube does NOT give N 2^N panels', len(panels(hole, 3)) != 3 * 2 ** 3)
print('FINAL ok' if ok else 'FINAL FAIL')
