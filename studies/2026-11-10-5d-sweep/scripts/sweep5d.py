"""The 5D test (DICTO 10 Nov: "yes queue the 5D test"; "can we use it to predict other unperceived elements of the higher dimensions").
For a simple 5-polytope and a generic height, sweeping a hyperplane: the slice is a 4-polytope tiled on its surface by the facets'
cross-sections; two facets touch in the slice iff their common ridge (3-face) crosses the hyperplane. PREDICTION (the corner argument one
dimension up): at a corner with i edges down: i = 1 a facet is born, i = 2 one contact is gained (nothing lost), i = 3 one contact is lost,
i = 4 a facet dies; counts h1 .. h4 in every generic direction. Polytopes: the 5-cube, h = (1, 5, 10, 10, 5, 1); the 5D permutohedron
(orderings of 1..6), h = Eulerian numbers (1, 57, 302, 302, 57, 1); control: the 4D permutohedron, h = (1, 26, 66, 26, 1), whose sweep must
show pure scutoid swaps. Three random directions each."""
import itertools, numpy as np
from collections import Counter
from scipy.spatial import ConvexHull
def frame(P):                                             # coordinates in the affine hull
    c = P.mean(0); U, S, Vt = np.linalg.svd(P - c); k = int((S > 1e-9).sum()); return (P - c) @ Vt[:k].T
def analyse(name, P, predicted, facets=None):
    X = frame(np.array(P, float)); d = X.shape[1]
    if facets is None:
        h = ConvexHull(X); F = {}
        for simp, eq in zip(h.simplices, h.equations): F.setdefault(tuple(np.round(eq, 7)), set()).update(simp)
        facets = [frozenset(v) for v in F.values()]
    else: facets = [frozenset(f) for f in facets]
    per = Counter(); [per.update(f) for f in facets]
    assert set(per.values()) == {d}, f'{name} not simple: {Counter(per.values())}'
    ridges = {}
    for a, b in itertools.combinations(range(len(facets)), 2):
        sh = facets[a] & facets[b]
        if len(sh) >= d - 1: ridges[(a, b)] = sorted(sh)      # two facets of a convex polytope sharing >= d - 1 corners share a ridge (no float rank test: thin ridges)
    rng = np.random.default_rng(11); out = []
    for t in range(3):
        u = rng.normal(size=d); u /= np.linalg.norm(u); H = X @ u; hs = np.sort(H)
        assert np.min(np.diff(hs)) > 1e-9, 'not generic'
        def state(z):
            alive = {i for i, f in enumerate(facets) if H[list(f)].min() < z < H[list(f)].max()}
            touch = {k for k, r in ridges.items() if H[r].min() < z < H[r].max()}
            return alive, touch
        C = Counter(); prev = state((hs[0] + hs[1]) / 2)
        for k in range(1, len(hs) - 1):
            cur = state((hs[k] + hs[k + 1]) / 2)
            born, died = len(cur[0] - prev[0]), len(prev[0] - cur[0])
            lost = len({e for e in prev[1] - cur[1] if e[0] in cur[0] and e[1] in cur[0]}); gained = len({e for e in cur[1] - prev[1] if e[0] in prev[0] and e[1] in prev[0]})
            if born: C['facet born'] += born
            if died: C['facet dies'] += died
            if (lost, gained) != (0, 0) and not born and not died: C[f'{lost} lost / {gained} gained'] += 1
            prev = cur
        out.append(dict(C)); print(f'  {name} direction {t + 1}: {dict(sorted(C.items()))}', flush=True)
    ok = all(o == out[0] for o in out) and all(out[0].get(k, 0) == v for k, v in predicted.items())
    print(f'{name}: {len(X)} corners, {len(facets)} facets, simple; predicted {predicted}: {"MATCH in all 3 directions" if ok else "MISMATCH"}', flush=True)
    return ok
print('START the 5D test', flush=True)
cube = list(itertools.product([0, 1], repeat=5))
perm6 = list(itertools.permutations(range(1, 7)))
perm5 = list(itertools.permutations(range(1, 6)))
r = [analyse('4D permutohedron (control)', perm5, {'facet born': 26, '1 lost / 1 gained': 66, 'facet dies': 26}),
     analyse('5-cube', cube, {'facet born': 5, '0 lost / 1 gained': 10, '1 lost / 0 gained': 10, 'facet dies': 5}),
     analyse('5D permutohedron', perm6, {'facet born': 57, '0 lost / 1 gained': 302, '1 lost / 0 gained': 302, 'facet dies': 57})]
print('FINAL ok' if all(r) else 'FINAL FAIL: a prediction failed')
