"""Shared exact-to-50-digit geometry for branch A: C1 (truncated icosahedron edge 1 + dodecahedron centre pyramids),
C1' = C1 sharing hexagon H with edge types swapped (B2), local frame on the neighbouring hexagon H2 of C1."""
import itertools
import mpmath as mp
mp.mp.dps = 50
TOL = mp.mpf(10) ** -35
phi = (1 + mp.sqrt(5)) / 2
BETA = mp.acos(1 / mp.sqrt(6))
V = lambda *a: mp.matrix([mp.mpf(x) for x in a])
def dot(u, v): return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]
def cross(u, v): return mp.matrix([u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]])
def nrm(u): return mp.sqrt(dot(u, u))
def unit(u): return u / nrm(u)
cyc = lambda t: [(t[0], t[1], t[2]), (t[2], t[0], t[1]), (t[1], t[2], t[0])]
def build_C1():
    TV = []
    for b in [(0, 1, 3*phi), (1, 2+phi, 2*phi), (phi, 2, 2*phi+1)]:
        for sg in itertools.product((1, -1), repeat=3):
            t = tuple(sg[i]*b[i]/2 for i in range(3))
            for c in cyc(t):
                p = V(*c)
                if all(nrm(p - q) > TOL for q in TV): TV.append(p)
    assert len(TV) == 60
    pd = []
    for a, b in itertools.product((1, -1), repeat=2):
        for c in cyc((0, a, b*phi)): pd.append(unit(V(*c)))
    hd = [unit(V(*s)) for s in itertools.product((1, -1), repeat=3)]
    for a, b in itertools.product((1, -1), repeat=2):
        for c in cyc((0, a*phi, b/phi)): hd.append(unit(V(*c)))
    def face(d):
        m = max(dot(d, v) for v in TV); return [v for v in TV if abs(dot(d, v) - m) < TOL]
    pents = [face(d) for d in pd]; hexes = [face(d) for d in hd]
    assert all(len(f) == 5 for f in pents) and all(len(f) == 6 for f in hexes)
    Rd = mp.sqrt(3)*phi/2
    apex = []
    for d, f in zip(pd, pents):
        c = sum(f, V(0, 0, 0))/5; apex.append(c + mp.sqrt(Rd**2 - nrm(f[0]-c)**2)*d)
    spikes = []   # (A, B, apex) base edge = pentagon edge
    for f, ap in zip(pents, apex):
        for u, w in itertools.combinations(f, 2):
            if abs(nrm(u - w) - 1) < TOL: spikes.append((u, w, ap))
    assert len(spikes) == 60
    pyrs = [f + [ap] for f, ap in zip(pents, apex)]
    return dict(TV=TV, pents=pents, hexes=hexes, hd=hd, pd=pd, apex=apex, spikes=spikes, pyrs=pyrs)
def iso_swap(Hface):
    """reflection in the plane of hexagon H followed by a 60 deg turn about its axis (B2: types swapped)"""
    hc = sum(Hface, V(0, 0, 0))/6; hn = unit(hc)
    def f(x):
        x = x - 2*dot(x - hc, hn)*hn
        y = x - hc; a = dot(y, hn)*hn; b = y - a; c = cross(hn, b)
        return hc + a + b*mp.cos(mp.pi/3) + c*mp.sin(mp.pi/3)
    return f
def same(p, q): return nrm(p - q) < TOL
