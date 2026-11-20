"""Step 2 (computed, 60 digits): where the arrangement of the sides changes along the rhombus members, c = u^2 in (0, 0.76).
Lines are the 27 full lines (base, left leg, right leg of t1..t9).  A triple of lines is an IDENTITY if |det| < 1e-40 at every
scan point (the exact concurrencies and parallel pairs of the model).  A triple matters for the SIDES (segments) only if, where it
becomes concurrent, the meeting point lies on all three sides; only those can change the regions.  For every such triple whose
det changes sign between scan points, the event c is solved to 55 digits (bisection then secant on that det alone, the member
followed by continuity) and the counts are taken just below and above.  Writes data/events.json.  usage: python s2_events.py N"""
import sys, os, json, time, itertools
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mpmath as mp
from multiprocessing import Pool
mp.mp.dps = 60
import yfam as Y
N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
CMAX = mp.mpf('0.76')

def member(c):
    u = mp.sqrt(c); ms = Y.members(u, u)
    assert len(ms) == 1, ('members', len(ms), c)
    return ms[0]

def one_det(y, k):
    L = Y.lines(y)
    if k[2] == 'inf':
        A, B = Y.hom(L[k[0]]), Y.hom(L[k[1]]); return A[0] * B[1] - A[1] * B[0]
    A, B, C = (Y.hom(L[n]) for n in k)
    return A[0] * (B[1] * C[2] - B[2] * C[1]) - A[1] * (B[0] * C[2] - B[2] * C[0]) + A[2] * (B[0] * C[1] - B[1] * C[0])

def on_sides(y, k, slack=mp.mpf(10) ** -12):
    """Meeting point of the first two lines of k lies on all three sides (segments), within slack."""
    if k[2] == 'inf': return False
    L = Y.lines(y); A, B = Y.hom(L[k[0]]), Y.hom(L[k[1]])
    den = A[0] * B[1] - A[1] * B[0]
    if abs(den) < mp.mpf(10) ** -30: return False
    x = (A[1] * B[2] - A[2] * B[1]) / den; d = (A[2] * B[0] - A[0] * B[2]) / den
    for n in k:
        (x1, y1), (x2, y2) = L[n]
        if not (min(x1, x2) - slack <= x <= max(x1, x2) + slack and min(y1, y2) - slack <= d <= max(y1, y2) + slack): return False
    return True

def job(c):
    mp.mp.dps = 60
    c = mp.mpf(c); y = member(c)
    return c, Y.dets(y)

def refine(arg):
    mp.mp.dps = 60
    lo, hi, k = mp.mpf(arg[0]), mp.mpf(arg[1]), tuple(arg[2])
    g = lambda c: one_det(member(c), k)
    flo = g(lo)
    for _ in range(40):
        mid = (lo + hi) / 2; fm = g(mid)
        if mp.sign(fm) == mp.sign(flo): lo, flo = mid, fm
        else: hi = mid
    cs = mp.findroot(g, (lo, hi), solver='secant', tol=mp.mpf(10) ** -110)
    y = member(cs)
    return dict(c=mp.nstr(cs, 55), lines=list(k), on_sides=on_sides(y, k), residual=mp.nstr(g(cs), 3))

if __name__ == '__main__':
    t0 = time.time()
    cs = [mp.nstr(CMAX * k / N, 30) for k in range(1, N)]
    with Pool(22) as pool:
        res = pool.map(job, cs, chunksize=2)
        keys = list(res[0][1].keys()); tiny = mp.mpf(10) ** -40
        ident = [k for k in keys if all(abs(r[1][k]) < tiny for r in res)]
        live = [k for k in keys if k not in ident]
        print('identities (zero at every scan point):', len(ident), '= triples', sum(k[2] != 'inf' for k in ident),
              '+ parallel pairs', sum(k[2] == 'inf' for k in ident), flush=True)
        changes = [(mp.nstr(res[j][0], 40), mp.nstr(res[j + 1][0], 40), list(k)) for j in range(len(res) - 1) for k in live
                   if mp.sign(res[j][1][k]) * mp.sign(res[j + 1][1][k]) < 0]
        print('sign changes of line triples (full lines) between scan points:', len(changes), f'{time.time()-t0:.0f}s', flush=True)
        ev = pool.map(refine, changes, chunksize=1)
    rel = sorted([e for e in ev if e['on_sides']], key=lambda e: mp.mpf(e['c']))
    print('of these, meeting point on all three sides (can change regions):', len(rel), f'{time.time()-t0:.0f}s', flush=True)
    groups = []
    for e in rel:
        if groups and abs(mp.mpf(groups[-1][0]['c']) - mp.mpf(e['c'])) < mp.mpf(10) ** -40: groups[-1].append(e)
        else: groups.append([e])
    out = []
    for gp in groups:
        c = mp.mpf(gp[0]['c']); sides = []
        for dc in (-mp.mpf(10) ** -8, mp.mpf(10) ** -8):
            y = member(c + dc); r = Y.regions(y); m, s = Y.counts_traditional(y)
            sides.append(dict(odd=r['odd'], odd_tri=r['odd_tri'], faces=r['faces'], marma=m, sandhi=s))
        tag = '' if sides[0] == sides[1] else '   <-- COUNT CHANGES'
        print(f"event c = {mp.nstr(c, 30)} (u = {mp.nstr(mp.sqrt(c), 22)}): {[tuple(e['lines']) for e in gp]}{tag}")
        print(f"     below {sides[0]}\n     above {sides[1]}")
        out.append(dict(c=gp[0]['c'], u=mp.nstr(mp.sqrt(c), 55), triples=[e['lines'] for e in gp], below=sides[0], above=sides[1]))
    json.dump(dict(N=N, identities=[list(k) for k in ident], events=out, all_changes=len(changes)),
              open(os.path.join(Y.ROOT, 'data', 'events.json'), 'w'), indent=1)
    print(f'time {time.time()-t0:.0f}s'); print('FINAL ok' if out else 'FINAL FAIL (no events)')
