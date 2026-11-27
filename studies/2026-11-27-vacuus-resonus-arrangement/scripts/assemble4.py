"""Step 3d (27 Nov 2026): do the Dehn-zero convex solids of step 3c fill space? With Claude (Anthropic).
Test: copies of the solid under symmetries of P4 that fit together into P4 exactly (images pairwise disjoint as cell sets and covering
all 248 cells): then the solid tiles space, since P4 does (truncated octahedra on the bcc lattice). Exact cover over the 48 images."""
import os, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'pieces4.py')).read(); exec(src[:src.index('types = []')])
cells = list(signs); C = json.load(open(os.path.join(HERE, '../data/convex4.json'))); out = []
for r in C:
    S = frozenset(c for c in cells if all(c[p] == s for p, s in zip(r['planes'], r['signs'])))
    imgs = {}
    for g in G:
        im = frozenset(act_sign(g, c) for c in S); imgs.setdefault(im, g)
    k = len(cells) // len(S); found = None
    ims = list(imgs)
    def rec(chosen, used):
        global found
        if found: return
        if len(chosen) == k:
            if len(used) == len(cells): found = list(chosen)
            return
        rest = [c for c in cells if c not in used]; first = rest[0]
        for im in ims:
            if first in im and not (im & used): rec(chosen + [im], used | im)
    rec([], frozenset())
    out.append(dict(pieces=len(S), copies=k, planes=r['planes'], signs=r['signs'], fills_P4=found is not None))
    print(f'{len(S)} pieces (1/{k} of P4), planes {r["planes"]}: {k} symmetric copies fill P4 exactly: {found is not None}', flush=True)
json.dump(out, open(os.path.join(HERE, '../data/assemble4.json'), 'w'), indent=1)
print('FINAL ok' if all(o['fills_P4'] for o in out) else 'FINAL ok (some do not assemble into P4: see list)')
