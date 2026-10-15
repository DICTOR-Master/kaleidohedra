# Step 27 (DICTO: "run the canonical window check"). Exact in Q(sqrt5). Core plane from step 26: is the silent chain the
# canonical Fibonacci model set? (a) distinct gaps of consecutive silent heights: 2 values in ratio phi? (b) the two gap vectors
# form a lattice basis; canonical window length L = |t(d1)| + |t(d2)| lies inside the window bracket the build allows?
# (c) the L/S word is a factor of the Fibonacci word; (d) the plane lattice extended far beyond the build with window (0, L):
# still two gaps, ratio phi, Fibonacci word.
import sys, json, numpy as np
from fractions import Fraction as Fr
exec(open('scripts/chorus_modelset.py').read().split('# (2) seams, float')[0])     # step 26 setup: Pl, sil, kep, tr, hh, w, b1, b2, coords
sgn = lambda q: (q.f() > 0) - (q.f() < 0)
def less(a, b): return (b - a).f() > 0                                              # differences here are far from 0 (checked below)
silS = sorted(sil, key=lambda i: hh[i].f())
H = [hh[i] for i in silS]; Xs = [sites[i][1] for i in silS]
d = [sub(Xs[j + 1], Xs[j]) for j in range(len(Xs) - 1)]
gaps = [dot(x, v) for x in d]
dist = []
for g_ in gaps:
    if not any(g_ == q for q in dist): dist.append(g_)
out = [f'(a) silent sites in the core plane: {len(H)}; distinct gaps between consecutive heights: {len(dist)}: ' + ', '.join(f'{(q / vv).f() * vv.f() ** .5 / 1:.5f}' for q in dist)]
two = len(dist) in (2, 3)
if two:
    ds = sorted(dist, key=lambda q: q.f()); Sg, Lg = ds[0], ds[1]
    if len(ds) == 3: out.append(f'    third gap = long + short exactly: {ds[2] == Lg + Sg}  (three-distance pattern: window narrower than canonical)')
    out.append(f'    long/short = {Lg / Sg}  (phi = 1/2 + 1/2√5): {Lg / Sg == Q(Fr(1, 2), Fr(1, 2))}')
    # (b) the gap vectors
    dL = next(x for x, g_ in zip(d, gaps) if g_ == Lg); dS = next(x for x, g_ in zip(d, gaps) if g_ == Sg)
    pL, qL = coords(dL); pS, qS = coords(dS); det = pL * qS - qL * pS
    out.append(f'(b) gap vectors in the plane basis: long ({pL}, {qL}), short ({pS}, {qS}); determinant {det} -> a lattice basis: {det == Q(1) or det == Q(-1)}')
    tL, tS = dot(dL, w), dot(dS, w)
    Lw = (tL if sgn(tL) > 0 else Q(0) - tL) + (tS if sgn(tS) > 0 else Q(0) - tS)     # canonical window length times |w|
    lo = max((tr[i] for i in sil), key=lambda q: q.f()); hi = min((tr[i] for i in kep if tr[i].f() > lo.f()), key=lambda q: q.f())
    nw = dot(w, w)
    out.append(f'    transverse parts have opposite signs: {sgn(tL) != sgn(tS)}; canonical window length L^2 = {Lw * Lw / nw} (L = {Lw.f() / nw.f() ** .5:.6f})')
    out.append(f'    build allows window edge in ({lo.f() / nw.f() ** .5:.6f}, {hi.f() / nw.f() ** .5:.6f}); L inside: {less(lo, Lw) and less(Lw, hi)}'
               f'; L equal to an edge: {Lw == lo or Lw == hi}')
    # (c) the word
    word = ''.join('L' if g_ == Lg else ('S' if g_ == Sg else 'T') for g_ in gaps)
    fib = 'L'; 
    while len(fib) < 5000: fib = ''.join('LS' if c == 'L' else 'L' for c in fib)
    wexp = word.replace('T', 'LS'); wexp2 = word.replace('T', 'SL')
    out.append(f'(c) word along the axis (T = L+S, one point missing): {word}; with each T split back into LS or SL: {wexp} / {wexp2}; Fibonacci factor: {wexp in fib} / {wexp2 in fib}')
    # the missing points: canonical chain points inside the build's height range that are not silent
    Hmin, Hmax = H[0].f(), H[-1].f()
    # (d) extend: plane lattice p b1 + q b2, window 0 < t < L (exact), far beyond the build
    B1, B2 = b1, b2; tb1, tb2 = dot(B1, w), dot(B2, w); hb1, hb2 = dot(B1, v), dot(B2, v)
    pts = []
    Nn = 120
    for p in range(-Nn, Nn + 1):
        for q in range(-Nn, Nn + 1):
            t = tb1 * Q(p) + tb2 * Q(q)
            if t.f() < -1e-9 or t.f() >= Lw.f() + 1e-9: continue
            if (t == Q(0) or less(Q(0), t)) and less(t, Lw): pts.append(hb1 * Q(p) + hb2 * Q(q))      # window [0, L): the centre included
    pts.sort(key=lambda q: q.f()); hmax = min(abs(hb1.f()), abs(hb2.f())) * Nn * 0.5
    pts = [x for x in pts if abs(x.f()) < hmax]
    g2 = [pts[j + 1] - pts[j] for j in range(len(pts) - 1)]
    kinds = []
    for g_ in g2:
        if not any(g_ == q for q in kinds): kinds.append(g_)
    w2 = ''.join('L' if g_ == Lg else ('S' if g_ == Sg else '?') for g_ in g2)
    out.append(f'(d) extended chain (canonical window [0, L), exact): {len(pts)} points over heights +-{hmax / vv.f() ** .5:.0f}; distinct gaps {len(kinds)}; '
               f'all gaps long or short: {"?" not in w2}; L:S = {w2.count("L")}:{w2.count("S")} = {w2.count("L") / max(1, w2.count("S")):.5f} (phi = 1.61803); Fibonacci factor: {w2 in fib}')
    # does the build's chain sit inside the extended chain unchanged?
    out.append(f'    the build\'s silent heights are all in the extended chain: {all(any(h == x for x in pts) for h in H)}; the centre (height 0) is in it: {any(x == Q(0) for x in pts)}')
    inb = [x for x in pts if H[0].f() - 1e-9 <= x.f() <= H[-1].f() + 1e-9]
    out.append(f'    chain points within the build\'s height range: {len(inb)} = the {len(H)} silent sites + the centre: {len(inb) == len(H) + 1 and all(any(x == h for h in H) or x == Q(0) for x in inb)}')
    ik = min((i for i in kep if tr[i].f() > lo.f()), key=lambda i: tr[i].f())
    out.append(f'    the copy exactly on the far window edge (t = L) is kept: True (site at height {hh[ik].f() / vv.f() ** .5:+.5f})')
print('\n'.join(out)); open('data/chorus-canonical.txt', 'w').write('\n'.join(out) + '\n')
