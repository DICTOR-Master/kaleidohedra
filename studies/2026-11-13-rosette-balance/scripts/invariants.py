"""Linear invariants of the sweep ledgers of the perturbed 16-cells (data/rosette-full.json): exact nullspace of the centred
ledger matrix, and which of its vectors are NOT combinations of the counting functionals (corners, down edges, contacts lost and
made, cells dying and born)."""
import json, sys
from fractions import Fraction as Fr
d = json.load(open(sys.argv[1]))
L = [x['ledger'] for r in d['general'] if r['polytope'].endswith('16-cell') for x in r['directions']]
cls = sorted({k for l in L for k in l}); ev = [eval(k) for k in cls]
rows = [[Fr(l.get(k, 0)) for k in cls] for l in L]; n = len(cls)
mean = [sum(c) / len(rows) for c in zip(*rows)]
def rref(M):
    M = [r[:] for r in M]; piv = []; r = 0
    for c in range(len(M[0])):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; M[r] = [a / M[r][c] for a in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0: f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
        if r == len(M): break
    return M[:r], piv
R, piv = rref([[a - m for a, m in zip(r, mean)] for r in rows])
free = [c for c in range(n) if c not in piv]; null = []
for f in free:
    v = [Fr(0)] * n; v[f] = Fr(1)
    for i, p in enumerate(piv): v[p] = -R[i][f]
    null.append(v)
print('classes (down, lost, made, die, born) and min..max count over', len(L), 'sweeps:')
for k, c in enumerate(cls): print('  ', c, int(min(r[k] for r in rows)), '..', int(max(r[k] for r in rows)), 'mean', float(mean[k]))
cnt = [[Fr(1)] * n] + [[Fr(t[i]) for t in ev] for i in range(5)] + [[Fr(int(t[0] == 0)) for t in ev], [Fr(int(t[0] == 6)) for t in ev]]
names = ['corners', 'down edges', 'contacts lost', 'contacts made', 'cells dying', 'cells born', 'lowest corner', 'highest corner']
Rc, _ = rref(cnt); print('counting functionals (with one lowest and one highest corner) rank', len(Rc), '; ledger invariants (nullspace) dim', len(null))
for v in null:
    val = sum(a * b for a, b in zip(v, mean))
    inspan = len(rref(Rc + [v])[0]) == len(Rc)
    print('  invariant', {cls[k]: str(v[k]) for k in range(n) if v[k] != 0}, '= ', val, ' counting combination:', inspan)
