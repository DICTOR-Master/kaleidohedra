# grogan_pN.py: our own N-dimensional chair code (written for this check; generalises recount.py, none of the authors' code) applied to
# Grogan's arithmetic child rule (aiXiv 2610.01307, eq. rule): f_A(i) = mu g^{|A|} (i - z_A) on F_p, signs -1 on A, outer translation
# 4*1_A, centre i -> mu i with translation 1. Computes the least contact language E (all face contacts inside substituted supertiles,
# closed under cross-child contacts) and compares |E| with his Proposition E formula
#   |E| = 2^(p+1) + (p+1)^2 - 2 (ell = 2),   2^(p+1) + 2p^2 - 2p + 2 + p*ell/2 (ell > 2),   ell = ord(g) mod p,
# and, if given, with his data file (a list of contacts) by count.
# usage: grogan_pN.py p g mu [his E json]
import sys, itertools, json, time
p, g, mu = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); N = p; t0 = time.time()
def act(h, x): f, s = h; return tuple(s[i] * x[f[i]] for i in range(N))
def mul(h, k):                                  # (h k)(x) = h(k(x)): (hk)(x)_i = s_i * (k x)_{f(i)} = s_i * t_{f(i)} x_{F(f(i))}
    f, s = h; F, t = k; return (tuple(F[f[i]] for i in range(N)), tuple(s[i] * t[f[i]] for i in range(N)))
def inv(h):
    f, s = h; fi = [0] * N; si = [1] * N
    for i in range(N): fi[f[i]] = i; si[f[i]] = s[i]
    return (tuple(fi), tuple(si))
ID = (tuple(range(N)), (1,) * N)
U = [u for u in itertools.product((0, 1), repeat=N) if any(c == 0 for c in u)]
LOC = [tuple(2 * c + 1 for c in u) for u in U]
DIRS = [tuple(2 * s if j == i else 0 for j in range(N)) for i in range(N) for s in (1, -1)]
def cubes(pose): h, t = pose; return [tuple(a + 2 * b for a, b in zip(act(h, c), t)) for c in LOC]
def rel(A, B): hA, tA = A; hB, tB = B; hi = inv(hA); return (mul(hi, hB), act(hi, tuple(b - a for a, b in zip(tA, tB))))
ell = next(k for k in range(1, p) if pow(g, k, p) == 1)
inv_mod = lambda a: pow(a, p - 2, p)
def f_role(A):
    if not A: return tuple((mu * i) % p for i in range(p))
    z = (sum(A) * inv_mod(len(A))) % p
    return tuple((mu * pow(g, len(A), p) * (i - z)) % p for i in range(p))
CH = [((tuple((mu * i) % p for i in range(p)), (1,) * N), (1,) * N)]
for v in U:
    A = [i for i in range(N) if v[i]]
    CH.append(((f_role(A), tuple(-1 if v[i] else 1 for i in range(N))), tuple(4 * c for c in v)))
def kids(S): G, T = S; return [(mul(G, h), tuple(a + b for a, b in zip(T, act(G, tau)))) for h, tau in CH]
S0 = kids((ID, (0,) * N))
allc = [c for k in S0 for c in cubes(k)]
big = {tuple(2 * c + 1 for c in u) for u in itertools.product(range(4), repeat=N) if any(c < 2 for c in u)}
part = len(allc) == len(set(allc)) and set(allc) == big
def contacts(tiles):
    own = {}
    for i, t in enumerate(tiles):
        for c in cubes(t): own[c] = i
    out = set()
    for i, t in enumerate(tiles):
        for c in cubes(t):
            for d in DIRS:
                j = own.get(tuple(a + b for a, b in zip(c, d)))
                if j is not None and j != i: out.add(rel(t, tiles[j]))
    return out
P1 = contacts(S0); A = set(P1); lev = 1; cache = {}
while True:
    B = set(P1)
    for (h, t) in A:
        if (h, t) not in cache: cache[(h, t)] = contacts(S0 + kids((h, tuple(2 * x for x in t))))
        B |= cache[(h, t)]
    lev += 1
    print(f'level {lev}: |E| {len(B)} ({time.time()-t0:.0f}s)', flush=True)
    if B == A: break
    A = B
formula = 2 ** (p + 1) + (p + 1) ** 2 - 2 if ell == 2 else 2 ** (p + 1) + 2 * p * p - 2 * p + 2 + p * ell // 2
line = f'p {p} g {g} mu {mu} (ell {ell}): children partition 2C_p {part}; |E| {len(A)}; his formula {formula}'
his = None
if len(sys.argv) > 4:
    D = json.load(open(sys.argv[4])); his = D if isinstance(D, list) else next((v for v in D.values() if isinstance(v, list)), None)
    # his format: frame = [s_i * (f(i) + 1)], translation t; the same t as ours (his cell lower corners t + hb - 1_D at side 1 are our
    # cube centres h(2b+1) + 2t at side 2, since h(1) = 1 - 2*1_D)
    H = {((tuple(abs(x) - 1 for x in e['frame']), tuple(1 if x > 0 else -1 for x in e['frame'])), tuple(e['translation'])) for e in his}
    line += f'; his data file lists {len(his)}; same set as ours: {H == A} (only ours {len(A - H)}, only his {len(H - A)})'
    his = H
import os
if os.environ.get('DUMP'):                     # 12 Nov: dump E (frame as signed 1-based index list, translation) for set comparisons
    json.dump(sorted([[s_i * (f_i + 1) for f_i, s_i in zip(h[0], h[1])], list(t)] for h, t in A), open(os.environ['DUMP'], 'w'))
print(line, flush=True)
ok = part and len(A) == formula and (his is None or his == A)
print('FINAL ok' if ok else 'FINAL FAIL', flush=True)
