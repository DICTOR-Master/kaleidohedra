"""Exact renders of four slot schemes for DICTO's three-card models, octahedron cut and cube cut (25 Nov 2026).
Cards: the planes x = 0, y = 0, z = 0; octahedron cut |u| + |v| <= 1 (corners on the two axes of the plane, DICTO's cardboard
octahedron), cube cut |u|, |v| <= 1 (the cube's middle square, corners (+-1, +-1, 0), the Resonus of the cube; the same axis segments).
Cards are drawn with no thickness; a slot is drawn as a strip of width W along its axis (the card thickness of a real model), so it shows.
A scheme gives each of the six half-axes to one of its two cards ('A' = first, 'B' = second, 'Ai'/'Bi' = that card owns the inner half
|s| < 1/2 and the other the outer half, '-' = neither) and the centre to one card, exactly as schemes.py; the pieces drawn are the
connected parts of each card's cells, and each scheme's pieces per card and outcome are asserted against the exhaustive search
(data/schemes-N4.json). Half-axes in the order +x, -x, +y, -y, +z, -z; sharers x: Y, Z; y: X, Z; z: X, Y.
Usage: python renders.py <schemes-N4.json> <out.html> <scenes.json>"""
import sys, os, json, itertools, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../2026-11-21-scutoid-stand-in/renders/scripts"))
import render3d

W, C, PULL = 1.5 / 40, 0.5, 9 / 5          # DICTO's templates: pieces 80 mm across (half 40 mm = 1), slots 1.5 mm wide, short slots 20 mm
HALF = [(a, s) for a in range(3) for s in (1, -1)]
def sharers(a): return [k for k in range(3) if k != a]
E3 = np.eye(3)
# the four schemes (the whole pair X, Z crosses on the vertical y-axis; Y is the horizontal card)
SCHEMES = {
  'W': dict(half=['Ai', 'Bi', 'Ai', 'Bi', 'Ai', 'Bi'], centre='X',
            title='Three whole cards', pull={'X': E3[0], 'Y': -E3[1], 'Z': E3[2]}),
  'a': dict(half=['Bi', 'Bi', 'A', 'B', 'A', 'A'], centre='Z',
            title="(a) DICTO's construction: A, B and C in two", pull={'X': E3[1], 'Z': -E3[1], 'Y+x': E3[0], 'Y-x': -E3[0]}),
  'b': dict(half=['B', 'B', 'A', 'B', 'A', 'A'], centre='Z',
            title='(b) Two whole cards + one card in four', pull={'X': E3[1], 'Z': -E3[1], 'Y++': np.array([1, 0, 1]) / 2 ** .5,
            'Y+-': np.array([1, 0, -1]) / 2 ** .5, 'Y-+': np.array([-1, 0, 1]) / 2 ** .5, 'Y--': np.array([-1, 0, -1]) / 2 ** .5}),
  'c': dict(half=['Bi', 'Bi', 'Bi', 'Bi', 'A', 'A'], centre='Z',
            title='(c) Closed central slot + one card in two', pull={'X': E3[0] * 0.75 + E3[1] * 0.75, 'Z': -E3[1], 'Y+x': E3[0] * 1.9, 'Y-x': -E3[0] * 1.6}),
}
COL = {0: '#c9a77c', 1: '#d8bd94', 2: '#b99467'}          # three close cardboard tans, one per card plane
EDGE = '#5e4428'

def owner(half, centre, p3):
    """card owning the shared point p3 on an axis (cells of the slot strips), or None"""
    nz = [i for i in range(3) if abs(p3[i]) > 1e-12]
    if not nz: return 'XYZ'.index(centre) if centre else None
    a = nz[0]; m = abs(p3[a]); s = 1 if p3[a] > 0 else -1
    o = half[HALF.index((a, s))]; A, B = sharers(a)
    return {'A': A, 'B': B, 'Ai': A if m < C else B, 'Bi': B if m < C else A, '-': None}[o]

def clip(poly, cut):
    if cut == 'cube': return poly
    for nu, nv in ((1, 1), (1, -1), (-1, 1), (-1, -1)):             # half-planes nu u + nv v <= 1
        out = []
        for i in range(len(poly)):
            P, Q = poly[i], poly[(i + 1) % len(poly)]; fp, fq = nu * P[0] + nv * P[1] - 1, nu * Q[0] + nv * Q[1] - 1
            if fp <= 1e-12: out.append(P)
            if (fp < -1e-12 and fq > 1e-12) or (fp > 1e-12 and fq < -1e-12):
                t = fp / (fp - fq); out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
        poly = out
        if len(poly) < 3: return []
    return poly

def card_pieces(k, half, centre, cut):
    i, j = sharers(k); B = [-1, -C, -W / 2, W / 2, C, 1]
    cells = {}
    for a in range(5):
        for b in range(5):
            um, vm = (B[a] + B[a + 1]) / 2, (B[b] + B[b + 1]) / 2
            p3 = np.zeros(3)
            if abs(um) < W / 2 and abs(vm) < W / 2: own = owner(half, centre, p3)
            elif abs(um) < W / 2: p3[j] = vm; own = owner(half, centre, p3)
            elif abs(vm) < W / 2: p3[i] = um; own = owner(half, centre, p3)
            else: own = k
            if own != k: continue
            poly = clip([(B[a], B[b]), (B[a + 1], B[b]), (B[a + 1], B[b + 1]), (B[a], B[b + 1])], cut)
            if poly: cells[(a, b)] = poly
    comps, seen = [], {(2, 2)}            # the centre cell is a point when t -> 0: it never joins two parts (as schemes.py)
    for c0 in cells:
        if c0 in seen: continue
        st, comp = [c0], {c0}; seen.add(c0)
        while st:
            a, b = st.pop()
            for q in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                if q in cells and q not in seen: seen.add(q); comp.add(q); st.append(q)
        comps.append(comp)
    if (2, 2) in cells:
        nb = [c for c in comps if any(q in c for q in ((1, 2), (3, 2), (2, 1), (2, 3)))]
        (nb[0] if nb else comps.append(set()) or comps[-1]).add((2, 2))
    comps = [[cells[c] for c in comp] for comp in comps]
    def to3(p): return p[0] * E3[i] + p[1] * E3[j]
    out = []
    for polys in comps:
        cen = np.mean([to3(p) for poly in polys for p in poly], axis=0)
        out.append((k, [[to3(p) for p in poly] for poly in polys], cen))
    return out

def piece_name(k, cen):
    n = 'XYZ'[k]; i, j = sharers(k)
    if k != 1: return n
    sx, sz = cen[0], cen[2]
    if abs(sz) < 0.05: return 'Y+x' if sx > 0 else 'Y-x'
    if abs(sx) < 0.05: return 'Y+z' if sz > 0 else 'Y-z'
    return 'Y' + ('+' if sx > 0 else '-') + ('+' if sz > 0 else '-')

def part(k, polys, shift):
    V, T, Cl, U = [], [], [], []
    def vid(p):
        p = list(np.round(np.array(p, float) + shift, 6))
        if p not in V: V.append(p)
        return V.index(p)
    segs = {}
    for poly in polys:
        ids = [vid(p) for p in poly]
        for a, b in zip(ids[1:-1], ids[2:]): T.append([ids[0], a, b]); Cl.append(COL[k])
        for m in range(len(ids)):
            e = tuple(sorted((ids[m], ids[(m + 1) % len(ids)])))
            if e[0] != e[1]: segs[e] = segs.get(e, 0) + 1
    bd = [e for e, n in segs.items() if n == 1]                       # outline: edges not shared by two cells of the piece
    for e in bd: U.append([e[0], e[1], EDGE, None])
    inc = {}
    for e in bd:
        for a in e: inc.setdefault(a, []).append(e)
    balls = []
    for a, es in inc.items():                                          # a ball where the outline turns (not on straight runs)
        if len(es) != 2: balls.append([a, EDGE]); continue
        d = [np.array(V[e[1] if e[0] == a else e[0]]) - np.array(V[a]) for e in es]
        if np.linalg.norm(np.cross(d[0], d[1])) > 1e-9 * np.linalg.norm(d[0]) * np.linalg.norm(d[1]): balls.append([a, EDGE])
    return {'v': V, 't': T, 'c': Cl, 'a': 1, 'tubes': U, 'rad': 0.0042, 'balls': balls}

def hull(P):
    P = sorted(map(tuple, P)); cr = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    def half(seq):
        H = []
        for p in seq:
            while len(H) >= 2 and cr(H[-2], H[-1], p) <= 0: H.pop()
            H.append(p)
        return H[:-1]
    return np.array(half(P) + half(P[::-1]))
def sep_gap(A, B):
    g = -1e9
    for H in (A, B):
        for i in range(len(H)):
            e = H[(i + 1) % len(H)] - H[i]; nrm = np.array([-e[1], e[0]]) / np.linalg.norm(e)
            pa, pb = A @ nrm, B @ nrm; g = max(g, pb.min() - pa.max(), pa.min() - pb.max())
    return g

if __name__ == '__main__':
    SRC, OUT, SJ = sys.argv[1:4]
    S = json.load(open(SRC))
    found = {(r['cut'], tuple(r['half']), r['centre']): r for r in S['results']}
    VO = [0.85, 0.62, 1.25]
    scenes, meta, ok = [], [], True
    for cut in ('octahedron', 'cube'):
        for key, sc in SCHEMES.items():
            P = [pc for k in range(3) for pc in card_pieces(k, sc['half'], sc['centre'], cut)]
            per = [sum(1 for k, _, _ in P if k == j) for j in range(3)]
            r = found[(cut, tuple(sc['half']), sc['centre'])]
            agree = r['pieces_per_card'] == per; ok &= agree
            names = ['XYZ'[k] if per[k] == 1 else piece_name(k, cen) for k, _, cen in P]
            assert len(set(names)) == len(names) and set(names) == set(sc['pull']), (key, names)
            whole = [part(k, polys, np.zeros(3)) for k, polys, _ in P]
            # pull 9/5 along each piece's direction, raised in steps of 1/10 until the pieces are apart IN THE PICTURE (projected hulls
            # at least 1.5 % of the frame apart); the frame half-width E is fitted to the pulled pieces (8 % margin)
            Qw = np.vstack([render3d.project(np.array(p['v']), VO, 1.0) for p in whole]) / render3d.PX * 2 - 1
            E1 = round(float(np.abs(Qw).max()) * 1.08, 3)                  # whole view: frame fitted with 8 % margin
            for f in np.arange(1, 4.01, 0.1):
                pulled = [part(k, polys, f * PULL * np.array(sc['pull'][nm], float)) for (k, polys, _), nm in zip(P, names)]
                Q = np.vstack([render3d.project(np.array(p['v']), VO, 1.0) for p in pulled]) / render3d.PX * 2 - 1
                E2 = round(float(np.abs(Q).max()) * 1.08, 3)
                H = [hull(render3d.project(np.array(p['v']), VO, E2)) for p in pulled]
                gap = min(sep_gap(a, b) for a, b in itertools.combinations(H, 2))
                inside = all(h.min() > 0 and h.max() < render3d.PX for h in H)
                if gap >= 0.015 * render3d.PX and inside: break
            print('   pull %.2f (= %.1f x 9/5), E %.3f' % (f * PULL, f, E2))
            ok &= gap >= 0.015 * render3d.PX and inside
            print('%-10s %s: pieces per card %s (search %s, %s, %s); pulled view: smallest gap between pieces %.0f px of %d, in frame %s'
                  % (cut, key, per, r['pieces_per_card'], r['outcome'], r['search'], gap, render3d.PX, inside))
            scenes += [{'E': E1, 'dir': VO, 'parts': whole}, {'E': E2, 'dir': VO, 'parts': pulled}]
            LAB = {'X': 'A', 'Z': 'B', 'Y': 'C', 'Y-x': 'C1', 'Y+x': 'C2', 'Y--': 'C1', 'Y+-': 'C2', 'Y++': 'C3', 'Y-+': 'C4'}
            labels = []
            for p, nm in zip(pulled, names):
                V = np.array(p['v']); q = render3d.project(V.mean(axis=0), VO, E2)[0]
                labels.append([LAB[nm], round(float(q[0]), 1), round(float(q[1]), 1)])
            meta += [dict(cut=cut, scheme=key, view='whole', title=sc['title'], outcome=r['outcome'], order=r['order']),
                     dict(cut=cut, scheme=key, view='pulled', title=sc['title'], outcome=r['outcome'], order=r['order'], labels=labels)]
    render3d.write(OUT, scenes); json.dump(meta, open(SJ, 'w'), indent=1)
    print('scenes', len(scenes)); print('FINAL ok' if ok else 'FINAL FAIL')
