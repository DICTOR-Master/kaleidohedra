# DICTO 2026-10-18 octet study -- STEP 24c: each wedge (non-convex, step 24b) is two convex tetrahedra A and B (step 24). Their exact faces,
# edge lengths (squared, exact) and named angles; are A and B golden?
import math
exec(open('step24b_wedge.py').read().split('out = []')[0])
S = load('step24-outer-corner.json'); seen = {}
for piece, info in zip(S['pieces'], S['checks']['below_pieces']):
    if info['volume'] in seen: continue
    C = [[q(x) for x in p] for p in piece]; F = []
    for i in range(4):
        X = [C[j] for j in range(4) if j != i]
        F.append(dict(edges2=[qs_(dot(vsub(X[(k + 1) % 3], X[k]), vsub(X[(k + 1) % 3], X[k]))) for k in range(3)],
                      edges=[round(qf(dot(vsub(X[(k + 1) % 3], X[k]), vsub(X[(k + 1) % 3], X[k]))) ** .5, 5) for k in range(3)],
                      angles=[ang(vsub(X[k - 1], X[k]), vsub(X[(k + 1) % 3], X[k])) for k in range(3)]))
    seen[info['volume']] = dict(volume=info['volume'], volume_float=info['float'], faces=F)
for k, v in seen.items():
    print('tetra', v['volume'], round(v['volume_float'], 7))
    for f in v['faces']: print('   ', f['edges'], f['angles'])
save('step24c-tetra.json', dict(mark=MARK, step='24c', tetrahedra=list(seen.values())))
