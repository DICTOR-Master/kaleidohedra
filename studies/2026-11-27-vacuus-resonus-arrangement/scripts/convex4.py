"""Step 3c (27 Nov 2026; DICTO "continue"): convex solids made of whole pieces of P4 with Dehn invariant 0. With Claude (Anthropic).
A union of pieces (cone cells of the 19 planes, cut by P4) is convex exactly when it is P4 cut by a convex cone K bounded by some
of the 19 planes (its boundary lies in the cell walls). Enumerated: every K = intersection of k half-spaces of the 19 planes,
k = 1..KMAX (default 4), nonempty; up to P4's 48 symmetries. For each: the pieces in it by type (8 types, step 3a), its Dehn
invariant from the exact type vectors (step 3b; angle basis identified, not proved). Kept: Dehn invariant 0, i.e. the solids that
pass the necessary condition for filling space. Control: k = 0 (the whole P4) is Dehn zero."""
import os, sys, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'pieces4.py')).read(); exec(src[:src.index('types = []')])
cell_type = {}
for ti, (key, members) in enumerate(orbits.items()):
    for sv in members: cell_type[sv] = ti
src2 = open(os.path.join(HERE, 'dehn4.py')).read(); exec(src2[:src2.index('K = M.nullspace()')])
import sympy
KMAX = int(os.environ.get('KMAX', 4)); cells = list(signs); NPL = len(PL)
seen = set(); found = []; tested = 0
def dehn_zero(counts):
    v = M * sympy.Matrix(counts); return all(x == 0 for x in v)
assert dehn_zero([t['orbit_size'] for t in T]), 'control'
for k in range(1, KMAX + 1):
    for planes in itertools.combinations(range(NPL), k):
        for sg in itertools.product((1, -1), repeat=k):
            inside = frozenset(c for c in cells if all(c[p] == s for p, s in zip(planes, sg)))
            if not inside or inside in seen: continue
            # canonical up to symmetry
            can = min(tuple(sorted(act_sign(g, c) for c in inside)) for g in G)
            if can in seen: continue
            seen.add(can); seen.add(inside); tested += 1
            counts = [0] * len(T)
            for c in inside: counts[cell_type[c]] += 1
            if dehn_zero(counts):
                found.append(dict(planes=list(planes), signs=list(sg), pieces=len(inside), counts=counts))
    print(f'k = {k}: distinct convex unions so far {tested}; Dehn zero {len(found)}', flush=True)
found.sort(key=lambda r: r['pieces'])
for r in found[:40]: print(f'   {r["pieces"]} pieces, types {r["counts"]}, bounded by planes {r["planes"]} signs {r["signs"]}')
json.dump(found, open(os.path.join(HERE, '../data/convex4.json'), 'w'), indent=1)
print('FINAL ok' if tested > 0 and any(r['pieces'] == len(cells) // 2 for r in found) else 'FINAL FAIL (no half of P4 found: halves are Dehn zero by central symmetry)')
