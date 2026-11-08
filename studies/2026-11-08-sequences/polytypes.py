"""Close-packed stackings counted by period (exact, by enumeration). A stacking of period n is a cyclic word in A, B, C of length n
with no two neighbours equal (also across the wrap), whose smallest period is exactly n. Two words give the same structure when one
is a cyclic shift and/or a relabelling of the letters (any of the 6 permutations of A, B, C: a translation or rotation of the
layer); with --mirror also a reversal (reading the stack upside down). Also the triangle by number of h layers (hexagonality).
Prints the sequences for an OEIS search."""
import itertools, sys
from collections import Counter
N = int(sys.argv[1]) if len(sys.argv) > 1 else 16
PERMS = [dict(zip('ABC', p)) for p in itertools.permutations('ABC')]
def words(n):
    for w in itertools.product('ABC', repeat=n):
        if all(w[i] != w[(i + 1) % n] for i in range(n)): yield w
def smallest_period(w):
    n = len(w)
    for d in range(1, n + 1):
        if n % d == 0 and all(w[i] == w[(i + d) % n] for i in range(n)): return d
def canon(w, mirror):
    n = len(w); best = None; cands = [w, w[::-1]] if mirror else [w]
    for x in cands:
        for p in PERMS:
            y = tuple(p[c] for c in x)
            for s in range(n):
                z = y[s:] + y[:s]
                if best is None or z < best: best = z
    return best
def hc(w):  # Jagodzinski: layer i is h when its two neighbours are equal
    n = len(w); return ''.join('h' if w[i - 1] == w[(i + 1) % n] else 'c' for i in range(n))
res = {}
for mirror in (False, True):
    seq = []; tri = []
    for n in range(1, N + 1):
        cl = {}
        for w in words(n):
            if smallest_period(w) != n: continue
            cl.setdefault(canon(w, mirror), w)
        seq.append(len(cl)); tri.append(Counter(hc(w).count('h') for w in cl.values()))
    res[mirror] = (seq, tri)
    print(('WITH reversal' if mirror else 'WITHOUT reversal') + f', n = 1..{N}:', ', '.join(map(str, seq)))
    for n, t in enumerate(tri, 1):
        print(f'  n={n}: by number of h layers', dict(sorted(t.items())))
KNOWN = {False: [0, 1, 1, 1, 1, 2, 3, 6, 10, 18, 31, 59, 105, 198, 371, 713], True: [0, 1, 1, 1, 1, 2, 3, 6, 7, 16, 21, 43, 63, 129, 203, 404]}
ok = all(res[m][0] == KNOWN[m][:N] for m in res) and all(sum(t.values()) == res[m][0][i] for m in res for i, t in enumerate(res[m][1]))
print('FINAL ok' if ok else 'FINAL FAIL: counts differ from OEIS A011957 / A011768 or rows do not sum')
