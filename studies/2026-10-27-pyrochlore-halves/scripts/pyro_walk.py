# Pyrochlore Halves, exact (DICTO 2026-10-27): #57's census engine (k-research studies/2026-10-25-stackings/scripts), unchanged, on the
# diamond-type stacking: per gap k (layers X, Y; third letter Z) the ball S over X at 0, the diamond atom C over X at 3/4, the
# octahedral hole O over Z at 1/2, the tetrahedral hole Y over Y at 1/4. Kinds: 'atom' (S, C) weight lam, 'hole' (O, Y) weight 0.
# Exact rational arithmetic in the lattice basis. Usage: python pyro_walk.py ABC AB ABAC ABCACB
import sys, json, os
E57 = os.path.expanduser('~/kres-tmp/st57/scripts'); sys.path.insert(0, E57); os.chdir(E57)
from fractions import Fraction as Fr
import networks, census
from networks import NETS
POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
def net_for(word):
    n = len(word); motif = []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
        z = lambda f: Fr(k, n) + f / n
        motif += [('atom', (*POS[X], z(Fr(0)))), ('atom', (*POS[X], z(Fr(3, 4)))), ('hole', (*POS[Z], z(Fr(1, 2)))), ('hole', (*POS[Y], z(Fr(1, 4))))]
    G = [[1, Fr(1, 2), 0], [Fr(1, 2), 1, 0], [0, 0, Fr(2, 3) * n * n]]
    return dict(name=f"pyrochlore stacking {word}", G=G, T=[(1, 0, 0), (0, 1, 0), (0, 0, 1)], motif=motif,
                w={"atom": (0, 1), "hole": (0, 0)}, A="atom", B="hole", D2=12, units="ball spacing 1; lam = w_atom - w_hole", expect=[])
if __name__ == '__main__':
    out = {}
    for word in sys.argv[1:]:
        key = 'py_' + word; NETS[key] = net_for(word); census.NETS[key] = NETS[key]
        C = census.Census(key); d = C.walk(); out[word] = d
        print(f'== {word}: {len(d["intervals"])} intervals, stops at ' + ', '.join(s['lam'] for s in d['stops']), flush=True)
        for s in d['stops']:
            seen = {}
            for x in s['sites']:
                sig = 'vanished' if x.get('vanished') else f"{x['corners']} corners, faces {sorted(x['face_sizes'])}"
                seen[(x['kind'], sig)] = seen.get((x['kind'], sig), 0) + 1
            for (k, sig), c in seen.items(): print(f'   {s["lam"]:>8}  {c} x {k}: {sig}', flush=True)
    json.dump(out, open(os.path.expanduser('~/kres-tmp/pyro/pyro_walk.json'), 'w'), indent=1, default=str)
