exec(open("scripts/bridge.py").read().split("FAM = {")[0])
fam = lambda m: [(n, 1.0) for n in CUBE] + [(n, 2.0) for n in OCT] + [(n, m) for n in RDN]
for m in (1.2, 1.4, 1.5, 1.6, 5/3, 1.7, 1.8, 1.9):
    P = solid(fam(m)); h = ConvexHull(P); X, F = hull_faces(P[h.vertices]); d = dehn(X, F)
    print('mu=%.4f corners %d zero=%s sums=%s' % (m, len(X), d['dehn_zero'], {k: round(v, 6) for k, v in d['coefficient_sums_over_maxL'].items()}))
