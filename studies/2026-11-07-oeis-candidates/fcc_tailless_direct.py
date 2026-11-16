# fcc: tailless (cyclically non-backtracking) closed walks per site, direct DP tracking the first step; n <= M.
import sys
M = int(sys.argv[1])
D = [(a, b, 0) for a in (1, -1) for b in (1, -1)] + [(a, 0, b) for a in (1, -1) for b in (1, -1)] + [(0, a, b) for a in (1, -1) for b in (1, -1)]
neg = {i: D.index(tuple(-x for x in d)) for i, d in enumerate(D)}
cur = {(d, i, i): 1 for i, d in enumerate(D)}   # (pos, last, first)
out = []
for n in range(1, M + 1):
    if n > 1:
        nxt = {}
        for (p, last, first), c in cur.items():
            for j, d in enumerate(D):
                if j == neg[last]: continue
                q = (p[0] + d[0], p[1] + d[1], p[2] + d[2])
                if abs(q[0]) + abs(q[1]) + abs(q[2]) > 2 * (M - n): continue
                k = (q, j, first); nxt[k] = nxt.get(k, 0) + c
        cur = nxt
    out.append(sum(c for (p, l, f), c in cur.items() if p == (0, 0, 0) and l != neg[f]))
print('fcc tailless 1..%d:' % M, ','.join(map(str, out)))
ref = [0, 0, 48, 264, 1680, 17016, 151872, 1401720, 13238400, 126357120, 1221557040, 11927724720]
ok = out == ref[:M]; print('matches #102 loops:', ok); print('FINAL ok' if ok else 'FINAL FAIL')
