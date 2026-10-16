# The chain RT ⊂ G ⊂ I·φ³ (G = the gap member, scripts/gap_member.py) as full-precision float corners of the exact stations, for
# ../2026-10-16-polar-dharma/scripts/polar_pieces.py (one piece per face of the inner solid: cone(F) ∩ outer ∩ beyond F). -> data/gap-chain.json
exec(open('scripts/core_hull_in_cycle.py').read().split("S = dict(C)")[0])
import json
S = dict(C); RT = S['RT']; IP = S['I·φ³']
sq = lambda v: dot(v, v); RI2 = max((sq(v) for v in RT), key=lambda q: q.f())
fc = [[sum((IP[i][k] for i in idx), Q(0)) / len(idx) for k in range(3)] for idx in planes(IP)]
G = [v for v in RT if sq(v) == RI2] + fc
fl = lambda V: [[x.f() for x in v] for v in V]
# 'icosahedron' is the name polar_pieces.py reads its symmetry frame from (this is I·φ³)
json.dump([['RT', fl(RT)], ['G', fl(G)], ['icosahedron', fl(IP)]], open('data/gap-chain.json', 'w'))
print('RT', len(RT), 'G', len(G), 'I·φ³', len(IP))
