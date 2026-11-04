import sys, json, numpy as np
sys.argv = sys.argv[:1] + ['x', '8', '300']
exec(open('scripts/dehn.py').read().split("if __name__")[0])
D = json.load(open('data/admiral-network-pieces.json')); seen = {}
for p in D:
    if p['kind'] in seen: continue
    P = np.unique(np.round(np.array([v for f in p['faces'] for v in f]), 9), axis=0)
    X, F = hull_faces(P); r = dehn(X, F, p['kind']); seen[p['kind']] = r
    print(p['kind'], len(X), 'corners; zero =', r['dehn_zero'], {k: round(v, 6) for k, v in r['coefficient_sums_over_maxL'].items()})
json.dump(seen, open('data/admiral-dehn.json', 'w'), indent=1, ensure_ascii=False)
