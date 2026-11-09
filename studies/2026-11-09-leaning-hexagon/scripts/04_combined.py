"""04: COMBINATION (DICTO 9 Nov: "maybe combination can provide the extra impetus"): leaning sides (lean matching on the
walls, in the plane, <= 12 placements per site) PLUS the ABC waveform of the abc-waveform study: crest planes fixed in
the piece, carried by every placement, matched on the top/bottom plates (between layers).

Crest planes (piece frame, coordinates (i, j, z), z in twelfths of a layer), as in wave_lib.py adapted to the plate
carrier:  tilted close-packed crests = planes containing a row direction AC[t] (t = 0, 1, 2) and the seat step up one
layer (D_u, 12) (u = 0..5: lean B-ward for u even, C-ward for u odd), at offsets through the plate vertices of the
piece; horizontal crests z = e.  Designs: the empty control, every single plane, every pair as one wave (one colour)
and as a two-wave mix (two colours).
Rules per shared plate triangle (as wave_lib.py):  STRICT  the set of crest planes (with colours) cutting the triangle
is the same from below and from above;  BEND  only the crest LINES on the triangle (with colours) agree.
Carriers (leaning pieces that tile, proper motions only, <= 12 placements):
  RD + six sides leaning (shear (1,0));  E6u0 + six sides leaning;  FLAT + six sides leaning;
  FLAT + stripe lean (rows, forced h);  FLAT + stripe(-1,0,0,-1,0,0) with centre lean (-1,0) (every layer step
  changes the lean pattern, 03 D).
Battery as in 02 (patches 5 layers radius 2, every lean word; periodic tilings with in-plane lattice of index <= 3).
"""
import sys, os, time, json, itertools
from fractions import Fraction as Fr
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pieces import *
import multiprocessing as mp

t0 = time.time()
PILOT = 'pilot' in sys.argv
OUT = os.path.join(HERE, '..', 'data')
ok = True
REL = reliefs()
CARRIERS = {
    'RD-shear': make(*REL['RD'], shear((1, 0)), (1, 0)),
    'E6u0-shear': make(*REL['E6u0'], shear((1, 0)), (1, 0)),
    'FLAT-shear': make(*REL['FLAT'], shear((1, 0)), (1, 0)),
    'FLAT-stripe': make(*REL['FLAT'], stripe((0, 0)), (1, 0)),
    'FLAT-stripe2': make(*REL['FLAT'], corner_leans((-1, 0), (-1, 0, 0, -1, 0, 0)), (-1, 0)),
}


def mat(f):
    a, b = f((1, 0)), f((0, 1))
    return ((a[0], b[0]), (a[1], b[1]))


def inv2(Mx):
    (p, q), (r, s) = Mx
    d = p * s - q * r
    assert d in (1, -1)
    return ((s * d, -q * d), (-r * d, p * d))


def norm_plane(a, b, c, e):
    g = gcd(gcd(abs(a), abs(b)), gcd(abs(c), abs(e))) or 1
    t = (a // g, b // g, c // g, e // g)
    for x in t:
        if x != 0:
            if x < 0:
                t = tuple(-y for y in t)
            break
    return t


def place_c(piece, g):
    base = place_l(piece[:4], g)
    r, m, z = g
    Fi = inv2(mat(planar(r, m)))
    out = []
    for (a, b, c, e, col) in piece[4]:
        a2 = a * Fi[0][0] + b * Fi[1][0]
        b2 = a * Fi[0][1] + b * Fi[1][1]
        c2 = -c if z else c
        out.append(norm_plane(a2, b2, c2, e) + (col,))
    return base + (tuple(sorted(out)),)


def states_c(piece):
    seen = {}
    for g in G_PROPER:
        Q = place_c(piece, g)
        seen.setdefault(Q, g)
    return list(seen.keys())


def crest_sig(planes, tri_pts, rule):
    """planes in the lower frame; tri_pts = 3 points (i, j, z).  STRICT: set of cutting planes; BEND: set of traces."""
    sig = set()
    for (a, b, c, e, col) in planes:
        vals = [a * p[0] + b * p[1] + c * p[2] - e for p in tri_pts]
        if not (min(vals) < 0 < max(vals)):
            continue
        if rule == 'STRICT':
            sig.add((a, b, c, e, col))
        else:
            pts = set()
            for k in range(3):
                p, q = tri_pts[k], tri_pts[(k + 1) % 3]
                vp, vq = vals[k], vals[(k + 1) % 3]
                if vp == 0:
                    pts.add(tuple(Fr(x) for x in p))
                elif vp * vq < 0:
                    t = Fr(vp, vp - vq)
                    pts.add(tuple(Fr(p[i]) + t * (q[i] - p[i]) for i in range(3)))
            sig.add((frozenset(pts), col))
    return frozenset(sig)


def inter_table_c(sts, rule):
    base = inter_table([s[:4] for s in sts])
    n = len(sts)
    tops = [[dict(x) for x in st[0]] for st in sts]
    out = {}
    for d, Cd in base.items():
        new = [[0] * n for _ in range(6)]
        for s in range(6):
            tris = [TRI[(s - 1) % 6], TRI[s]]
            for il in range(n):
                m = Cd[s][il]
                if not m:
                    continue
                for iu in range(n):
                    if not m >> iu & 1:
                        continue
                    good = True
                    up = [(a, b, c, e + a * D[s][0] + b * D[s][1] + 12 * c, col) for (a, b, c, e, col) in sts[iu][4]]
                    up = [norm_plane(*p[:4]) + (p[4],) for p in up]
                    for T in tris:
                        Tl = sorted(T)
                        pts = [(v[0], v[1], tops[il][sec(T)][v]) for v in Tl]
                        if crest_sig(sts[il][4], pts, rule) != crest_sig(up, pts, rule):
                            good = False
                            break
                    if good:
                        new[s][il] |= 1 << iu
        if any(any(row) for row in new):
            out[d] = new
    return out


def battery_c(piece, rule, patch=(5, 2), maxidx=3):
    sts = states_c(piece)
    n = len(sts)
    T = inlayer_table([s[:4] for s in sts])
    C = inter_table_c(sts, rule)
    res = {'states': n}
    if not C:
        res.update(verdict='NO PATCH', patch_words=[])
        return res
    K, R = patch
    adm = []
    for w in itertools.product((1, 2), repeat=K - 1):
        if w[0] != 1:
            continue
        cells, con_k, il = lean_patch(w, R)
        if sat_lean(len(cells), n, con_k, il, T, C, K - 1)[0]:
            adm.append(''.join('c' if w[i] == w[i - 1] else 'h' for i in range(1, len(w))))
    res['patch_words'] = adm
    if not adm:
        res['verdict'] = 'NO PATCH'
        return res
    skipped = []
    for M in hnf(maxidx):
        r = periodic_alive_l(T, C, n, M)
        if r is None:
            skipped.append(M)
            continue
        alive, edges, V = r
        if alive:
            res.update(verdict=f'PERIODIC-{M[0]*M[2]}', M=M, periodic_words=ch_words(edges, 4),
                       uniform_layers_stack=(M == (1, 0, 1)))
            return res
    res['verdict'] = 'CANDIDATE' if not skipped else 'UNDECIDED'
    res['skipped'] = skipped
    return res


def crest_menu(piece):
    top = [dict(s) for s in piece[0]]
    pts = {(v[0], v[1], top[s][v]) for s in range(6) for v in top[s]}
    menu = []
    for t in range(3):
        r_ = AC[t]
        a0 = (r_[1], -r_[0])
        for u in range(6):
            a, b = 12 * a0[0], 12 * a0[1]
            c = -(a0[0] * D[u][0] + a0[1] * D[u][1])
            vals = sorted({a * p[0] + b * p[1] + c * p[2] for p in pts})
            # offsets: through plate vertices (lowest, middle, highest value) - only planes that can cut the top
            for e in sorted({vals[len(vals) // 2], (vals[0] + vals[len(vals) // 2]) // 2,
                             (vals[-1] + vals[len(vals) // 2]) // 2}):
                menu.append(norm_plane(a, b, c, e))
    hz = sorted({p[2] for p in pts})
    for e in sorted({hz[len(hz) // 2]} | ({(hz[0] + hz[-1]) // 2} if len(hz) > 1 else set())):
        menu.append(norm_plane(0, 0, 1, e))
    return sorted(set(menu))


def designs(menu):
    out = [()]
    for p in menu:
        out.append((p + (0,),))
    for p, q in itertools.combinations(menu, 2):
        out.append((p + (0,), q + (0,)))
        out.append((p + (0,), q + (1,)))
    return out


TASKS = []
for cn, P in CARRIERS.items():
    menu = crest_menu(P)
    ds = designs(menu)
    for k, d in enumerate(ds):
        for rule in ('STRICT', 'BEND'):
            TASKS.append((cn, d, rule))
    print(f'carrier {cn}: {len(menu)} crest planes, {len(ds)} designs')
if PILOT:
    TASKS = [t for t in TASKS if t[1] == ()] + TASKS[1::max(1, len(TASKS) // 120)]
print(f'tasks {len(TASKS)}')


def run(task):
    cn, d, rule = task
    t = time.time()
    r = battery_c(CARRIERS[cn] + (d,), rule)
    r.update(carrier=cn, design=d, rule=rule, sec=round(time.time() - t, 2))
    return r


res = []
with mp.get_context('fork').Pool(22) as pool:
    for k, r in enumerate(pool.imap_unordered(run, TASKS, chunksize=8)):
        res.append(r)
        if k % 2000 == 0:
            print(f'  heartbeat {k}/{len(TASKS)} {time.time()-t0:.0f}s', flush=True)
json.dump(res, open(os.path.join(OUT, '04_combined_pilot.json' if PILOT else '04_combined.json'), 'w'), default=list)
# controls: empty design = leaning carrier alone (periodic, as in 02)
for r in res:
    if r['design'] == ():
        print(f'control {r["carrier"]} {r["rule"]} empty design: {r["verdict"]} words {r["patch_words"]}')
        ok &= r['verdict'].startswith('PERIODIC')
summ = {}
for r in res:
    key = (r['carrier'], r['rule'], r['verdict'].split('-')[0], ' '.join(sorted(r['patch_words'])))
    summ[key] = summ.get(key, 0) + 1
print('carrier, rule, verdict, patch words (length 3): designs')
for k, c in sorted(summ.items()):
    print('  ', k, c)
til = [r for r in res if r['verdict'].startswith('PERIODIC')]
nonuni = [r for r in til if not r.get('uniform_layers_stack')]
print(f'tiling designs: {len(til)}; of these with NO periodic tiling from uniform layers (index-1 lattice dead): '
      f'{len(nonuni)}')
pw = {}
for r in til:
    k = (r['carrier'], r['verdict'], ' '.join(r['periodic_words']))
    pw[k] = pw.get(k, 0) + 1
print('periodic: carrier, smallest lattice, words of length 4: designs')
for k, c in sorted(pw.items()):
    print('  ', k, c)
cands = [r for r in res if r['verdict'] in ('CANDIDATE', 'UNDECIDED')]
print('CANDIDATE / UNDECIDED:', len(cands))
for r in cands[:20]:
    print('   ', r['carrier'], r['rule'], r['design'], r['verdict'], r['patch_words'], r.get('skipped'))
print(f'max battery {max(r["sec"] for r in res):.1f}s; total {time.time()-t0:.0f}s')
print('FINAL ok' if ok else 'FINAL FAIL: a control (empty design) did not tile periodically')
