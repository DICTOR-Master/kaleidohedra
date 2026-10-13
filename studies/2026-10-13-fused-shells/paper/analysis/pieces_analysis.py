# Piece forms of DICTO's Chain of Karma, Spheres of Dharma and Bodhi Seed (paper "Capturing the In-betweens", 2026-10-13).
# For every piece type (one representative per role per view, deduplicated by congruence): corners, edges, faces (with
# side lengths), dihedral angles, volume, symmetry group order (proper / with reflections), chirality, a structural class,
# and a closed-form guess in Q(sqrt5) for squared lengths and dihedral cosines (fitted to 1e-6; a guess, not a proof).
# Input: ../../pieces.json. Output: pieces-analysis.json (+ printed table). DICTO · dictospheres.com
import json, os, itertools, math
import numpy as np
from scipy.spatial import ConvexHull
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, '..', '..', 'pieces.json')))
S5 = math.sqrt(5); PHI = (1 + S5) / 2

def q5(x, tol=3e-5):
    """x ~ (a + b*sqrt5)/c with small integers; returns string or None."""
    best = None
    for c in (1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36):
        for b in range(-12, 13):
            a = round(x * c - b * S5)
            if abs((a + b * S5) / c - x) < tol:
                g = math.gcd(math.gcd(abs(a), abs(b)), c)
                cand = (abs(b) + c, a // g, b // g, c // g)
                if best is None or cand < best: best = cand
        if best: break
    if not best: return None
    _, a, b, c = best
    if a == 0 and b == 0 and abs(x) > 1e-3: return None
    s = f"{a}" if b == 0 else (f"{a} {'+' if b > 0 else '-'} {abs(b)}√5" if a else f"{b}√5")
    return s if c == 1 else f"({s})/{c}"

def cluster(xs, tol):
    out = []
    for x in sorted(xs):
        if not out or x - out[-1][-1] > tol: out.append([x])
        else: out[-1].append(x)
    return [round(sum(g) / len(g), 6) for g in out]

def mult(xs, tol):
    cs = cluster(xs, tol)
    return {f'{c:.5f}': sum(abs(x - c) < 3 * tol for x in xs) for c in cs}

def form(x, tol, name='L'):
    for k, lab in ((2, f'{name}²'), (1, name), (4, f'{name}⁴')):
        v = q5(x ** k, tol * k)
        if v: return f'{lab} = {v}'
    return None

def faces_of(V, F):
    return [list(f) for f in F]

def normal(V, f):
    c = V[f].mean(0); n = np.zeros(3)
    for i in range(len(f)): n += np.cross(V[f[i]] - c, V[f[(i + 1) % len(f)]] - c)
    return n / np.linalg.norm(n)

def analyse(V, F):
    V = np.array(V, float); c = V.mean(0)
    # orient faces outward (pieces are convex: check)
    hull = ConvexHull(V); vol = hull.volume
    F2 = []
    for f in F:
        n = normal(V, f)
        if n @ (V[f].mean(0) - c) < 0: f = f[::-1]
        F2.append(f)
    F = F2
    edges = {}
    for fi, f in enumerate(F):
        for i in range(len(f)):
            e = tuple(sorted((f[i], f[(i + 1) % len(f)])))
            edges.setdefault(e, []).append(fi)
    dih = []
    for e, fs in edges.items():
        if len(fs) != 2: return None
        n1, n2 = normal(V, F[fs[0]]), normal(V, F[fs[1]])
        dih.append(math.degrees(math.pi - math.acos(max(-1, min(1, n1 @ n2)))))
    L = [float(np.linalg.norm(V[a] - V[b])) for a, b in edges]
    # convex? every vertex on hull and every face on a hull plane
    convex = abs(vol - poly_volume(V, F)) < 1e-4 * vol
    sym, sym_proper = symmetry(V)
    return dict(corners=len(V), edges=len(edges), faces=len(F), euler=len(V) - len(edges) + len(F),
                faceTypes=sorted(len(f) for f in F), volume=poly_volume(V, F), convex=convex,
                edgeLengths=cluster(L, 1e-4), dihedrals=cluster(dih, 0.01), edgeMult=mult(L, 1e-4),
                symmetryOrder=sym, properRotations=sym_proper, chiral=(sym == sym_proper),
                faceSides=sorted(tuple(sorted(round(float(np.linalg.norm(V[f[i]] - V[f[(i + 1) % len(f)]])), 4) for i in range(len(f)))) for f in F),
                V=V, F=F, edgesMap=edges)

def poly_volume(V, F):
    return float(sum(np.dot(V[f[0]], np.cross(V[f[m]], V[f[m + 1]])) for f in F for m in range(1, len(f) - 1)) / 6)

def symmetry(V):
    P = V - V.mean(0)
    D = np.linalg.norm(P[:, None] - P[None], axis=2)
    n = len(P)
    # reference triple: three non-collinear points
    for i0, i1, i2 in itertools.combinations(range(n), 3):
        if np.linalg.norm(np.cross(P[i1] - P[i0], P[i2] - P[i0])) > 1e-3: break
    A = np.array([P[i0], P[i1], P[i2]])
    count = proper = 0
    for a, b, cc in itertools.permutations(range(n), 3):
        if abs(D[a, b] - D[i0, i1]) > 1e-4 or abs(D[a, cc] - D[i0, i2]) > 1e-4 or abs(D[b, cc] - D[i1, i2]) > 1e-4: continue
        if abs(np.linalg.norm(P[a]) - np.linalg.norm(P[i0])) > 1e-4: continue
        B = np.array([P[a], P[b], P[cc]])
        # solve R with R A_i = B_i (A has rank 3 about the centroid unless the triple spans a plane through it)
        Aext = np.vstack([A, np.cross(A[1] - A[0], A[2] - A[0])])
        for sgn in (1, -1):
            Bext = np.vstack([B, sgn * np.cross(B[1] - B[0], B[2] - B[0])])
            R, *_ = np.linalg.lstsq(Aext, Bext, rcond=None); R = R.T
            if not np.allclose(R @ R.T, np.eye(3), atol=1e-4): continue
            Q = P @ R.T
            if all(np.min(np.linalg.norm(P - q, axis=1)) < 1e-4 for q in Q):
                count += 1; proper += int(np.linalg.det(R) > 0)
    return count, proper

def classify(a):
    ft = a['faceTypes']; n = a['corners']
    V, F = a['V'], a['F']
    if n == 4:
        L = a['edgeLengths']
        # opposite edges equal pairwise -> disphenoid
        pairs = [((0, 1), (2, 3)), ((0, 2), (1, 3)), ((0, 3), (1, 2))]
        d = lambda i, j: np.linalg.norm(V[i] - V[j])
        eq = [abs(d(*p) - d(*q)) < 1e-4 for p, q in pairs]
        if len(L) == 1: return 'regular tetrahedron'
        if all(eq): return 'tetragonal or rhombic disphenoid (isosceles tetrahedron)' if len(L) <= 3 else 'disphenoid'
        return f"tetrahedron (symmetry order {a['symmetryOrder']})"
    if n == 5 and ft == [3] * 6: return 'triangular bipyramid (irregular)'
    if n == 5 and ft == [3, 3, 3, 3, 4]: return 'quadrilateral pyramid'
    # pyramid: one face containing all corners but one
    for f in F:
        if len(f) == n - 1 and len(F) == len(f) + 1: return f"{len(f)}-gonal pyramid"
    # frustum/prismatoid: two parallel faces containing all corners
    for f, g in itertools.combinations(F, 2):
        if len(f) + len(g) == n and abs(abs(normal(V, f) @ normal(V, g)) - 1) < 1e-6:
            if len(f) == len(g):
                sf = np.linalg.norm(V[f[0]] - V[f[1]]); sg = np.linalg.norm(V[g[0]] - V[g[1]])
                side = [len(x) for x in F if x is not f and x is not g]
                twist = 'twisted ' if set(side) == {3} else ''
                return f"{twist}{len(f)}-gonal {'antiprism-like ' if twist else ''}frustum (prismatoid)" if twist else f"{len(f)}-gonal frustum"
            return f"prismatoid ({len(f)}-gon and {len(g)}-gon on parallel planes)"
    return f"{n}-corner convex polyhedron" if a['convex'] else f"{n}-corner non-convex polyhedron"

def congruent(a, b):
    if a['corners'] != b['corners'] or a['faceTypes'] != b['faceTypes']: return None
    k = max(b['edgeLengths']) / max(a['edgeLengths'])
    if len(a['edgeLengths']) != len(b['edgeLengths']) or any(abs(x * k - y) > 3e-4 * max(1, y) for x, y in zip(a['edgeLengths'], b['edgeLengths'])): return None
    if abs(a['volume'] * k ** 3 - b['volume']) > 1e-3 * b['volume']: return None
    if a['dihedrals'] != b['dihedrals'] and any(abs(x - y) > 0.05 for x, y in zip(a['dihedrals'], b['dihedrals'])): return None
    return 'same' if abs(k - 1) < 1e-4 else f'x{k:.6f}'

# DICTO's names (DISCOVERIES #19/#24, the Chain of Karma Kit and the Dharma Piece Names page, 2026-10-13); '' = no name yet
NAMES = {'dharma.cycle:core': 'core icosahedron', 'dharma.cycle:npyr5': '(pentagonal pyramid; no name yet)', 'dharma.cycle:nfru3': 'Vajra (twist)',
         'dharma.cycle:npyr3': 'Cleo-low', 'dharma.cycle:nfru5': '(twisted pentagonal frustum; no name yet)', 'dharma.cycle:nt1': 't1 (Mosseri–Sadoc)',
         'dharma.cycle:ncap5': 'pentagonal cap (J2)', 'dharma.cycle:ncap6': 'Shield', 'dharma.cycle:nwedge': 'Vajra-blade', 'dharma.cycle:nedge': 'Sevenfold-blade',
         'dharma.cycle:nface': 'Cleo-low 2', 'karma.lotus:axe': 'AXE', 'karma.lotus:fuji': 'FUJI', 'karma.lotus:cleo': 'CLEO',
         'bodhi.kitB:copy': 'rhombic triacontahedron', 'bodhi.kitB:B1': 'Vajra (fine)', 'bodhi.kitB:B4': 'Crown Jewel', 'bodhi.kitB:B5L': 'Diadem L (R = mirror image)',
         'dharma.hinge:lj11': 'J11 (gyroelongated pentagonal pyramid)', 'bodhi.kitA:B2': 'Chatra', 'bodhi.kitA:B3': 'Mudra'}
MS = json.load(open(os.path.expanduser('~/Documents/kaleidohedra-references/shapes/mosseri-sadoc-tiles.json')))['tiles'] if os.path.exists(os.path.expanduser('~/Documents/kaleidohedra-references/shapes/mosseri-sadoc-tiles.json')) else []
out, reps = [], []
for view, pieces in DATA.items():
    seen = set()
    for role, Vr, Fr in pieces:
        Vn = np.array(Vr, float)
        sig = (role, len(Vr), len(Fr), round(ConvexHull(Vn).volume, 4))
        if sig in seen: continue
        seen.add(sig)
        a = analyse(Vr, Fr)
        if a is None: print('open piece', view, role); continue
        a['class'] = classify(a)
        dup = next((r for r in reps if congruent(r, a)), None)
        if dup is not None:
            tag = congruent(dup, a)
            dup['alsoIn'].append(f'{view}:{role}' + ('' if tag == 'same' else f' ({tag})')); continue
        a['id'] = f'{view}:{role}'; a['alsoIn'] = []
        if a['id'] == 'dharma.cycle:ncap': a['id'] += '5' if a['corners'] == 6 else '6'
        a['dictoName'] = NAMES.get(a['id'], '')
        a['mosseriSadoc'] = []
        for t in MS:
            b = analyse(t['vertices']['icosa13'], t['faces'])
            tag = congruent(b, a) if b else None
            if tag: a['mosseriSadoc'].append(f"{t['name']} at Icosa-13 scale" + ('' if tag == 'same' else f' {tag}'))
        a['exact'] = {'edge': {f'{x:.6f}': form(x, 3e-5) for x in a['edgeLengths']},
                      'dihedral': {f'{x:.3f}': form(math.cos(math.radians(x)), 4e-5, 'cos') for x in a['dihedrals']},
                      'volume': q5(a['volume'], 1e-5)}
        reps.append(a)
for a in reps:
    print(a['dictoName'], '| MS:', a['mosseriSadoc'])
    print(f"{a['id']:24s} also {','.join(a['alsoIn'])[:60]:60s} V{a['corners']} E{a['edges']} F{a['faces']} {a['faceTypes']} vol {a['volume']:.6f} sym {a['symmetryOrder']}/{a['properRotations']} {'convex' if a['convex'] else 'NONCONVEX'} | {a['class']}")
    print('     edges', a['edgeLengths'], ' dihedrals', a['dihedrals'])
    print('     exact', a['exact'])
    out.append({k: v for k, v in a.items() if k not in ('V', 'F', 'edgesMap')})
json.dump({'credit': 'DICTO · dictospheres.com', 'note': 'One representative per congruence class; lengths in the study units of pieces.json. Closed forms are fitted to 1e-6 (lengths) / 2e-5 (cosines): guesses, not proofs.', 'pieces': out},
          open(os.path.join(HERE, 'pieces-analysis.json'), 'w'), indent=1, ensure_ascii=False)
