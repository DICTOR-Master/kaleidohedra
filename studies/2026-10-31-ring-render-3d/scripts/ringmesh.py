# True 3D meshes of DICTO's PET-bottle-cap security-ring builds (2026-10-31).
# Each ring = a closed band: a rounded-triangle centreline in the face plane (its straight parts on the ring triangle's sides,
# where neighbouring rings touch), swept across by the band height h along a band direction d, with wall thickness w on the
# ring's inner side. d = face normal tilted about the centreline tangent by phi:
#   side shared with a ring of the same face (or a free side): phi = +cone for corner rings, -cone for the central ring
#   (central ring turned over, DICTO; corner rings: wide rim outside the solid -- my choice, a top view cannot tell);
#   side on an edge of the solid: phi turns the band into the bisector plane of the two faces, so the two bands lie face to
#   face (what the photos show: bands twist at the solid's edges and around its vertices);
#   phi is blended smoothly through each rounded corner.
# Inner tabs: 9 per ring, equally spaced (one at each side midpoint), hinged at the narrow rim, standing square to the face.
# Zip ties: a strap loop around both walls at the two tie points of every shared side, square head on the outside;
# open variant: one more tie around the two touching tips at each big-edge midpoint.
# All lengths below in units of the ring side s.  Output: Wavefront OBJ (objects Rings, Straps, Heads), metres.
import json, math, sys
import numpy as np

P = dict(h=0.16, w=0.016, cone=0.10, r=0.20, r_tip=0.07, tie_at=0.32, ntab=9, tab_len=0.11, tab_h=0.6, tab_t=0.012,
         tab_gap=0.006, strap_w=0.05, strap_t=0.014, clear=0.003, head=(0.075, 0.08, 0.055), blend=0.10, N=180)
S_M = 0.040        # ring side in metres (a security ring of ~29 mm diameter pulled into a triangle: perimeter 2.26 s)

def unit(v): v = np.asarray(v, float); return v / np.linalg.norm(v)

# ---------------- models (lattice units; ring side = 1/2) ----------------
def big_face(A, B, C, n, open_=False):
    m = lambda p, q: (p + q) / 2
    ab, bc, ca = m(A, B), m(B, C), m(C, A)
    out = [dict(T=[A, ab, ca], n=n, central=False), dict(T=[ab, B, bc], n=n, central=False),
           dict(T=[ca, bc, C], n=n, central=False)]
    if not open_: out.append(dict(T=[ab, bc, ca], n=n, central=True))
    return out

def bipyramid(open_=False):
    E = [np.array([0, 0, 0.]), np.array([1, 0, 0.]), np.array([.5, 3 ** .5 / 2, 0])]
    c = np.mean(E, 0); H = (2 / 3) ** .5
    A, B = c + [0, 0, H], c - [0, 0, H]; rings = []
    for X in (A, B):
        for i in range(3):
            P1, P2 = E[i], E[(i + 1) % 3]; n = unit(np.cross(P2 - P1, X - P1))
            if n @ (P1 - c) < 0: n = -n
            for r in big_face(X, P1, P2, n, open_): r['face'] = len(rings) // (3 if open_ else 4); rings.append(r)
    for r in rings: r['T'] = [p - c for p in r['T']]
    return rings, (np.vstack([E, [A, B]]) - c)

def load_rings(path):
    J = json.load(open(path)); rings = []
    for r in J['rings']:
        rings.append(dict(T=[np.array(p) for p in r['T']], n=np.array(r['n']), central=r['central'], face=r['face']))
    return rings

# ---------------- ring centreline ----------------
class Ring:
    def __init__(self, T, n, central, L, phis, radii):
        T = [np.asarray(p, float) for p in T]; self.n = unit(n); self.central = central; self.L = L
        cen = np.mean(T, 0); self.cen = cen
        # walk: side j from T[j] to T[j+1]; corner k at T[k]
        segs = []                                     # (kind, data, length)
        tp = {}
        for k in range(3):
            a, b, c = T[k - 1], T[k], T[(k + 1) % 3]; R = radii[k] * L
            u1, u2 = unit(a - b), unit(c - b); tl = R * 3 ** .5
            tp[k] = (b + u1 * tl, b + u2 * tl, b + unit(u1 + u2) * 2 * R, R)
        for j in range(3):
            k2 = (j + 1) % 3
            p0 = tp[j][1]; p1 = tp[k2][0]
            segs.append(('L', (p0, p1, j), np.linalg.norm(p1 - p0)))
            C0 = tp[k2][2]; R = tp[k2][3]
            a0 = p1 - C0; a1 = tp[k2][1] - C0
            ang = math.acos(np.clip(unit(a0) @ unit(a1), -1, 1))
            segs.append(('A', (C0, a0, a1, ang, j, k2), R * ang))
        self.segs = segs; self.total = sum(s[2] for s in segs)
        self.phis = phis
        # blend zones: around corner after side j, from (end of side j - b) to (start of side j+1 + b)
        acc = 0; self.zones = []
        for i, s in enumerate(segs):
            if s[0] == 'A':
                b = P['blend'] * L
                self.zones.append((acc - b, acc + s[2] + b, s[1][4], (s[1][4] + 1) % 3))
            acc += s[2]

    def at(self, sarc):
        sarc %= self.total; acc = 0
        for s in self.segs:
            if sarc <= acc + s[2] + 1e-12: break
            acc += s[2]
        x = sarc - acc
        if s[0] == 'L':
            p0, p1, j = s[1]; t = unit(p1 - p0); c = p0 + t * x
        else:
            C0, a0, a1, ang, j, k2 = s[1]; R = np.linalg.norm(a0)
            e1 = unit(a0); e2 = unit(a1 - (a1 @ e1) * e1); th = x / R
            c = C0 + R * (math.cos(th) * e1 + math.sin(th) * e2); t = unit(-math.sin(th) * e1 + math.cos(th) * e2)
        o = unit(np.cross(t, self.n))
        if o @ (c - self.cen) < 0: o = -o                     # in-plane outward
        phi = self.phi_at(sarc)
        d = math.cos(phi) * self.n + math.sin(phi) * o
        m = math.sin(phi) * self.n - math.cos(phi) * o          # toward the ring's inside, square to d
        return c, t, o, d, m, phi

    def phi_at(self, sarc):
        for a, b, j1, j2 in self.zones:
            for off in (0, self.total, -self.total):
                x = sarc + off
                if a <= x <= b:
                    tau = (x - a) / (b - a); w = tau * tau * (3 - 2 * tau)
                    return self.phis[j1] * (1 - w) + self.phis[j2] * w
        # on a straight side: which one?
        acc = 0
        for s in self.segs:
            if sarc <= acc + s[2] + 1e-12:
                return self.phis[s[1][2] if s[0] == 'L' else s[1][4]]
            acc += s[2]
        return self.phis[0]

    def nearest(self, p, n=400):
        best = None
        for i in range(n):
            sa = self.total * i / n; c = self.at(sa)[0]; dd = np.linalg.norm(c - p)
            if best is None or dd < best[0]: best = (dd, sa)
        return best[1]

# ---------------- mesh accumulation ----------------
class Mesh:
    def __init__(self): self.V = []; self.F = []
    def add_loop_tube(self, rows, closed=True):
        """rows: list of K-point cross-sections (same K, closed polygon each); sweeps a closed tube"""
        base = len(self.V); K = len(rows[0]); n = len(rows)
        for r in rows: self.V += [tuple(p) for p in r]
        for i in range(n if closed else n - 1):
            i2 = (i + 1) % n
            for k in range(K):
                k2 = (k + 1) % K
                self.F.append((base + i * K + k, base + i2 * K + k, base + i2 * K + k2, base + i * K + k2))
        if not closed:
            self.F.append(tuple(base + k for k in range(K))[::-1]); self.F.append(tuple(base + (n - 1) * K + k for k in range(K)))
    def add_box(self, c, ex, ey, ez):
        base = len(self.V)
        for sx in (-1, 1):
            for sy in (-1, 1):
                for sz in (-1, 1): self.V.append(tuple(c + sx * ex + sy * ey + sz * ez))
        for f in ((0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)):
            self.F.append(tuple(base + i for i in f))

def key(p): return tuple(np.round(p, 6))

def build(rings, open_=False, N=None, scale=None, tabs=True, ties=True):
    """rings in lattice units (ring side L); returns dict of Mesh (coordinates scaled so that L -> S_M metres)"""
    N = N or P['N']
    L = np.linalg.norm(np.asarray(rings[0]['T'][1]) - rings[0]['T'][0])
    sc = (scale or S_M) / L
    sides = {}
    for i, r in enumerate(rings):
        for j in range(3):
            a, b = r['T'][j], r['T'][(j + 1) % 3]; sides.setdefault(tuple(sorted((key(a), key(b)))), []).append((i, j))
    alpha = math.atan2(P['cone'], P['h'])
    objs = []
    # tip contacts (open variant): rings of one face sharing exactly one vertex
    tipv = {}
    if open_:
        for i, r in enumerate(rings):
            for k, p in enumerate(r['T']): tipv.setdefault((r['face'], key(p)), []).append((i, k))
    for i, r in enumerate(rings):
        phis = []
        for j in range(3):
            a, b = r['T'][j], r['T'][(j + 1) % 3]; nb = [x for x in sides[tuple(sorted((key(a), key(b))))] if x[0] != i]
            base = alpha * (-1 if r['central'] else 1)
            if nb and np.linalg.norm(rings[nb[0][0]]['n'] - r['n']) > 1e-6:
                d = unit(r['n'] + rings[nb[0][0]]['n']); t = unit(b - a)
                o = unit(np.cross(t, r['n'])); o = o if o @ ((a + b) / 2 - np.mean(r['T'], 0)) > 0 else -o
                phis.append(math.atan2(d @ o, d @ r['n']))
            else: phis.append(base)
        radii = [P['r']] * 3
        if open_:
            for k, p in enumerate(r['T']):
                if len(tipv.get((r['face'], key(p)), [])) == 2: radii[k] = P['r_tip']
        objs.append(Ring(r['T'], r['n'], r['central'], L, phis, radii))
    M = {'Rings': Mesh(), 'Straps': Mesh(), 'Heads': Mesh()}
    h, w = P['h'] * L, P['w'] * L
    for R in objs:
        rows = []
        for q in range(N):
            c, t, o, d, m, phi = R.at(R.total * q / N)
            rows.append([c - d * h / 2, c + d * h / 2, c + d * h / 2 + m * w, c - d * h / 2 + m * w])
        M['Rings'].add_loop_tube(rows)
        if tabs:
            sig = 1 if R.central else -1                                        # narrow rim at v = sig*h/2
            # tab centres: side midpoints and equal spacing
            s_mid = R.segs[0][2] / 2; step = R.total / P['ntab']; tl = P['tab_len'] * L
            for k in range(P['ntab']):
                s0 = s_mid + k * step; rows = []
                for q in range(7):
                    sa = s0 - tl / 2 + tl * q / 6; c, t, o, d, m, phi = R.at(sa)
                    ang = phi + sig * alpha; dt = math.cos(ang) * R.n + math.sin(ang) * o
                    mt = math.sin(ang) * R.n - math.cos(ang) * o
                    b0 = c + d * sig * h / 2 + m * (w + P['tab_gap'] * L)
                    b1 = b0 - sig * dt * P['tab_h'] * h
                    tt = P['tab_t'] * L
                    rows.append([b0, b1, b1 + mt * tt, b0 + mt * tt])
                M['Rings'].add_loop_tube(rows, closed=False)
    if ties:
        def wall(Ri, p):
            sa = Ri.nearest(p); c, t, o, d, m, phi = Ri.at(sa)
            return [c - d * h / 2, c + d * h / 2, c + d * h / 2 + m * w, c - d * h / 2 + m * w], t
        def tie(pts, t, nout):
            from shapely.geometry import MultiPoint
            e1 = unit(nout - (nout @ t) * t); e2 = np.cross(t, e1); ctr = np.mean(pts, 0)
            q2 = [((p - ctr) @ e1, (p - ctr) @ e2) for p in pts]
            hull = MultiPoint(q2).convex_hull.buffer(P['clear'] * L + P['strap_t'] * L / 2, join_style=1, quad_segs=6)
            ring = hull.exterior; K = 40
            loop = [np.array(ring.interpolate(ring.length * k / K).coords[0]) for k in range(K)]
            rows = []
            for k in range(K):
                p2 = loop[k]; tg = loop[(k + 1) % K] - loop[k - 1]; nn = np.array([tg[1], -tg[0]]); nn /= np.linalg.norm(nn)
                if (p2 - np.mean(loop, 0)) @ nn < 0: nn = -nn
                P3 = ctr + p2[0] * e1 + p2[1] * e2; N3 = nn[0] * e1 + nn[1] * e2
                hw, ht = P['strap_w'] * L / 2, P['strap_t'] * L / 2
                rows.append([P3 - N3 * ht - t * hw, P3 + N3 * ht - t * hw, P3 + N3 * ht + t * hw, P3 - N3 * ht + t * hw])
            M['Straps'].add_loop_tube(rows)
            k = int(np.argmax([lp[0] for lp in loop])); p2 = loop[k]
            P3 = ctr + p2[0] * e1 + p2[1] * e2; hd = P['head']
            tg = unit((loop[(k + 1) % K] - loop[k - 1])[0] * e1 + (loop[(k + 1) % K] - loop[k - 1])[1] * e2)
            M['Heads'].add_box(P3 + e1 * (hd[2] - P['strap_t']) * L / 2, t * hd[0] * L / 2, tg * hd[1] * L / 2, e1 * hd[2] * L / 2)
        for (ka, kb), lst in sides.items():
            if len(lst) != 2: continue
            (i, j), (i2, j2) = lst; a, b = rings[i]['T'][j], rings[i]['T'][(j + 1) % 3]
            for f in (P['tie_at'], 1 - P['tie_at']):
                p = a + (b - a) * f
                w1, t1 = wall(objs[i], p); w2, _ = wall(objs[i2], p)
                tie(w1 + w2, unit(b - a), rings[i]['n'] + rings[i2]['n'])
        if open_:
            for (fc, kp), lst in tipv.items():
                if len(lst) != 2: continue
                (i, k), (i2, k2) = lst; p = rings[i]['T'][k]
                w1, _ = wall(objs[i], p); w2, _ = wall(objs[i2], p)
                t = unit(np.cross(rings[i]['n'], objs[i].cen - objs[i2].cen))
                tie(w1 + w2, t, rings[i]['n'])
    for k in M: M[k].V = [tuple(np.array(v) * sc) for v in M[k].V]
    return M

def write_obj(M, path):
    with open(path, 'w') as f:
        off = 1
        for name, m in M.items():
            f.write(f'o {name}\n')
            for v in m.V: f.write('v %.6f %.6f %.6f\n' % v)
            for fc in m.F: f.write('f ' + ' '.join(str(off + i) for i in fc) + '\n')
            off += len(m.V)

if __name__ == '__main__':
    # usage: ringmesh.py bipyramid|bipyramid-open|<rings.json> out.obj [params.json]
    if len(sys.argv) > 3: P.update(json.load(open(sys.argv[3])))
    if sys.argv[1].startswith('bipyramid'):
        rings, _ = bipyramid(open_=sys.argv[1].endswith('open')); op = sys.argv[1].endswith('open')
    else: rings = load_rings(sys.argv[1]); op = False
    M = build(rings, open_=op); write_obj(M, sys.argv[2])
    print(sys.argv[2], {k: (len(m.V), len(m.F)) for k, m in M.items()}, 'rings', len(rings))
