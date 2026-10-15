# The interlock's piece kinds described for naming (DICTO names them): for each kind (grouped by volume, which the exact check
# showed equals the symmetry-orbit grouping), the count, the original layer and flipped layer it lies in, its corners, and its
# faces (coplanar triangles of the float hull merged). Float shapes; exact volumes are matched from data/interlock-<setting>-exact.txt.
# -> data/interlock-kinds.txt
import json, re, sys, collections, itertools
import numpy as np
from scipy.spatial import ConvexHull
out = []
for setting in ('ends', 'middle'):
    d = json.load(open(f'data/interlock-{setting}.json'))
    exact = re.findall(r'^\s+(\d+) x\s+(.*?) = ([0-9.]+)$', open(f'data/interlock-{setting}-exact.txt').read(), re.M)
    groups = collections.defaultdict(list)
    for p in d['pieces']: groups[round(p['vol'], 7)].append(p)
    out.append(f'== {setting} setting: {len(d["pieces"])} pieces, {len(groups)} kinds')
    rows = []
    for vol, ps in groups.items():
        ex = [e for e in exact if abs(float(e[2]) - vol) < 2e-7]
        assert len(ex) == 1 and int(ex[0][0]) == len(ps), (setting, vol, ex, len(ps))
        P = np.array(ps[0]['v'])
        U = []                                              # merge float duplicates
        for x in P:
            if all(np.linalg.norm(x - y) > 1e-6 for y in U): U.append(x)
        P = np.array(U)
        def is_corner(i):                                   # a true corner is where >= 3 face planes with independent normals meet
            Hh = ConvexHull(P); ns = [e[:3] for e in Hh.equations if abs(P[i] @ e[:3] + e[3]) < 1e-7]
            return np.linalg.matrix_rank(np.array(ns), tol=1e-6) == 3
        P = P[[i for i in range(len(P)) if is_corner(i)]]
        h = ConvexHull(P)
        faces = []
        for e in h.equations:
            on = tuple(sorted(i for i in range(len(P)) if abs(P[i] @ e[:3] + e[3]) < 1e-7))
            if on not in faces: faces.append(on)
        corners = sorted(set(itertools.chain(*faces)))
        fs = collections.Counter(len(f) for f in faces)
        olay = collections.Counter(d['orig_layers'][p['o'][0]] for p in ps)
        flay = collections.Counter(f"{d['flip_layers'][p['f'][1]]} (turn {p['f'][0]})" for p in ps)
        # edge lengths
        E = set()
        for f in faces:
            Q = P[list(f)]; c = Q.mean(0); n = np.cross(Q[1] - Q[0], Q[2] - Q[0]); u = (Q[0] - c); u /= np.linalg.norm(u); w = np.cross(n / np.linalg.norm(n), u)
            order = [f[i] for i in np.argsort([np.arctan2((P[j] - c) @ w, (P[j] - c) @ u) for j in f])]
            for a, b in zip(order, order[1:] + order[:1]): E.add(tuple(sorted((a, b))))
        el = sorted(round(float(np.linalg.norm(P[a] - P[b])), 4) for a, b in E)
        rows.append((-vol, f"  {len(ps):3d} x vol {ex[0][1]} = {ex[0][2]}\n"
                           f"      in original layer: {', '.join(f'{k} ({v})' for k, v in olay.items())}\n"
                           f"      in flipped layer: {', '.join(f'{k} ({v})' for k, v in flay.items())}\n"
                           f"      {len(corners)} corners, {len(faces)} faces " + ', '.join(f'{v}×{k}-gon' for k, v in sorted(fs.items())) + f"; {len(E)} edges, lengths {sorted(set(el))}"))
    out += [r for _, r in sorted(rows)]
open('data/interlock-kinds.txt', 'w').write('DICTO · dictospheres.com\n' + '\n'.join(out) + '\n'); print('\n'.join(out))
