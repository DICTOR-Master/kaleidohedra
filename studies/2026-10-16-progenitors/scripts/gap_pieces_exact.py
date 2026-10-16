# Exact volumes of the gap layers (one kind of piece each, so each piece is the layer / its count): RT -> G (30) and G -> I·φ³ (60),
# in Q(√5); with the float edge lengths of each piece from data/gap-pieces.json. -> data/gap-pieces-exact.txt
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
import json
S = dict(C); RT = S['RT']; IP = S['I·φ³']
sq = lambda v: dot(v, v); RI2 = max((sq(v) for v in RT), key=lambda q: q.f())
fc = [[sum((IP[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)] for idx in planes(IP)]
G = [v for v in RT if sq(v) == RI2] + fc
vol = lambda V: volume(V, np.array([[x.f() for x in v] for v in V]))
vRT, vG, vI = vol(RT), vol(G), vol(IP)
out = ['DICTO · dictospheres.com', 'Gap layers, exact (Q(√5))',
       f'  vol RT = {vRT!r};  vol G = {vG!r};  vol I·φ³ = {vI!r}',
       f'  RT -> G: 30 pieces of {(vG - vRT) / 30!r} = {((vG - vRT) / 30).f():.9f} each',
       f'  G -> I·φ³: 60 pieces of {(vI - vG) / 60!r} = {((vI - vG) / 60).f():.9f} each',
       f'  share of the step RT -> I·φ³ taken by G: {((vG - vRT) / (vI - vRT)).f():.6f} of the volume']
P = json.load(open('data/gap-pieces.json'))
for layer, pcs in (P.items() if isinstance(P, dict) else []):
    V = np.array(pcs[0]['v'] if isinstance(pcs[0], dict) else pcs[0]); h = ConvexHull(V); E = set()
    for t in h.simplices:
        for a, b in ((t[0], t[1]), (t[1], t[2]), (t[0], t[2])): E.add((min(a, b), max(a, b)))
    L = sorted({round(float(np.linalg.norm(V[a] - V[b])), 6) for a, b in E})
    out.append(f'  {layer}: edge lengths in one piece (float, incl. diagonals of flat faces): {L}')
print('\n'.join(out)); open('data/gap-pieces-exact.txt', 'w').write('\n'.join(out) + '\n')
