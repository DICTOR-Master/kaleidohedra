#!/usr/bin/env python3
"""Covers of Theorem B' (d): write the question "is there a cover of Q's 720 pentagons by at most K dual copies of one family?"
as a CNF file (DIMACS), for a SAT solver whose UNSAT proof (DRAT) is then checked by drat-trim.

Variables 1..n: x_c = copy c is chosen (n = 120 for A*, B*; 60 for C3*).
Cover clauses: for each pentagon p, (x_c for every copy c covering p).
At most K: Sinz's sequential counter (Sinz 2005), written out here so it can be read:
  s(i, j) for i = 1..n-1, j = 1..K means "at least j of x_1..x_i are true";
  (-x_1 v s(1,1)); (-s(1,j)) for j > 1;
  for 1 < i < n: (-x_i v s(i,1)), (-s(i-1,1) v s(i,1)),
                 for j > 1: (-x_i v -s(i-1,j-1) v s(i,j)), (-s(i-1,j) v s(i,j)),
                 (-x_i v -s(i-1,K));
  (-x_n v -s(n-1,K)).
No symmetry breaking: the CNF says exactly "a cover with at most K copies exists".
Usage: make_cnf.py instance.json FAMILY K out.cnf     (prints FINAL ok / FINAL FAIL)"""
import sys, json
inst, fam, K, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
d = json.load(open(inst)); sets = d[fam]['sets']; n = len(sets)
cover = {}
for c, S in enumerate(sets):
    for p in S: cover.setdefault(p, []).append(c + 1)
ok = sorted(cover) == list(range(720)) and all(len(S) == 60 for S in sets)
cls = [cover[p] for p in range(720)]
s = lambda i, j: n + (i - 1) * K + j            # i = 1..n-1, j = 1..K
cls.append([-1, s(1, 1)])
for j in range(2, K + 1): cls.append([-s(1, j)])
for i in range(2, n):
    cls += [[-i, s(i, 1)], [-s(i - 1, 1), s(i, 1)]]
    for j in range(2, K + 1):
        cls += [[-i, -s(i - 1, j - 1), s(i, j)], [-s(i - 1, j), s(i, j)]]
    cls.append([-i, -s(i - 1, K)])
cls.append([-n, -s(n - 1, K)])
nv = n + (n - 1) * K
with open(out, 'w') as f:
    f.write(f'c covers of Theorem B\' (d): family {fam}, at most {K} of {n} copies, 720 pentagons, no symmetry breaking\n')
    f.write(f'p cnf {nv} {len(cls)}\n')
    for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
print(f'{fam} K={K}: {n} copies, {nv} variables, {len(cls)} clauses -> {out}')
print('FINAL ok' if ok else 'FINAL FAIL instance malformed (pentagons not 0..719 or a copy without 60 pentagons)')
