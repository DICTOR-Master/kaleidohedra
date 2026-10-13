# Fused shells (DICTO 2026-10-13): the solids that the many pieces form. For each view, the layers between
# classic solids; in each layer, the pieces under each face of the layer's outer solid, fused into one solid;
# is it convex, what are its faces, and what is it called technically.
# Input: ../pieces.json (exported from src/app/seeds-data.js). Output: ../fused.json + a printed report.
import json, sys, os
import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(HERE, '..', 'pieces.json')))
TOL = 1e-6


def hull_faces(P):
    """Convex hull of points P as merged polygon faces: [(normal, offset, [vertex indices in order])]."""
    h = ConvexHull(P)
    faces = []
    for eq, simplex in zip(h.equations, h.simplices):
        n, d = eq[:3], -eq[3]
        for f in faces:
            if np.allclose(f[0], n, atol=1e-4) and abs(f[1] - d) < 1e-4:
                f[2].update(simplex); break
        else:
            faces.append([n, d, set(simplex)])
    out = []
    for n, d, idx in faces:
        idx = list(idx)
        c = P[idx].mean(0)
        u = P[idx[0]] - c; u /= np.linalg.norm(u); v = np.cross(n, u)
        idx.sort(key=lambda i: np.arctan2(np.dot(P[i] - c, v), np.dot(P[i] - c, u)))
        out.append((n, d, idx))
    return h, out


def dedupe(P):
    U = []
    for p in P:
        if not any(np.linalg.norm(p - q) < 1e-5 for q in U): U.append(p)
    return np.array(U)


def describe(P):
    """Face signature and a technical name for a convex solid with corner points P."""
    P = dedupe(P)
    h, F = hull_faces(P)
    # only true corners (drop points in the middle of edges/faces)
    used = sorted({i for _, _, f in F for i in f})
    corners = [i for i in used if sum(i in f for _, _, f in F) >= 3]
    P = P[corners]
    h, F = hull_faces(P)
    sig = {}
    for _, _, f in F: sig[len(f)] = sig.get(len(f), 0) + 1
    nV, nF = len(P), len(F)
    nE = nV + nF - 2
    name = classify(P, F, sig)
    edges = sorted({round(float(np.linalg.norm(P[f[i]] - P[f[(i + 1) % len(f)]])), 4) for _, _, f in F for i in range(len(f))})
    return {'V': nV, 'E': nE, 'F': nF, 'faces': {f'{k}-gon': v for k, v in sorted(sig.items())}, 'name': name,
            'volume': round(float(h.volume), 6), 'edgeLengths': edges}


NGON = {3: 'triangular', 4: 'quadrilateral', 5: 'pentagonal', 6: 'hexagonal', 7: 'heptagonal', 8: 'octagonal', 10: 'decagonal'}


def regular(P, f):
    L = [np.linalg.norm(P[f[i]] - P[f[(i + 1) % len(f)]]) for i in range(len(f))]
    c = P[f].mean(0); R = [np.linalg.norm(P[i] - c) for i in f]
    return max(L) - min(L) < 1e-5 and max(R) - min(R) < 1e-5


def classify(P, F, sig):
    nV = len(P)
    # pyramid: one face holds all but one corner
    for n, d, f in F:
        if len(f) == nV - 1:
            base = NGON.get(len(f), f'{len(f)}-gonal')
            if len(f) == 3: return 'tetrahedron (triangular pyramid)' + (' — regular' if all(regular(P, g) for _, _, g in F) else '')
            return f'{base} pyramid' + (' (regular base)' if regular(P, f) else '')
    # prismatoid: two parallel faces holding every corner
    for i, (n1, d1, f1) in enumerate(F):
        for n2, d2, f2 in F[i + 1:]:
            if np.allclose(n1, -n2, atol=1e-6) and len(set(f1) | set(f2)) == nV:
                a, b = sorted([f1, f2], key=len)
                sides = [g for _, _, g in F if g is not f1 and g is not f2]
                if len(a) == len(b):
                    k = NGON.get(len(a), f'{len(a)}-gonal')
                    if all(len(g) == 4 for g in sides):
                        sa = np.mean([np.linalg.norm(P[j] - P[a].mean(0)) for j in a]); sb = np.mean([np.linalg.norm(P[j] - P[b].mean(0)) for j in b])
                        return f'{k} prism' if abs(sa - sb) < 1e-5 else f'{k} frustum (truncated {k} pyramid)'
                    if all(len(g) == 3 for g in sides):
                        sa = np.mean([np.linalg.norm(P[j] - P[a].mean(0)) for j in a]); sb = np.mean([np.linalg.norm(P[j] - P[b].mean(0)) for j in b])
                        return f'{k} antiprism' if abs(sa - sb) < 1e-5 else f'twisted {k} frustum ({k} antiprismoid)'
                    return f'{k} prismatoid'
                if len(b) == 2 * len(a) and all(len(g) in (3, 4) for g in sides):
                    return f'{NGON.get(len(a), str(len(a)))} cupola-like prismatoid ({len(a)}-gon over {len(b)}-gon)'
                return f'prismatoid ({len(a)}-gon over {len(b)}-gon)'
    s = ', '.join(f'{v} {NGON.get(k, str(k) + "-gon")}{"s" if v > 1 else ""}' for k, v in sorted(sig.items()))
    return f'convex polyhedron ({s})'


def piece_hull(V):
    P = np.array(V, float)
    return P, ConvexHull(P).volume


def run(view):
    pieces = DATA[view]
    allP = np.array([p for _, V, _ in pieces for p in V], float)
    c0 = allP.mean(0)
    items = []
    for role, V, F in pieces:
        P = np.array(V, float) - c0
        items.append({'role': role, 'P': P, 'F': F, 'vol': ConvexHull(P).volume, 'rmax': round(float(np.linalg.norm(P, axis=1).max()), 3)})
    keys = sorted({it['rmax'] for it in items})
    report = {'view': view, 'layers': []}
    for k in keys:
        inside = [it for it in items if it['rmax'] <= k + 1e-9]
        layer = [it for it in items if abs(it['rmax'] - k) < 1e-9]
        Pall = np.vstack([it['P'] for it in inside])
        h, HF = hull_faces(Pall)
        vol_union = sum(it['vol'] for it in inside)
        convex = abs(h.volume - vol_union) < 1e-6 * max(1, h.volume)
        L = {'outerRadius': k, 'pieces': {}, 'outerSolid': describe(Pall) if convex else None, 'outerConvex': bool(convex)}
        for it in layer: L['pieces'][it['role']] = L['pieces'].get(it['role'], 0) + 1
        if convex:
            # which hull faces each piece lies on (one of its faces in the hull face's plane, centre inside it)
            tiles = {i: [] for i in range(len(HF))}
            edge, inner = [], []
            for it in layer:
                on = set()
                for f in it['F']:
                    q = it['P'][f]; c = q.mean(0)
                    for i, (n, d, _) in enumerate(HF):
                        if np.all(np.abs(q @ n - d) < 1e-6): on.add(i)
                it['on'] = on
                (tiles[next(iter(on))].append(it) if len(on) == 1 else (edge if on else inner).append(it))
            # inner pieces join the tile of a piece they share a whole face with
            changed = True
            while changed and inner:
                changed = False
                for it in list(inner):
                    for i, ts in tiles.items():
                        if any(shares_face(it, t) for t in ts):
                            ts.append(it); inner.remove(it); changed = True; break
            kinds = {}
            for i, ts in tiles.items():
                if not ts: continue
                P = np.vstack([t['P'] for t in ts])
                hv = ConvexHull(P).volume; uv = sum(t['vol'] for t in ts)
                d = describe(P) if abs(hv - uv) < 1e-6 * max(1, hv) else None
                key = (tuple(sorted(t['role'] for t in ts)), d['name'] if d else 'not convex', tuple(d['edgeLengths']) if d else ())
                kinds.setdefault(key, {'count': 0, 'roles': list(key[0]), 'convex': d is not None, 'solid': d, 'outerFace': f'{len(HF[i][2])}-gon'})
                kinds[key]['count'] += 1
            L['faceTiles'] = list(kinds.values())
            L['edgePieces'] = sorted({it['role'] for it in edge})
            L['unplaced'] = sorted({it['role'] for it in inner})
        report['layers'].append(L)
    return report


def shares_face(a, b):
    for f in a['F']:
        q = a['P'][f]
        for g in b['F']:
            r = b['P'][g]
            if len(f) == len(g) and all(any(np.linalg.norm(x - y) < 1e-6 for y in r) for x in q): return True
    return False


if __name__ == '__main__':
    out = [run(v) for v in DATA]
    json.dump(out, open(os.path.join(HERE, '..', 'fused.json'), 'w'), indent=1)
    for R in out:
        print('==', R['view'])
        for L in R['layers']:
            o = L['outerSolid']
            print(f"  layer to r={L['outerRadius']}: pieces {L['pieces']}; outer {'convex: ' + o['name'] + ' ' + str(o['faces']) if o else 'NOT convex'}")
            for t in L.get('faceTiles', []):
                s = t['solid']
                print(f"    x{t['count']} under a {t['outerFace']}: {'+'.join(t['roles'])} -> {s['name'] + ' ' + str(s['faces']) + ' V' + str(s['V']) if s else 'not convex'}")
            if L.get('edgePieces'): print('    edge/corner pieces:', L['edgePieces'])
            if L.get('unplaced'): print('    unplaced inner pieces:', L['unplaced'])
