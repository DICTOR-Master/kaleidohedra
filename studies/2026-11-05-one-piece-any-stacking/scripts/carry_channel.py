"""Route (a) pilot: the CARRY channel of one keyed down piece.
The down piece takes 6 placements per site (3 turns + 3 mirrors, the group C3v), and placement g plays tile t3(g) in x3 slabs and
t2(g) in x1/2 slabs (Culik a = 1/3 set). Row neighbours meet on side triangles: OUT (azimuth a0) of one against IN (a0 + 180) of the next.
One key pattern K on the 6 triangles (colours with a mating involution sigma) must make
    K[g^-1 OUT] mates K[h^-1 IN]   <=>   e(t(g)) == w(t(h))      for all g, h, in BOTH slab types.
For row direction we take a0 = each triangle azimuth in turn. Brute force over t3, t2 (bijections G -> tiles); keys follow (see README)."""
import numpy as np, itertools, sys
sys.path.insert(0, '.')
from fractions import Fraction as Fr
from math import floor
from n_slabs import narc, SITE, H
from scipy.spatial import ConvexHull
P = narc(SITE['A'], H, 0, 'C'); c = P[:6].mean(0)
h = ConvexHull(P); tri = {}
for s, eq in zip(h.simplices, h.equations):
    k = tuple(np.round(eq, 6))
    tri.setdefault(k, set()).update(s)
tris = [np.array(k[:3]) for k, v in tri.items() if len(v) == 3]
assert len(tris) == 6
az = [np.degrees(np.arctan2(n[1], n[0])) % 360 for n in tris]
# the group C3v about the vertical axis through the hexagon centre: rotations by 0, 120, 240 and the mirrors of N
mids = [p for p in P if abs(p[2] - H / 2) < 1e-9]; m0 = np.degrees(np.arctan2(*(mids[0][:2] - c[:2])[::-1]))
def act(g, a):   # g = (k, mirror): rotate by 120k after (optionally) mirroring in the plane at azimuth m0
    if g[1]: a = 2 * m0 - a
    return (a + 120 * g[0]) % 360
G = [(k, m) for m in (0, 1) for k in range(3)]
def idx(a): return min(range(6), key=lambda i: min(abs(az[i] - a) % 360, 360 - abs(az[i] - a) % 360))
inv = {g: next(h for h in G if all(idx(act(h, act(g, az[i]))) == i for i in range(6))) for g in G}
print('triangle azimuths', [round(a, 1) for a in az])
def tiles(q, lo, hi):
    T = set()
    for den in (97, 101, 103, 107, 211):
        for a in range(int(lo * den), int(hi * den) + 1):
            x = Fr(a, den)
            if not (lo <= x <= hi): continue
            for k in range(1, 300):
                n = floor(k * x) - floor((k - 1) * x); s = floor(k * q * x) - floor((k - 1) * q * x)
                w = q * floor((k - 1) * x) - floor((k - 1) * q * x); e = q * floor(k * x) - floor(k * q * x)
                T.add((n, s, w, e))
    return sorted(T)
T3 = tiles(Fr(3), Fr(1, 3), Fr(2, 3)); T2 = tiles(Fr(1, 2), Fr(2, 3), Fr(2))
print('tiles x3', len(T3), 'x1/2', len(T2))
def ok_row(t, a0):
    """keys exist for this slab type with row direction a0: returns face -> (out value, in value) or None"""
    OUT, IN = a0, (a0 + 180) % 360
    if idx(IN) is None: return None
    need = {}
    for g in G:
        fo = idx(act(inv[g], OUT)); fi = idx(act(inv[g], IN))
        need.setdefault(fo, {}).setdefault('e', set()).add(t[g][3])
        need.setdefault(fi, {}).setdefault('w', set()).add(t[g][2])
    pair = {}
    for f, d in need.items():
        if len(d.get('e', ())) > 1 or len(d.get('w', ())) > 1: return None   # one face, one key: one value each way
        e = next(iter(d['e'])) if 'e' in d else None; w = next(iter(d['w'])) if 'w' in d else None
        pair[f] = (e, w)
    # keys: face with out value e and in value w gets colour code(e) and must equal sigma(code(w)): e <-> w must be an involution
    sig = {}
    for e, w in pair.values():
        if e is None or w is None: continue
        if sig.get(e, w) != w or sig.get(w, e) != e: return None
        sig[e] = w; sig[w] = e
    return pair
found = 0
for a0 in sorted(set(round(a) for a in az)):
    for p3 in itertools.permutations(range(6)):
        t3 = {g: T3[p3[i]] for i, g in enumerate(G)}
        r3 = ok_row(t3, a0)
        if r3 is None: continue
        for p2 in itertools.permutations(range(6)):
            t2 = {g: T2[p2[i]] for i, g in enumerate(G)}
            r2 = ok_row(t2, a0)
            if r2 is None: continue
            # the same physical key on each face must serve both slab types: faces with equal x3 keys must have equal x1/2 keys and v.v.
            k3 = {f: r3[f][0] for f in r3}; k2 = {f: r2[f][0] for f in r2}
            if all((k3[f] == k3[g]) == (k2[f] == k2[g]) for f in k3 for g in k3):
                found += 1
                if found <= 3: print('FOUND a0', a0, 'x3', [t3[g] for g in G], 'x1/2', [t2[g] for g in G])
print('FINAL', 'carry channel feasible, solutions', found if found else 0)
