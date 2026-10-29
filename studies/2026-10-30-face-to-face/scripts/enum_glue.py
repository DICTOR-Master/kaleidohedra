# #77 Face to Face (DICTO 2026-10-30): the five-pyramids search of 2026-10-27 (copied unchanged but for the output names and
# the worker count argument), run one piece further: DICTO's pieces alone to 6 pieces (DEEP=1).
# Five pyramids study, question 2 (DICTO, 2026-10-27): enumerate small face-to-face gluings of DICTO's pieces (and the
# regular solids) and keep those whose surface is made of equilateral triangles. Float screening (tolerance 1e-7) on
# dicto-big-brother; every kept result is re-checked exactly by exact_check.py.
#
# Rules of the search (stated in the README):
#  * pieces at the scale where their equilateral faces have edge 1, plus the Mosseri-Sadoc tiles also at the scale where
#    their other edge length is 1 (so that tiles can meet on their (1,1,tau) and (1,tau,tau) faces at both sizes);
#    mirror images of chiral pieces included;
#  * a new piece is glued whole face to whole congruent face (any congruent face, equilateral or not), interiors disjoint;
#  * levels 1-3 are complete; at level 4 the fourth piece must be glued on a face that is not yet equilateral-safe when
#    such a face exists (a face of the 3-piece cluster that would otherwise stay non-equilateral).
import itertools, json, sys, time, pickle, os
from multiprocessing import Pool
import numpy as np
import manifold3d as m3
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pieces import build, fl

TOL = 1e-7
PHI = (1 + 5 ** 0.5) / 2
USE = ['Tetrahedron', 'Octahedron', 'Icosahedron', 'Q (tetrahedron face pyramid)', 'Octahedron face pyramid', 'Cleo-Icos',
       'Half octahedron P', 'Antonius', 'Admiral Cap', 'M-S t1', 'Hound Tooth (M-S t2)', 'Tricap (M-S t3)', 'CLEO (M-S t4)',
       'M-S t5', 'AXE (M-S t6)', 'Weirdstone', 'Tadpole']
MS = ['M-S t1', 'Hound Tooth (M-S t2)', 'Tricap (M-S t3)', 'CLEO (M-S t4)', 'M-S t5', 'AXE (M-S t6)']

def tri_mesh(V, F):
    tris = [[f[0], f[k], f[k + 1]] for f in F for k in range(1, len(f) - 1)]
    return np.asarray(V, float), np.asarray(tris, np.uint32)

def manifold_of(V, F):
    v, t = tri_mesh(V, F)
    return m3.Manifold(m3.Mesh64(vert_properties=np.ascontiguousarray(v, np.float64), tri_verts=np.ascontiguousarray(t, np.uint32)))

def eq_edge(V, F):
    best = None
    for f in F:
        if len(f) == 3:
            l = [np.linalg.norm(V[f[i]] - V[f[(i + 1) % 3]]) for i in range(3)]
            if max(l) - min(l) < TOL: best = l[0] if best is None else min(best, l[0])
    return best

def congruent_to_mirror(V):
    """True if the point set V is carried onto its mirror image by a proper rigid motion (corner matching)."""
    W = V * np.array([-1, 1, 1]); return match_sets(V, W)

def match_sets(A, B):
    n = len(A)
    if n != len(B): return False
    ca, cb = A.mean(0), B.mean(0); A0, B0 = A - ca, B - cb
    da = np.sort(np.linalg.norm(A0, axis=1)); db = np.sort(np.linalg.norm(B0, axis=1))
    if np.abs(da - db).max() > 1e-6: return False
    # pick three non-collinear points of A, try every image triple in B with the same distances
    idx = [0]
    for i in range(1, n):
        if np.linalg.norm(A0[i] - A0[0]) > 1e-6: idx.append(i); break
    for i in range(1, n):
        if i not in idx and np.linalg.norm(np.cross(A0[idx[1]] - A0[idx[0]], A0[i] - A0[idx[0]])) > 1e-6: idx.append(i); break
    if len(idx) < 3: return True
    for p in itertools.permutations(range(n), 3):
        ok = all(abs(np.linalg.norm(B0[p[a]] - B0[p[b]]) - np.linalg.norm(A0[idx[a]] - A0[idx[b]])) < 1e-6 for a, b in [(0, 1), (0, 2), (1, 2)])
        if not ok or any(abs(np.linalg.norm(B0[p[a]]) - np.linalg.norm(A0[idx[a]])) > 1e-6 for a in range(3)): continue
        R = kabsch(A0[idx], B0[list(p)])
        if R is None: continue
        C = A0 @ R.T
        if all(np.linalg.norm(B0 - c, axis=1).min() < 1e-6 for c in C): return True
    return False

def kabsch(P, Q):
    """Proper rotation R with R P_i = Q_i (least squares); None if the fit is poor."""
    H = P.T @ Q; U, S, Wt = np.linalg.svd(H); d = np.sign(np.linalg.det(Wt.T @ U.T))
    R = Wt.T @ np.diag([1, 1, d]) @ U.T
    return R if np.abs(P @ R.T - Q).max() < 1e-6 else None

DEEP = os.environ.get('DEEP') == '1'   # deep mode: DICTO's pieces only, non-equilateral faces glued first (see README)
REGULAR = ['Tetrahedron', 'Octahedron', 'Icosahedron', 'Half octahedron P']

def library():
    L = build(); lib = []
    for nm in USE:
        if DEEP and nm in REGULAR: continue
        V = fl(L[nm]['V']); F = L[nm]['F']; e = eq_edge(V, F)
        scales = [1 / e]
        if nm in MS:  # also the scale where the tile's other edge length is 1
            ls = sorted({round(np.linalg.norm(V[a] - V[b]), 9) for f in F for a, b in zip(f, f[1:] + f[:1])})
            other = [x for x in ls if abs(x - e) > 1e-6][0]; scales.append(1 / other)
        chiral = not congruent_to_mirror(V - V.mean(0))
        for s in scales:
            W = (V - V.mean(0)) * s; tag = '' if abs(s * e - 1) < 1e-9 else ' [eq %.4f]' % (s * e)
            lib.append(dict(name=nm + tag, base=nm, V=W, F=F))
            if chiral:
                lib.append(dict(name=nm + tag + ' (mirror)', base=nm, V=W * np.array([-1, 1, 1]), F=[list(reversed(f)) for f in F]))
    for p in lib:
        p['M'] = manifold_of(p['V'], p['F']); p['vol'] = p['M'].volume()
        p['faces'] = [face_data(p['V'], f) for f in p['F']]
    return lib

def face_data(V, f):
    P = V[f]; n = np.cross(P[1] - P[0], P[2] - P[0]); n /= np.linalg.norm(n)
    sides = [np.linalg.norm(P[(i + 1) % len(f)] - P[i]) for i in range(len(f))]
    eq = len(f) == 3 and max(sides) - min(sides) < TOL
    return dict(P=P, n=n, sides=np.array(sides), eq=eq, k=len(f), area=0.5 * np.linalg.norm(sum(np.cross(P[i], P[(i + 1) % len(f)]) for i in range(len(f)))))

# A cluster: list of (lib index, R, t). Its exposed faces are piece faces not glued.
def placed(lib, item):
    i, R, t = item; return lib[i]['V'] @ R.T + t

def placements(lib, Fc, j):
    """All placements of library piece j glued with one of its faces onto the exposed face Fc (a points array, ccw out)."""
    out = []; k = len(Fc['P'])
    for gi, g in enumerate(lib[j]['faces']):
        if g['k'] != k or abs(g['area'] - Fc['area']) > 1e-6: continue
        G = g['P'][::-1]  # reversed: the new piece's face faces the other way
        for s in range(k):
            Gs = np.roll(G, -s, axis=0)
            if np.abs(np.linalg.norm(np.roll(Gs, -1, 0) - Gs, axis=1) - np.linalg.norm(np.roll(Fc['P'], -1, 0) - Fc['P'], axis=1)).max() > 1e-6: continue
            cg, cf = Gs.mean(0), Fc['P'].mean(0)
            R = kabsch(Gs - cg, Fc['P'] - cf)
            if R is None: continue
            out.append((j, R, cf - R @ cg, gi))
    return out

def signature(lib, cl):
    pts = np.vstack([placed(lib, it) for it in cl]); lab = np.concatenate([[lib[it[0]]['base'].__hash__() % 997] * len(lib[it[0]]['V']) for it in cl])
    D = np.round(np.linalg.norm(pts[:, None] - pts[None], axis=2), 5)
    rows = sorted(tuple(sorted(zip(D[a], lab))) + (lab[a],) for a in range(len(pts)))
    return hash((tuple(sorted(lib[it[0]]['base'] for it in cl)), tuple(rows)))

def cluster_manifold(lib, cl):
    M = None
    for (i, R, t) in cl:
        m = lib[i]['M'].transform(np.hstack([R, t[:, None]]).astype(float))
        M = m if M is None else M + m
    return M

def exposed(lib, cl):
    """Exposed faces (piece, face index, data) of the cluster: piece faces not met by an opposite congruent face."""
    F = []
    for a, (i, R, t) in enumerate(cl):
        for fi, f in enumerate(lib[i]['faces']):
            P = f['P'] @ R.T + t; n = R @ f['n']
            F.append(dict(a=a, fi=fi, P=P, n=n, c=P.mean(0), k=f['k'], eq=f['eq'], area=f['area'], sides=f['sides']))
    keep = []
    for x in F:
        glued = any(y['a'] != x['a'] and y['k'] == x['k'] and np.linalg.norm(y['c'] - x['c']) < 1e-6 and np.dot(y['n'], x['n']) < -1 + 1e-6
                    and abs(y['area'] - x['area']) < 1e-6 for y in F)
        if not glued: keep.append(x)
    return keep

def overlaps(lib, cl, new):
    j, R, t = new[:3]; m = lib[j]['M'].transform(np.hstack([R, t[:, None]]))
    P = lib[j]['V'] @ R.T + t; c = P.mean(0); rad = np.linalg.norm(P - c, axis=1).max()
    for (i, R2, t2) in cl:
        Q = lib[i]['V'] @ R2.T + t2
        if np.linalg.norm(Q.mean(0) - c) > rad + np.linalg.norm(Q - Q.mean(0), axis=1).max() + 1e-9: continue
        mi = lib[i]['M'].transform(np.hstack([R2, t2[:, None]]))
        if (m ^ mi).volume() > 1e-7: return True
    return False

def surface_report(lib, cl, info=None):
    """The cluster's surface: its exposed piece faces, merged into planar faces. Returns the merged faces (corner arrays,
    ccw from outside) or None if the surface is not a closed 2-manifold of Euler characteristic 2 (e.g. pieces touching
    along an edge or a partial face without being glued, or a pinch)."""
    ex = exposed(lib, cl)
    # unglued faces of different pieces lying against each other (opposite normals, same plane) = a partial contact: reject
    for x, y in itertools.combinations(ex, 2):
        if x['a'] != y['a'] and np.dot(x['n'], y['n']) < -1 + 1e-7 and abs(np.dot(x['n'], y['c'] - x['c'])) < 1e-7:
            if poly_overlap(x, y): 
                if info is not None: info['reason'] = 'partial face contact'
                return None
    # plane groups
    groups = []
    for x in ex:
        for g in groups:
            y = g[0]
            if np.dot(x['n'], y['n']) > 1 - 1e-9 and abs(np.dot(y['n'], x['c'] - y['c'])) < 1e-7: g.append(x); break
        else: groups.append([x])
    # global vertex list
    pts = []
    def vid(p):
        for i, q in enumerate(pts):
            if np.linalg.norm(p - q) < 1e-6: return i
        pts.append(p); return len(pts) - 1
    allv = [vid(p) for x in ex for p in x['P']]
    faces = []; halfedges = {}
    for g in groups:
        # directed boundary edges of the group's polygons, split at every group vertex lying on them, cancelled in pairs
        gv = sorted({vid(p) for x in g for p in x['P']})
        E = {}
        for x in g:
            ids = [vid(p) for p in x['P']]
            for a_, b_ in zip(ids, ids[1:] + ids[:1]):
                A, B = pts[a_], pts[b_]; L = np.linalg.norm(B - A); u = (B - A) / L
                on = sorted([(np.dot(pts[v] - A, u), v) for v in gv if v not in (a_, b_) and 1e-7 < np.dot(pts[v] - A, u) < L - 1e-7
                             and np.linalg.norm(pts[v] - A - np.dot(pts[v] - A, u) * u) < 1e-7])
                chain = [a_] + [v for _, v in on] + [b_]
                for p_, q_ in zip(chain, chain[1:]): E[(p_, q_)] = E.get((p_, q_), 0) + 1
        bd = []
        for (p_, q_), c in E.items():
            net = c - E.get((q_, p_), 0)
            if net > 1: return None
            if net == 1: bd.append((p_, q_))
        nxt = {}
        for p_, q_ in bd: nxt.setdefault(p_, []).append(q_)
        if any(len(v) != 1 for v in nxt.values()):
            if info is not None: info['reason'] = 'region with hole or pinch'
            return None
        used = set(); 
        for s0 in list(nxt):
            if s0 in used: continue
            loop = [s0]; used.add(s0); cur = nxt[s0][0]
            while cur != s0: loop.append(cur); used.add(cur); cur = nxt[cur][0]
            faces.append(loop)
    # surface checks: each undirected edge (between corners, after splitting) in exactly two faces, opposite directions
    for f in faces:
        for p_, q_ in zip(f, f[1:] + f[:1]):
            if (p_, q_) in halfedges: 
                if info is not None: info['reason'] = 'edge used twice in one direction'
                return None
            halfedges[(p_, q_)] = 1
    if any((q_, p_) not in halfedges for (p_, q_) in halfedges):
        if info is not None: info['reason'] = 'open edge'
        return None
    out = []
    for f in faces:
        P = np.array([pts[i] for i in f])
        keep = [i for i in range(len(P)) if np.linalg.norm(np.cross(P[i] - P[i - 1], P[(i + 1) % len(P)] - P[i])) > 1e-7]
        out.append(P[keep])
    # Euler characteristic of the merged surface (corners only)
    cid = {}
    for P in out:
        for p in P: cid.setdefault(tuple(np.round(p, 6)), len(cid))
    Ed = set()
    for P in out:
        ids = [cid[tuple(np.round(p, 6))] for p in P]
        for p_, q_ in zip(ids, ids[1:] + ids[:1]): Ed.add((min(p_, q_), max(p_, q_)))
    chi = len(cid) - len(Ed) + len(out)
    if info is not None: info['chi'] = chi
    if chi != 2:
        if info is not None: info['reason'] = 'Euler characteristic %d' % chi
        return None
    # volume enclosed by the surface = the pieces' volumes
    vol = sum(np.dot(P[0], np.cross(P[k], P[k + 1])) for P in out for k in range(1, len(P) - 1)) / 6
    if abs(vol - sum(lib[i]['vol'] for i, _, _ in cl)) > 1e-6:
        if info is not None: info['reason'] = 'volume mismatch'
        return None
    return out

def poly_overlap(x, y):
    """Do two coplanar convex polygons overlap in area? (separating axes in their plane)"""
    n = x['n']; u = x['P'][1] - x['P'][0]; u /= np.linalg.norm(u); w = np.cross(n, u)
    A = np.c_[x['P'] @ u, x['P'] @ w]; B = np.c_[y['P'] @ u, y['P'] @ w]
    for P in (A, B):
        for i in range(len(P)):
            e = P[(i + 1) % len(P)] - P[i]; ax = np.array([-e[1], e[0]])
            a1, a2 = (A @ ax).min(), (A @ ax).max(); b1, b2 = (B @ ax).min(), (B @ ax).max()
            if a2 <= b1 + 1e-9 or b2 <= a1 + 1e-9: return False
    return True

def classify_faces(faces):
    """'strict' if every merged face is an equilateral triangle of one common edge; 'tri-surface' handled by caller."""
    if faces is None: return None, None
    sides = []
    for P in faces:
        if len(P) != 3: return 'not', None
        l = [np.linalg.norm(P[i] - P[(i + 1) % 3]) for i in range(3)]
        if max(l) - min(l) > 1e-6: return 'not', None
        sides.append(l[0])
    if max(sides) - min(sides) > 1e-6: return 'mixed-size', sides
    return 'strict', sides

LIB = None
def init_worker():
    global LIB
    LIB = library()

def extend(args):
    cl, restrict = args; lib = LIB
    ex = exposed(lib, cl); out = []
    targets = ex
    if restrict:
        bad = [x for x in ex if not x['eq']]
        if bad: targets = bad
        elif DEEP: return []
    for x in targets:
        for j in range(len(lib)):
            for pl in placements(lib, x, j):
                if overlaps(lib, cl, pl): continue
                out.append(cl + [pl[:3]])
    return out

def run(maxlevel=4, nproc=4):
    t0 = time.time(); lib = library()
    print('library', len(lib), [p['name'] for p in lib], flush=True)
    levels = [[[(j, np.eye(3), np.zeros(3))] for j in range(len(lib))]]
    seen = set(); lev = []
    for cl in levels[0]:
        s = signature(lib, cl)
        if s not in seen: seen.add(s); lev.append(cl)
    levels[0] = lev; results = []
    def evaluate(level_list, k):
        for cl in level_list:
            ex = exposed(lib, cl)
            # quick screen: every exposed face must be an equilateral triangle, or lie in a plane shared with other exposed
            # faces (a possible merged triangle)
            nb = [x for x in ex if not x['eq']]
            if nb:
                ok = all(sum(1 for y in ex if y is not x and abs(np.dot(y['n'], x['n']) - 1) < 1e-7 and abs(np.dot(y['n'], y['c'] - x['c'])) < 1e-7) for x in nb)
                if not ok: continue
            faces = surface_report(lib, cl); cls, sides = classify_faces(faces)
            allpieces_eq = not nb
            if cls == 'strict' or (allpieces_eq and faces is not None):
                results.append(dict(level=k, pieces=[lib[i]['name'] for i, _, _ in cl], cls=cls, nfaces=len(faces),
                                    sides=sorted(set(np.round(sides, 6))) if sides else None, cl=[(i, R.tolist(), t.tolist()) for i, R, t in cl],
                                    merged_faces=[P.tolist() for P in faces]))
    evaluate(levels[0], 1)
    with Pool(nproc, initializer=init_worker) as pool:
        for k in range(2, maxlevel + 1):
            restrict = (k == maxlevel and maxlevel >= 4) or (DEEP and k >= 3)
            chunks = pool.map(extend, [(cl, restrict) for cl in levels[-1]], chunksize=4)
            lev = []
            for ch in chunks:
                for cl in ch:
                    s = signature(lib, cl)
                    if s not in seen: seen.add(s); lev.append(cl)
            levels.append(lev); evaluate(lev, k)
            print('level', k, 'clusters', len(lev), 'results so far', len(results), '%.0fs' % (time.time() - t0), flush=True)
            if k < maxlevel:
                pickle.dump(lev, open('data/f2f-%slevel%d.pkl' % ('deep-' if DEEP else '', k), 'wb'))
    json.dump(dict(library=[p['name'] for p in lib], counts=[len(l) for l in levels], results=results), open('data/f2f-%s-L%d-results.json' % ('deep' if DEEP else 'all', maxlevel), 'w'))
    print('done', len(results), '%.0fs' % (time.time() - t0))

if __name__ == '__main__':
    run(int(sys.argv[1]) if len(sys.argv) > 1 else 4, int(sys.argv[2]) if len(sys.argv) > 2 else 4)
