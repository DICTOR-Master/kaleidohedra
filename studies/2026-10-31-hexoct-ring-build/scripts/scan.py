# Scan of the hole weight lambda over the walk -11/24 <= lambda <= 3/8: the outer faces of the c-tile (ABC, layer 1) and the
# h-tile (AB, layer 0) as ONE solid each, exact, and how many of the faces can be laid with rings.
# Ring = security ring pulled into a triangle of side 1/2 (build at double scale: a unit triangle = 4 rings).
# Usage (dicto-big-brother): TILES_DIR=~/kres-tmp/endless ~/geom/bin/python scan.py [lambda ...]  -> ../out/scan.tsv, ../out/scan.txt
import os, sys, json
from fractions import Fraction as Fr
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get('TILES_DIR', os.path.join(HERE, '../../2026-10-29-endless-stack-cell/scripts')))
sys.path.insert(0, HERE)
from tiles import tile
import exactfaces
from exactfaces import union_faces, ring_test, face_info, volume6, piece_volume6, edge_multiplicity, sub, cross

TILES = (('c', 'ABC', 1), ('h', 'AB', 0))

def components(faces):
    segs, bad = edge_multiplicity(faces)
    own = {}
    for fi, f in enumerate(faces):
        for lp in f['loops']:
            for i in range(len(lp)): own.setdefault(frozenset((lp[i], lp[(i + 1) % len(lp)])), set()).add(fi)
    # faces meeting along a (sub)segment: use split segments
    par = list(range(len(faces)))
    def fd(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    segface = {}
    for fi, f in enumerate(faces):
        for lp in f['loops']:
            for i in range(len(lp)):
                p, q = lp[i], lp[(i + 1) % len(lp)]
                for (a, b) in segs:
                    if cross(sub(a, p), sub(q, p)) == (0, 0, 0) and cross(sub(b, p), sub(q, p)) == (0, 0, 0):
                        d = sub(q, p); ta = sum(x * y for x, y in zip(sub(a, p), d)); tb = sum(x * y for x, y in zip(sub(b, p), d))
                        dd = sum(x * x for x in d)
                        if 0 <= ta <= dd and 0 <= tb <= dd: segface.setdefault(frozenset((a, b)), set()).add(fi)
    for s, F in segface.items():
        F = list(F)
        for j in F[1:]: par[fd(j)] = fd(F[0])
    return len({fd(i) for i in range(len(faces))}), bad

def analyse(word, L, lam):
    P, _ = tile(word, L, lam)
    pieces = [pts for k, up, s, pts, J in P]
    faces = union_faces(pieces); glue = sorted(exactfaces.GLUE)
    vol_ok = volume6(faces) == sum(piece_volume6(X) for X in pieces)
    ncomp, bad = components(faces)
    kinds = Counter(); ring_ok = 0; unit_ok = 0; rings = 0; holes = 0
    for f in faces:
        n, sides = face_info(f); holes += len(f['loops']) - 1
        r = ring_test(f, Fr(1, 2)); u = ring_test(f, Fr(1))
        kinds[n] += 1
        if r: ring_ok += 1; rings += r['rings']
        if u: unit_ok += 1
    return dict(pieces=len(pieces), faces=len(faces), kinds=dict(sorted(kinds.items())), ring_ok=ring_ok, unit_ok=unit_ok,
                rings=rings if ring_ok == len(faces) else None, holes=holes, vol_ok=vol_ok, surface_parts=ncomp, edge_bad=len(bad),
                glued=['-'.join(f"{P[i][0]}{'' if P[i][1] is None else ('^' if P[i][1] else 'v')}{'+' if P[i][2][2] > 0 else '-'}" for i in g) for g in glue])

def kinds_str(k): return ' '.join(f'{v}x{n}' for n, v in sorted(k.items()))

if __name__ == '__main__':
    if sys.argv[1:]:
        lams = [Fr(x) for x in sys.argv[1:]]
    else:
        grid = [Fr(k, 96) for k in range(-44, 37)]
        known = [Fr(-11, 24), Fr(-3, 8), Fr(-7, 24), Fr(-1, 8), Fr(0), Fr(1, 10), Fr(3, 8)]
        lams = sorted(set(grid + known))
    OUT = os.path.join(HERE, '../out'); os.makedirs(OUT, exist_ok=True)
    rows = []
    for lam in lams:
        row = {'lam': str(lam)}
        for t, w, L in TILES:
            a = analyse(w, L, lam); row[t] = a
        rows.append(row)
        c, h = row['c'], row['h']
        print(f"{str(lam):>7} | c: {c['faces']:>2} faces [{kinds_str(c['kinds'])}] ring {c['ring_ok']}/{c['faces']} unit {c['unit_ok']} parts {c['surface_parts']}"
              f" vol {c['vol_ok']} edges {c['edge_bad']} | h: {h['faces']:>2} faces [{kinds_str(h['kinds'])}] ring {h['ring_ok']}/{h['faces']}"
              f" unit {h['unit_ok']} parts {h['surface_parts']} vol {h['vol_ok']} edges {h['edge_bad']}", flush=True)
        print(f"          glued c: {c['glued']}  h: {h['glued']}", flush=True)
    tag = 'scan' if not sys.argv[1:] else 'scan-extra'
    json.dump(rows, open(os.path.join(OUT, f'{tag}.json'), 'w'), indent=1, default=str)
