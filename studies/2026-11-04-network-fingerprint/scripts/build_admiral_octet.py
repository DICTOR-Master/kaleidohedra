#!/usr/bin/env python3
"""Full 3D Admiral Cap network: the octet (vertices = even-sum points of Z^3, edge sqrt2; tetrahedra on unit cubes' even corners,
octahedra |x-c|_1 <= 1 at odd-sum c), each octahedron = a Pacioli icosahedron (corners on its 12 edges, divided in the golden ratio)
+ six Admiral Caps (hull of an octahedron corner and the 4 icosahedron corners on its edges) [#47; edgeRoof.js].
Twin choice per octahedron: cyclic order (0, a, b) or (0, b, a) with a = 1/phi^2, b = 1/phi (the two pyritohedral twins).
mode 'same': all octahedra the same twin; 'alt': twin by parity of (c_x - 1)/... (checkerboard of the octahedra's simple cubic sublattices).
Writes data/admiral-octet-<mode>-pieces.json as [{kind, V}]. Scale: multiply by phi^2/2 for icosahedron edge 1 (not needed for fingerprints)."""
import itertools, json, os, sys
import numpy as np
phi = (1 + 5**.5)/2; a, b = 1/phi**2, 1/phi
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
mode = sys.argv[1] if len(sys.argv) > 1 else 'same'
R = 3
def ico(order):
    p, q = (a, b) if order == 0 else (b, a)
    out = []
    for k in range(3):
        for s1, s2 in itertools.product((1, -1), repeat=2):
            v = [0, 0, 0]; v[(k+1) % 3] = s1*p; v[(k+2) % 3] = s2*q; out.append(v)
    return np.array(out, float)
pieces = []
for c in itertools.product(range(-R, R+1), repeat=3):
    c = np.array(c)
    if c.sum() % 2 == 0: continue
    odd = tuple(int(x) % 2 for x in c)
    order = 0 if mode == 'same' else ((int(c.sum()) - 1)//2) % 2   # 'alt': twins alternate layer by layer along (1,1,1)
    I = ico(order) + c
    pieces.append({'kind': 'I', 'V': I.tolist()})
    for i in range(3):
        for s in (1, -1):
            e = np.zeros(3); e[i] = s; corner = c + e
            near = [v for v in I if abs(np.abs(v - c).sum() - 1) < 1e-9 and abs((v - c) @ e) > 1e-9 and np.sign((v - c) @ e) == s]
            # the Admiral Cap is NOT convex: two tetrahedra over the icosahedron edge among the 4 points (edgeRoof.js)
            pr = [(i1, i2) for i1, i2 in itertools.combinations(range(4), 2) if abs(np.linalg.norm(near[i1] - near[i2]) - 2*a) < 1e-9 and abs((near[i1] - near[i2]) @ e) < 1e-9]
            assert len(pr) == 1, pr
            e0, e1 = near[pr[0][0]], near[pr[0][1]]
            for k in range(4):
                if k not in pr[0]: pieces.append({'kind': 'A', 'V': [corner.tolist(), e0.tolist(), e1.tolist(), near[k].tolist()]})
for lo in itertools.product(range(-R, R), repeat=3):
    cs = [np.array(lo) + np.array(d) for d in itertools.product((0, 1), repeat=3)]
    pieces.append({'kind': 'T', 'V': [x.tolist() for x in cs if x.sum() % 2 == 0]})
ok = all(len(p['V']) == 4 for p in pieces if p['kind'] == 'A')
print(mode, {k: sum(1 for p in pieces if p['kind'] == k) for k in 'IAT'}, 'cap halves (tetrahedra):', ok)
json.dump(pieces, open(os.path.join(D, f'admiral-octet-{mode}-pieces.json'), 'w'))
