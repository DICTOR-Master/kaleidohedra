"""Which symmetries does the floating-resin state keep, and which faces change? (27 Nov 2026). With Claude (Anthropic).
A symmetry g of T_h is kept when the pairing commutes with it: sigma(g F) = g sigma(F) for every face F."""
import os, sys, json
from collections import Counter
import numpy as np
argv = list(sys.argv); sys.argv = sys.argv[:1]
import amber_aequus as A
sys.argv = argv
HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, '../data/c116/pairing.json'))); gface, S = d['gface'], [np.array(m) for m in d['S']]
Dm = A.build("aequus-377"); M = np.array([[float(x) for x in u] for u, c in Dm["planes"]]); M /= np.linalg.norm(M, axis=1)[:, None]
Mg = [[int(np.argmax(M @ (S[g] @ M[t]))) for t in range(60)] for g in range(24)]
cs = [len(f) for f in d['faces']]; ms = [len(f) for f in d['minana_faces']]
res = {}
for name, f in (('enumeration best (144)', 'onefloor.json'), ('floating resin (156)', 'onefloor_float.json')):
    sig = {int(k): int(v) for k, v in json.load(open(os.path.join(HERE, '../data/c116/' + f)))['pairing'].items()}
    keep = [g for g in range(24) if all(sig[gface[g][k]] == Mg[g][sig[k]] for k in range(60))]
    res[f] = len(keep)
    dets = Counter(int(round(np.linalg.det(S[g]))) for g in keep)
    print(f'{name}: symmetries kept {len(keep)} of 24 (rotations {dets[1]}, mirror-type {dets[-1]}); changes',
          sorted(Counter(f"{cs[k]}->{ms[sig[k]]}" for k in range(60)).items()), flush=True)
print('FINAL ok' if res.get('onefloor.json') == 24 else 'FINAL FAIL (control: the symmetric pairing must keep all 24)')
