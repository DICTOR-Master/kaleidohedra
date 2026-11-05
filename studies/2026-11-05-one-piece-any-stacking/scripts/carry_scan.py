"""Route (a) step 2b: scan two-branch multiplier maps (Kari/Culik type) for a carry channel that ONE keyed down piece can carry.
Map on [lo, hi]: x -> q1 x on [lo, c], x -> q2 x on [c, hi] (q1 > 1 > q2, multiplicatively independent), both branches into [lo, hi].
Each branch: Beatty tiles (n, s, w, e). A down piece has 6 placements (C3v); placement g plays tile t_i(g) in slab type i; t_i onto (a tile may
be played by several placements). Keys on the 6 side triangles mate one-to-one, so (proved in step 2a) the triangles' key classes must equal the
outgoing-carry classes in BOTH slab types, and per slab the out/in carries on each key class must pair as an involution.
Reports maps with <= 6 tiles per branch, no zero tile (n = s = 0), and a joint solution. HEARTBEAT + FINAL."""
import itertools, time, sys
from fractions import Fraction as Fr
from math import floor
t0 = time.time()
def hb(m): print(f'HEARTBEAT {time.time()-t0:.0f}s {m}', flush=True)
exec(open('carry_channel.py').read().split('def tiles')[0])          # geometry: az, G, act, inv, idx
def tiles(q, lo, hi):
    T = set()
    for den in (97, 101):
        for a in range(int(lo * den), int(hi * den) + 1):
            x = Fr(a, den)
            if not (lo <= x <= hi): continue
            for k in range(1, 130):
                n = floor(k * x) - floor((k - 1) * x); s = floor(k * q * x) - floor((k - 1) * q * x)
                w = q * floor((k - 1) * x) - floor((k - 1) * q * x); e = q * floor(k * x) - floor(k * q * x)
                T.add((n, s, w, e))
    return sorted(T)
def row_maps(T, a0):
    """all onto maps G -> T that pass one slab type; returns list of (partition of triangles by key, map)"""
    OUT, IN = a0, (a0 + 180) % 360; res = []
    for assign in itertools.product(range(len(T)), repeat=6):
        if len(set(assign)) < len(T): continue
        t = {g: T[assign[i]] for i, g in enumerate(G)}
        pair = {}
        for g in G:
            fo = idx(act(inv[g], OUT)); fi = idx(act(inv[g], IN))
            pair.setdefault(fo, [None, None])[0] = t[g][3]; pair.setdefault(fi, [None, None])[1] = t[g][2]
        # key classes = out-carry classes; the in-carry must be constant on each class and pair as an involution
        cls = {}
        for f, (e, w) in pair.items(): cls.setdefault(e, set()).add(f)
        ok = True; sig = {}
        for e, fs in cls.items():
            ws = {pair[f][1] for f in fs}
            if len(ws) != 1: ok = False; break
            w = ws.pop()
            if sig.get(e, w) != w or sig.get(w, e) != e: ok = False; break
            sig[e] = w; sig[w] = e
        if ok: res.append((frozenset(frozenset(fs) for fs in cls.values()), assign))
    return res
Q = [Fr(2), Fr(3), Fr(3, 2), Fr(4, 3), Fr(5, 2), Fr(5, 3)]
cands = []
for q1 in Q:
    for q2 in [1 / q for q in Q] + [Fr(2, 3), Fr(3, 4), Fr(2, 5), Fr(3, 5)]:
        if q2 >= 1 or q1 * q2 == 1: continue
        for lo in (Fr(1, 4), Fr(1, 3), Fr(2, 5), Fr(1, 2), Fr(2, 3), Fr(3, 4), Fr(1)):
            for hi in (2 * lo, Fr(5, 2) * lo, 3 * lo, 4 * lo, 6 * lo):
                c = hi / q1
                if not (lo < c < hi) or q2 * c < lo or q2 * hi > hi or q1 * lo < lo: continue
                if q2 * hi < lo: continue
                cands.append((q1, q2, lo, c, hi))
hb(f'{len(cands)} maps')
hits = 0
for q1, q2, lo, c, hi in cands:
    T1 = tiles(q1, lo, c)
    if len(T1) > 6: continue
    T2 = tiles(q2, c, hi)
    if len(T1) > 6 or len(T2) > 6: continue
    if any(t[0] == 0 and t[1] == 0 for t in T1 + T2): continue
    for a0 in (0, 60):
        R1 = {}; [R1.setdefault(p, m) for p, m in row_maps(T1, a0)]
        R2 = {}; [R2.setdefault(p, m) for p, m in row_maps(T2, a0)]
        common = set(R1) & set(R2)
        hb(f'x{q1} [{lo},{c}] / x{q2} [{c},{hi}]: tiles {len(T1)}+{len(T2)}, row direction {a0}: partitions {len(R1)} / {len(R2)}, common {len(common)}')
        if common: hits += 1
print('FINAL', f'{hits} map(s) with a joint carry channel' if hits else 'no map with a joint carry channel', f'{time.time()-t0:.0f}s', flush=True)
