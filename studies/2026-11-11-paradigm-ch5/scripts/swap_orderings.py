"""Chapter 5: in a sweep of the 4D permutohedron (corners = orderings x of 1..5) by f(x) = u.x with u1 < u2 < ... < u5 (generic),
the edge from x to the ordering with values k and k+1 exchanged goes DOWN exactly when k stands to the left of k+1. Check: (i) the
direct count of down edges at every corner equals the number of such k; (ii) corners by that number = 1, 26, 66, 26, 1 (Eulerian);
(iii) the same for a random generic increasing u."""
import itertools, random
ok = True
for trial in range(3):
    u = sorted(random.random() for _ in range(5)) if trial else [1, 2, 3, 4, 5]
    cnt = [0] * 5
    for x in itertools.permutations(range(1, 6)):
        f = sum(a * b for a, b in zip(u, x)); pos = {v: i for i, v in enumerate(x)}
        down = 0
        for k in range(1, 5):
            y = list(x); y[pos[k]], y[pos[k + 1]] = k + 1, k
            if sum(a * b for a, b in zip(u, y)) < f: down += 1
        rule = sum(1 for k in range(1, 5) if pos[k] < pos[k + 1])
        ok &= down == rule; cnt[down] += 1
    print('u', [round(a, 3) for a in u], 'corners by edges below', cnt); ok &= cnt == [1, 26, 66, 26, 1]
print('FINAL ok' if ok else 'FINAL FAIL')
