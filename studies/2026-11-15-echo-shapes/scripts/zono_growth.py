#!/usr/bin/env python3
"""Part C1, grown echoes (convex): DICTO's gnomon read for zonohedra = add one whole zone, i.e. Minkowski-add a segment; keeping the
symmetry means adding a whole orbit of zones at once. Growth trees:
  Ih: orbits A5 (6 five-fold axes), A3 (10 three-fold axes), A2 (15 two-fold axes); every union, unit lengths, and the golden lengths
      variant (each orbit scaled by phi^j so that all generators of the same orbit keep one length).
  Oh: orbits C4 (3), C3 (4), C2 (6).
  Golden ladder: nested subsets of the six 5-fold axes (3 -> 4 -> 5 -> 6), every subset class.
For each zonohedron: faces (exact: a plane spanned by m generators gives two 2m-gons), zone sizes, rhombic / monohedral,
translation tiling (Venkov-McMullen: a zonohedron tiles by translations iff every zone has 4 or 6 faces), Dehn invariant (zero for
every zonotope: it is a union of parallelepipeds; computed as a control), tones of the vertex set with forced/unforced zeros.
Usage: zono_growth.py out.json"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from echo_lib import *
OUT = sys.argv[1]; t0 = time.time(); FAILS = []
def check(c, msg):
    print(('CHECK ok   ' if c else 'CHECK FAIL ') + msg, flush=True)
    if not c: FAILS.append(msg)
Z = Q5(0); O1 = Q5(1)

def lines(vecs):
    """one representative per line (first nonzero coordinate positive)"""
    out = {}
    for v in vecs:
        v = tuple(q5(x) for x in v)
        s = next(x for x in v if not x.iszero()).sign()
        if s < 0: v = vscale(Q5(-1), v)
        out.setdefault(vkey(v), v)
    return list(out.values())
def cyc3(v): return [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])]
def all_signs_cyc(v): return [w for u in cyc3(v) for w in signs(u)]
ICO = all_signs_cyc((Z, O1, PHI))
A5 = lines(ICO)                                                                # 6 five-fold axes (vertices)
_E = [(a, b) for a, b in itertools.combinations(ICO, 2) if dot(vsub(a, b), vsub(a, b)) == 4]
A2 = lines([vadd(a, b) for a, b in _E])                                        # 15 two-fold axes (edge midpoints)
_F = [(a, b, c) for a, b, c in itertools.combinations(ICO, 3) if all(dot(vsub(x, y), vsub(x, y)) == 4 for x, y in ((a, b), (b, c), (a, c)))]
A3 = lines([vadd(vadd(a, b), c) for a, b, c in _F])                            # 10 three-fold axes (face centres)
C4 = lines(all_signs_cyc((O1, Z, Z))); C3 = lines(signs((O1, O1, O1))); C2 = lines(all_signs_cyc((O1, O1, Z)))
assert (len(A5), len(A3), len(A2), len(C4), len(C3), len(C2)) == (6, 10, 15, 3, 4, 6)

def cross(u, v): return (u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0])
def iszero_v(u): return all(x.iszero() for x in u)
def zonohedron(G):
    """exact face structure from generators G (list of Q5 3-vectors, pairwise non-parallel)"""
    planes = []        # list of (normal, members)
    for i, j in itertools.combinations(range(len(G)), 2):
        n = cross(G[i], G[j])
        for pl in planes:
            if iszero_v(cross(pl[0], n)): pl[1].update((i, j)); break
        else: planes.append([n, {i, j}])
    F = 2*len(planes); faces = {}
    for n, mem in planes: faces[2*len(mem)] = faces.get(2*len(mem), 0) + 2
    zone = [2*sum(1 for n, mem in planes if g in mem) for g in range(len(G))]
    E = sum(2*len(mem) for n, mem in planes); V = 2 - F + E
    # rhombus shapes: angle between the two generators (cos^2, exact) and side lengths
    shapes = set()
    for n, mem in planes:
        if len(mem) == 2:
            i, j = sorted(mem); c2 = dot(G[i], G[j])**Q5(1) if False else (dot(G[i], G[j])*dot(G[i], G[j]))/(dot(G[i], G[i])*dot(G[j], G[j]))
            shapes.add((str(c2), str(dot(G[i], G[i])), str(dot(G[j], G[j]))))
    return {'F': F, 'E': E, 'V': V, 'faces': dict(sorted(faces.items())), 'zones': len(G), 'zone_sizes': sorted(set(zone)),
            'rhombic': set(faces) == {4}, 'rhombus_shapes': len(shapes), 'planes': planes,
            'translation_tiler': all(z in (4, 6) for z in zone)}

def vertices(G):
    """vertices of sum [-g, g] (exact), by iterated Minkowski sum with hull pruning"""
    from scipy.spatial import ConvexHull
    pts = {vkey(tuple(Q5() for _ in range(3))): tuple(Q5() for _ in range(3))}
    for g in G:
        new = {}
        for p in pts.values():
            for s in (1, -1):
                q = vadd(p, vscale(Q5(s), g)); new[vkey(q)] = q
        P = list(new.values()); X = np.array([to_np(p) for p in P])
        if len(P) > 8 and np.linalg.matrix_rank(X - X.mean(0)) == 3:
            Hh = ConvexHull(X); keep = set(Hh.vertices.tolist())
            # qhull drops points on facets/edges; we keep only true vertices (zonotope vertices are hull vertices)
            P = [P[i] for i in sorted(keep)]
        pts = {vkey(p): p for p in P}
    return list(pts.values())

def study(label, G, gname):
    z = zonohedron(G); Vx = vertices(G)
    check(len(Vx) == z['V'], f'{label}: vertex count {len(Vx)} = Euler {z["V"]}')
    X = np.array([to_np(p) for p in Vx]); H = hull3(X)
    check(len(H['faces']) == z['F'], f'{label}: hull faces {len(H["faces"])} = {z["F"]}')
    Pmp = [to_mp(p) for p in Vx]
    dz = dehn(Pmp, H) if len(Vx) <= 400 else {'zero': None, 'note': 'skipped (size); zero by the parallelepiped dissection'}
    if dz['zero'] is not None: check(dz['zero'], f'{label}: Dehn invariant zero (zonotope control)')
    tr = parallelohedron(H)
    check(tr['tiles_by_translation'] == z['translation_tiler'], f'{label}: Venkov test on the hull agrees with the zone count rule')
    T_ = tones(Vx, 30); rep = tone_report(T_, gname)
    for kk in rep['unforced_zero']:
        if kk % 2 == 0:
            e = tones_exact_even(Vx, kk); check(e.iszero(), f'{label}: unforced zero T_{kk} exact')
    o, i_, n_ = sym_group(X); g2 = group_name(o, i_, n_)
    row = {k: v for k, v in z.items() if k != 'planes'}
    row.update({'label': label, 'group': g2, 'name': name_of(H), 'dehn_zero': dz['zero'], 'tones': rep,
                'T_first_nonzero': {k: float(T_[k]) for k in range(1, 21) if abs(T_[k]) > mp.mpf(10)**-40}})
    print(f'ZONO {label}: F={z["F"]} {z["faces"]} zones {z["zones"]} sizes {z["zone_sizes"]} group {g2} tiler(transl) {z["translation_tiler"]} '
          f'name {row["name"]} zeros {rep["zero"][:12]} unforced {rep["unforced_zero"]}', flush=True)
    return row

def main():
    res = {'Ih_tree': [], 'Ih_golden_lengths': [], 'Oh_tree': [], 'golden_ladder': []}
    orbs = {'A5': A5, 'A3': A3, 'A2': A2}
    names = list(orbs); steps = 0; total = 7 + 7 + 7 + 6
    for r in range(1, 4):
        for sub in itertools.combinations(names, r):
            G = [g for nm in sub for g in orbs[nm]]
            res['Ih_tree'].append(dict(study('Ih ' + '+'.join(sub), G, 'Ih'), orbits=list(sub))); steps += 1
            print(f'PROGRESS {steps/total:.3f}', flush=True)
    # golden lengths: A5 x 1, A3 x phi, A2 x phi^2 (one length per orbit; unit lengths above are the other natural choice)
    scale = {'A5': O1, 'A3': PHI, 'A2': PHI*PHI}
    for r in range(2, 4):
        for sub in itertools.combinations(names, r):
            G = [vscale(scale[nm]/(dot(g, g)), g) for nm in sub for g in orbs[nm]]
            res['Ih_golden_lengths'].append(dict(study('Ih golden-lengths ' + '+'.join(sub), G, 'Ih'), orbits=list(sub))); steps += 1
            print(f'PROGRESS {steps/total:.3f}', flush=True)
    oorbs = {'C4': C4, 'C3': C3, 'C2': C2}
    for r in range(1, 4):
        for sub in itertools.combinations(list(oorbs), r):
            G = [g for nm in sub for g in oorbs[nm]]
            res['Oh_tree'].append(dict(study('Oh ' + '+'.join(sub), G, 'Oh'), orbits=list(sub))); steps += 1
            print(f'PROGRESS {steps/total:.3f}', flush=True)
    # golden ladder: subsets of the six 5-fold axes up to the 120 symmetries (classes by sorted Gram data)
    seen = {}
    for r in range(3, 7):
        for sub in itertools.combinations(range(6), r):
            G = [A5[i] for i in sub]
            gram = tuple(sorted(dot(G[i], G[j]).sign() for i, j in itertools.combinations(range(r), 2)))
            # invariant up to sign flips of generators: the multiset of triple products' signs
            trip = tuple(sorted((dot(G[i], G[j])*dot(G[j], G[k])*dot(G[i], G[k])).sign() for i, j, k in itertools.combinations(range(r), 3)))
            key = (r, trip)
            seen.setdefault(key, sub)
    for (r, trip), sub in sorted(seen.items()):
        G = [A5[i] for i in sub]
        gname = {6: 'Ih'}.get(r, 'Ih')
        z = zonohedron(G); Vx = vertices(G); X = np.array([to_np(p) for p in Vx]); H = hull3(X)
        o, i_, n_ = sym_group(X); T_ = tones(Vx, 30)
        row = {k: v for k, v in z.items() if k != 'planes'}; row.update({'axes': list(sub), 'name': name_of(H), 'group_order': o,
              'inversion': i_, 'tone_zeros': [k for k in range(1, 31) if abs(T_[k]) < mp.mpf(10)**-40]})
        res['golden_ladder'].append(row)
        print(f'GOLDEN {r} axes {sub}: F={z["F"]} {z["faces"]} zone sizes {z["zone_sizes"]} shapes {z["rhombus_shapes"]} '
              f'name {row["name"]} |G|={o} tiler(transl) {z["translation_tiler"]}', flush=True)
    steps += 6; print(f'PROGRESS {min(1, steps/total):.3f}', flush=True)
    # controls
    tri = [r for r in res['Ih_tree'] if r['orbits'] == ['A5']][0]
    check(tri['F'] == 30 and tri['rhombic'] and tri['zone_sizes'] == [10], 'control: A5 gives the rhombic triacontahedron (30 rhombi, zones of 10)')
    gi = [r for r in res['Ih_tree'] if r['orbits'] == ['A2']][0]
    check(gi['faces'] == {4: 30, 6: 20, 10: 12}, 'control: A2 gives the truncated icosidodecahedron type (30 squares, 20 hexagons, 12 decagons)')
    to = [r for r in res['Oh_tree'] if r['orbits'] == ['C2']][0]
    check(to['translation_tiler'] and to['F'] == 14, 'control: C2 (6 face diagonals) gives the truncated octahedron type, a translation tiler')
    rd = [r for r in res['Oh_tree'] if r['orbits'] == ['C3']][0]
    check(rd['F'] == 12 and rd['translation_tiler'], 'control: C3 gives the rhombic dodecahedron, a translation tiler')
    json.dump({**res, 'fails': FAILS, 'seconds': time.time() - t0}, open(OUT, 'w'), indent=1, default=str)
    print(f'{len(FAILS)} failed checks, {time.time() - t0:.0f} s'); print('FINAL ok' if not FAILS else 'FINAL FAIL')

if __name__ == '__main__': main()
