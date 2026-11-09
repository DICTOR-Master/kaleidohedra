"""probe: E6u0 + shear(1,0): which layer-graph steps lie on cycles (strongly connected components), per lattice."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pieces import *
REL = reliefs()
PE = make(*REL['E6u0'], shear((1, 0)), (1, 0))
for mir in (False, True):
    sts, info = states_l([PE], mir)
    T, C = inlayer_table(sts), inter_table(sts)
    for M in hnf(3):
        r = periodic_alive_l(T, C, len(sts), M, budget=4e8)
        if r is None or not r[0]:
            continue
        alive, edges, V = r
        adj = {}
        for a, l, b in edges:
            adj.setdefault(a, set()).add(b)
        def reach(x):
            seen, st = {x}, [x]
            while st:
                y = st.pop()
                for z in adj.get(y, ()):
                    if z not in seen:
                        seen.add(z); st.append(z)
            return seen
        R = {x: reach(x) for x in alive}
        # an edge a->b lies on a cycle iff a is reachable from b
        lab = {}
        for a, l, b in edges:
            lab.setdefault((a, b), set()).add(l)
        oncyc = [(a, l, b) for a, l, b in edges if a in R[b]]
        # c/h letter of a step needs the previous lean: count lean CHANGES along cycles: a cycle with both leans
        leans_on_cycles = {l for a, l, b in oncyc}
        mixed = False
        for a, l, b in oncyc:
            for a2, l2, b2 in oncyc:
                if a2 == b and l2 != l and a in R[b2] | {b2}:
                    mixed = True
        comps = {frozenset(x for x in alive if x in R[y] and y in R[x]) for y in alive}
        cid = {x: c for c in comps for x in c}
        trans = {(cid[a], cid[b]) for a, l, b in edges if cid[a] != cid[b]}
        # longest chain of components (number of one-way steps a stack can make)
        import functools
        @functools.lru_cache(None)
        def longest(c):
            return max([1 + longest(d) for (e, d) in trans if e == c] or [0])
        chain = max(longest(c) for c in comps)
        print(f'   components {len(comps)} (sizes {sorted(len(c) for c in comps)}), one-way steps between them '
              f'{len(trans)}, longest chain of one-way steps {chain}')
        print(f'mirrors {mir} M {M}: alive {len(alive)}, steps {len(edges)}, on cycles {len(oncyc)}, '
              f'leans used on cycles {sorted(leans_on_cycles)}, cycle through a lean change (an h): {mixed}')
print('probe done (exploratory, no check)')
