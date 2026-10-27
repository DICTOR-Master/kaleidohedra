# Five pyramids study, question 1 (DICTO, 2026-10-27): exact face shapes and dihedral angles of the five Platonic face
# pyramids, exact face-congruence tests between different pyramids, and every edge star (dihedral angles adding to 360
# degrees round one edge) that the five pyramids can make. Run on dicto-big-brother.
import itertools, json, sys
import sympy as sp
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from pieces import build

def dihedrals(P):
    """Exact interior dihedral angle (as cos, and a reflex flag) along every edge of piece P."""
    V, F = P['V'], P['F']; out = {}
    nrm = [(V[f[1]] - V[f[0]]).cross(V[f[2]] - V[f[0]]) for f in F]
    for i, f in enumerate(F):
        for k in range(len(f)):
            u, v = f[k], f[(k + 1) % len(f)]
            for j, g in enumerate(F):
                if j != i and any(g[m] == v and g[(m + 1) % len(g)] == u for m in range(len(g))):
                    c = sp.radsimp(-(nrm[i].T * nrm[j])[0] / sp.sqrt((nrm[i].T * nrm[i])[0] * (nrm[j].T * nrm[j])[0]))
                    w = next(x for x in g if x not in (u, v))
                    reflex = sp.simplify((nrm[i].T * (V[w] - V[u]))[0]) > 0
                    out[tuple(sorted((u, v)))] = (sp.nsimplify(sp.simplify(c)), bool(reflex))
    return out

def L2(a, b): return sp.radsimp(sp.expand(((a - b).T * (a - b))[0]))

def run():
    L = build(); rep = {}
    names = {'C': 'Cube face pyramid', 'T': 'Q (tetrahedron face pyramid)', 'O': 'Octahedron face pyramid',
             'D': 'Dodecahedron face pyramid', 'I': 'Cleo-Icos'}
    apexcos = {}
    for key, nm in names.items():
        P = L[nm]; V = P['V']; apex = len(V) - 1   # the centre is the last vertex in every pyramid here
        dh = dihedrals(P); base = [e for e in dh if apex not in e]; side = [e for e in dh if apex in e]
        cb = {dh[e][0] for e in base}; cs = {dh[e][0] for e in side}
        lat = [f for f in P['F'] if apex in f]; bf = [f for f in P['F'] if apex not in f][0]
        f = lat[0]; i = f.index(apex); p, q = f[(i + 1) % 3], f[(i + 2) % 3]
        s, r = L2(V[p], V[q]), L2(V[apex], V[p])           # squared base edge, squared side edge
        ca = sp.radsimp(1 - s / (2 * r))                  # cos of the lateral face's apex angle (law of cosines)
        apexcos[key] = (sp.nsimplify(sp.simplify(ca)), sp.radsimp(r / s))
        rep[key] = dict(piece=nm, base=f'{len(bf)}-gon (regular)', lateral=f'isosceles, side/base = sqrt({sp.simplify(r / s)})',
                        lateral_apex_angle_cos=str(apexcos[key][0]), lateral_apex_angle_deg=float(sp.acos(apexcos[key][0]) * 180 / sp.pi),
                        base_edge_dihedral_cos=[str(c) for c in cb], base_edge_dihedral_deg=[float(sp.acos(c) * 180 / sp.pi) for c in cb],
                        side_edge_dihedral_cos=[str(c) for c in cs], side_edge_dihedral_deg=[float(sp.acos(c) * 180 / sp.pi) for c in cs])
        print(key, rep[key])
    # lateral faces of different pyramids are never congruent at any scale: their apex angles differ (exact cosines)
    pairs = []
    for a, b in itertools.combinations(names, 2):
        same = sp.simplify(apexcos[a][0] - apexcos[b][0]) == 0
        pairs.append(dict(pair=a + b, lateral_faces_similar=bool(same)))
    print('lateral similarity between kinds:', pairs)
    assert not any(p['lateral_faces_similar'] for p in pairs)
    # lateral faces are never equilateral (side/base != 1), so a lateral face can only meet a lateral face of the same kind
    assert all(sp.simplify(apexcos[k][1] - 1) != 0 for k in names)
    # base faces: squares (C) and pentagons (D) only match their own kind; triangles of T, O, I match each other at equal edge
    # edge stars: every multiset of the ten dihedral angles adding to 2 pi (float screen with a 1e-6 margin; each hit is
    # exact because the base angles enter only as alpha/2, (pi-alpha)/2, thetaD/2, thetaI/2, which by #44 Lemma 2 are
    # Q-independent of pi apart from alpha/2 + (pi-alpha)/2 = pi/2, and all side angles are rational multiples of pi)
    ang = {}
    for k in names:
        ang[k + ' base'] = rep[k]['base_edge_dihedral_deg'][0]; ang[k + ' side'] = rep[k]['side_edge_dihedral_deg'][0]
    keys = list(ang); stars = []
    def rec(i, left, cur):
        if abs(left) < 1e-6: stars.append(dict(cur)); return
        if i == len(keys) or left < 0: return
        k = keys[i]; n = 0
        while n * ang[k] <= left + 1e-6:
            if n: cur[k] = n
            rec(i + 1, left - n * ang[k], cur); n += 1
        cur.pop(k, None)
    rec(0, 360.0, {})
    mixed = [s for s in stars if len({k.split()[0] for k in s}) > 1]
    print(len(stars), 'edge stars;', len(mixed), 'use two or more kinds')
    for s in mixed: print('  ', s)
    json.dump(dict(pyramids=rep, lateral_pairs=pairs, edge_stars=stars, mixed_edge_stars=mixed), open('data/q1-pyramids.json', 'w'), indent=1)

if __name__ == '__main__':
    run()
