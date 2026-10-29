# Lead 1 (DICTO 2026-10-25, "lets go with 1"): the weight walk on the octahedral + tetrahedral holes of close packings with other
# stackings. A stacking is a periodic word in A, B, C (no letter twice in a row); ball spacing 1, layer spacing d = √(2/3).
# Between layers X (height z) and Y (z + d): an octahedral hole over the third position Z at z + d/2, a tetrahedral hole over X at
# z + 3d/4 and one over Y at z + d/4 (the census hcp motif is the case AB). Weights w_oct = 0, w_tet = λ, as in the census.
# Checks: ABC must give the cubic octet's walk (stops −1/8, 3/8: octahedra+tetrahedra, then cubes) and AB the twinned one
# (−11/24, −1/8, 5/24, 3/8). Usage: python stackings.py ABC AB ABAC ABCACB ...
import sys, json
from fractions import Fraction as Fr
import networks
from networks import NETS
POS = {'A': (Fr(0), Fr(0)), 'B': (Fr(1, 3), Fr(1, 3)), 'C': (Fr(2, 3), Fr(2, 3))}
def net_for(word):
    n = len(word); assert all(word[i] != word[(i + 1) % n] for i in range(n)), word
    motif = []
    for k in range(n):
        X, Y = word[k], word[(k + 1) % n]; Z = ({'A', 'B', 'C'} - {X, Y}).pop()
        z = lambda f: Fr(k, n) + f / n            # fraction of the cell height
        motif += [('oct', (*POS[Z], z(Fr(1, 2)))), ('tet', (*POS[X], z(Fr(3, 4)))), ('tet', (*POS[Y], z(Fr(1, 4))))]
    G = [[1, Fr(1, 2), 0], [Fr(1, 2), 1, 0], [0, 0, Fr(2, 3) * n * n]]
    return dict(name=f"stacking {word} (holes of close packing)", G=G, T=[(1, 0, 0), (0, 1, 0), (0, 0, 1)], motif=motif,
                w={"tet": (0, 1), "oct": (0, 0)}, A="tet", B="oct", D2=12, units="ball spacing 1; lam = w_tet - w_oct", expect=[])
if __name__ == '__main__':
    import census
    for word in sys.argv[1:]:
        key = 'st_' + word; NETS[key] = net_for(word); census.NETS[key] = NETS[key]
        C = census.Census(key); d = C.walk(); d['checks'] = C.checks
        json.dump(d, open(f'../data/raw/{key}.json', 'w'), indent=1, default=str)
        print(f'== {word}: {len(d["intervals"])} intervals, stops at ' + ', '.join(s['lam'] for s in d['stops']), flush=True)
        for s in d['stops']:
            seen = {}
            for x in s['sites']:
                sig = 'vanished' if x.get('vanished') else f"{x['corners']} corners, faces {sorted(x['face_sizes'])}, bonds {x['bonds']}"
                seen.setdefault((x['kind'], sig), 0); seen[(x['kind'], sig)] += 1
            for (k, sig), c in seen.items(): print(f'   {s["lam"]:>7}  {c} x {k}: {sig}', flush=True)
