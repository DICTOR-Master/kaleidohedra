"""General balance law, closed form (proof in README): in a generic sweep of a simple 4-polytope whose corners all see the same
multiset of cell types (m_t cells of type t at each corner, n_t cells of type t in all, N_X faces of type X), the swaps that CREATE a
contact of type X number  in(X) = N_X - sum_C c_X(t_C) + p_X,  with c_X(t) = faces of type X at a corner that involve a given cell of
type t, p_X = faces of type X at a corner. Checked against every simple row of the Atlas (sweeps)."""
import json, sys, ast
from collections import Counter
from math import comb
ok = True; rows = 0
for f in sys.argv[1:]:
    for key, r in json.load(open(f)).items():
        if not r.get('swaps'): continue
        V = r['corners']; n = {int(k): v for k, v in r['facets_by_node'].items()}
        m = {}
        for t in n:   # corners per cell of type t (all cells of a type are congruent)
            sz = [int(s) for s in r['facet_sizes_by_node'][str(t)]]; assert len(sz) == 1; m[t] = n[t] * sz[0] // V
        assert sum(m.values()) == 4, (key, m)
        N = Counter()
        for k, c in r['mirror_split'].items():
            a, b = k.split('types ')[1].split('+'); N[tuple(sorted((int(a), int(b))))] += c
        sw = Counter()
        for k, c in r['swaps'].items():
            X, Y = k.split('->'); sw[tuple(ast.literal_eval(Y))] += c
        for X in N:
            a, b = X
            if a != b: sc, p = n[a] * m[b] + n[b] * m[a], m[a] * m[b]
            else: sc, p = n[a] * (m[a] - 1), comb(m[a], 2)
            pred = N[X] - sc + p; rows += 1
            if pred != sw[X]: ok = False; print('MISMATCH', key, X, 'predicted', pred, 'swept', sw[X])
print(f'{rows} (polytope, face type) checks of in(X) = N_X - sum c_X + p_X')
print('FINAL ok' if ok else 'FINAL FAIL')
