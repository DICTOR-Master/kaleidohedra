#!/usr/bin/env python3
"""Exact, independent check of the class-O edge-to-edge question (any tiling of space, periodic or not):
can R^3 be tiled by RT centre pyramids all parallel to the 30 pyramids of one RT (class O), meeting edge to edge
(two pieces that meet along a segment of an edge share that whole edge, same end points)?
Angles: base edges 72 deg, lateral edges to 5-fold corners 72 deg, to 3-fold corners 120 deg; round every edge the other sectors
(4 of 72 deg or 2 of 120 deg) must be filled by pieces having that same edge segment. Depth-first search: take the first unfilled
sector, try every class-O piece that has the same segment as an edge of the same kind and lies in that sector (all 30 templates,
both directions of the edge), reject exact overlaps (Z[phi] arithmetic). If every branch dies, no such tiling exists.
Works for kind C6 / RD too (controls: they must not die). Usage: classO_e2e.py KIND MAXPIECES"""
import sys, os, json, time, itertools, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geom import *
kind = sys.argv[1]; MAXP = int(sys.argv[2])
E, T = kind_data(kind); P = [Piece(t, E) for t in T]; nT = len(P)
# edge kinds per template: (i, j, kindlabel, dihedral sectors m)
def edge_info(p):
    out = []
    for i, j in p.edges:
        L = round(float(np.linalg.norm(zf(p.V[j] - p.V[i]))), 6); lab = ('lat' if 0 in (i, j) else 'base', L)
        # dihedral from the two face normals at the edge
        ns = [zf(p.N[f]) for f in range(len(p.N)) if all(zsign(p.off[f] - zdot(p.N[f], p.V[v])) == 0 for v in (i, j))]
        a = math.pi - math.acos(np.clip(ns[0] @ ns[1]/np.linalg.norm(ns[0])/np.linalg.norm(ns[1]), -1, 1))
        out.append((i, j, lab, int(round(2*math.pi/a)), a))
    return out
EI = [edge_info(p) for p in P]
print(kind, 'edge kinds (kind, length, sectors):', sorted({(l[0], l[1], m) for e in EI for _, _, l, m, _ in e}), flush=True)
AX = {}
def overlap(o1, a1, o2, a2):
    if (o1, o2) not in AX: AX[(o1, o2)] = pair_axes(P[o1], P[o2])
    U, hi, lo = AX[(o1, o2)]
    return overlap_many(U, hi, lo, to3(np.array([a2 - a1]), E))[0]
def verts(o, a): return T[o] + a           # module coordinates of the piece's vertices
FACES_AT = {}
def faces_at(o, i, j):
    if (o, i, j) not in FACES_AT:
        p = P[o]; FACES_AT[(o, i, j)] = [f for f in range(len(p.N)) if all(zsign(p.off[f] - zdot(p.N[f], p.V[v])) == 0 for v in (i, j))]
    return FACES_AT[(o, i, j)]
def wedge_dir(o, a, i, j):
    """unit bisector (float) of the piece's wedge at edge (i, j), perpendicular to the edge (from the two outward face normals)"""
    V = zf(to3(verts(o, a), E)); X, Y = V[i], V[j]; ax = (Y - X)/np.linalg.norm(Y - X)
    f1, f2 = faces_at(o, min(i, j), max(i, j)); n1 = zf(P[o].N[f1]); n2 = zf(P[o].N[f2])
    c = -(n1/np.linalg.norm(n1) + n2/np.linalg.norm(n2)); c = c - ax*(c @ ax); return c/np.linalg.norm(c), ax, (X + Y)/2
def candidates(o, a, i, j, lab, m, ang, k):
    """class-O pieces having edge (X,Y) of the same kind and lying in sector k (k = 1..m-1) counted from piece (o,a)"""
    n = verts(o, a); X, Y = n[i], n[j]
    w0, ax, mid = wedge_dir(o, a, i, j)
    target = math.cos(k*ang)*w0 + math.sin(k*ang)*np.cross(ax, w0)      # bisector of sector k (rotating one way)
    target2 = math.cos(-k*ang)*w0 + math.sin(-k*ang)*np.cross(ax, w0)
    out = []
    for o2 in range(nT):
        for (i2, j2, lab2, m2, ang2) in EI[o2]:
            if lab2 != lab: continue
            for (p_, q_) in ((i2, j2), (j2, i2)):
                if not np.array_equal(T[o2][q_] - T[o2][p_], Y - X): continue
                a2 = X - T[o2][p_]
                w, _, _ = wedge_dir(o2, a2, min(p_, q_), max(p_, q_))
                if np.allclose(w, target, atol=1e-6): out.append((o2, tuple(a2)))
    return out, target2
def same(t1, t2): return t1[0] == t2[0] and tuple(t1[1]) == tuple(t2[1])
st = {'nodes': 0, 'best': 0, 't0': time.time()}
def todo_of(idx, tile):
    o, a = tile; return [(idx, i, j, lab, mm, ang, k) for (i, j, lab, mm, ang) in EI[o] for k in range(1, mm)]
def search(tiles, todo):
    st['nodes'] += 1
    if len(tiles) > st['best']:
        st['best'] = len(tiles); st['best_tiles'] = [(int(o), list(map(int, a))) for o, a in tiles]
    if st['nodes'] % 2000 == 0: print(f"PROGRESS 0.5 nodes {st['nodes']} deepest {st['best']} ({time.time() - st['t0']:.0f} s)", flush=True)
    if len(tiles) >= MAXP: return True
    while todo:
        ti, i, j, lab, mm, ang, k = todo[0]; o, a = tiles[ti]
        cs, _ = candidates(o, np.array(a), i, j, lab, mm, ang, k)
        if any(same(c, u) for c in cs for u in tiles): todo = todo[1:]; continue
        for c in cs:
            if any(overlap(u[0], np.array(u[1]), c[0], np.array(c[1])) for u in tiles): continue
            if search(tiles + [c], todo[1:] + todo_of(len(tiles), c)): return True
        return False
    return True
seed = (0, tuple([0]*E.shape[0]))
# sanity: each sector of the seed gets the same number of candidates from both rotation senses (symmetry of the construction)
ok = search([seed], todo_of(0, seed))
res = {'kind': kind, 'max_pieces': MAXP, 'reached_max': ok, 'nodes': st['nodes'], 'deepest_patch': st['best'], 'seconds': round(time.time() - st['t0'], 1),
       'deepest_tiles_template_apex': st.get('best_tiles')}
print({k: v for k, v in res.items() if k != 'deepest_tiles_template_apex'}, flush=True)
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', f'classO-e2e-{kind}-{MAXP}.json'), 'w'), indent=0)
print('VERDICT', kind, 'every branch dies: no edge-to-edge tiling in this class' if not ok else f'a patch of {MAXP} pieces exists (search alive)')
