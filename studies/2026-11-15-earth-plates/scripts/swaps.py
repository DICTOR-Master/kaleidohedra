"""Swap counting rules for the Earth stream of "One tissue, three scales" (DICTO, 15 Nov 2026). Post-processing of an event log
made by eventlog.py (../../2026-11-15-event-logger/scripts); eventlog's own behaviour is not changed here.
RULES (stated before counting):
  * swap through a four-fold meeting: with a minimum boundary length, a shrinking boundary is removed before the new one is long
    enough to count, so one swap shows as "one contact lost" at one step and "one contact gained" at a later step. The two are
    joined into one swap when the gained pair (c, d) were both neighbours of the lost pair (a, b) before, a and b are both
    neighbours of c and d after, and a, b, c, d meet at one junction in every frame in between;
  * persistence k (Myr): a swap counts only when the contact it removes had lasted at least k Myr and the contact it creates lasts
    at least k Myr (two-sided, so a swap and its quick reversal both drop out). "Lasts" = present (with at least as many shared
    boundaries) in consecutive frames of the same series, frames x step >= k. A contact that runs into the start or the end of
    the record passes (censored; the number censored is reported);
  * length filter lmin (km; needs per-frame boundary lengths): a swap counts only when the removed contact's boundary reached lmin
    at some frame of its run before the swap and the created contact's boundary reaches lmin at some frame of its run after it
    (for a pair with several boundaries, its shortest boundary is taken as the one that changes). Unlike a hard cut of short
    boundaries out of the map, this creates no events of its own."""
from collections import Counter

ONE_LOST, ONE_GAINED = 'born 0 died 0 lost 1 gained 0', 'born 0 died 0 lost 0 gained 1'

def _mult(frames):
    return [Counter(T.segments) for T in frames]

def swap_list(frames, rows):
    """All swaps as dicts (iA, iB, lost, gained, via): plain swaps from the log plus swaps through a four-fold meeting."""
    idx = {T.t: i for i, T in enumerate(frames)}; M = _mult(frames); out = []
    for r in rows:
        if r['type'] != 'swap': continue
        i = idx[r['t0']]; cs = r['cells']
        pairs = {tuple(sorted((x, y))) for x in cs for y in cs if x < y}
        lost = [p for p in pairs if M[i + 1][p] < M[i][p]]; gained = [p for p in pairs if M[i + 1][p] > M[i][p]]
        out.append(dict(iA=i, iB=i + 1, lost=lost[0], gained=gained[0], via='direct'))
    L = [(idx[r['t0']], tuple(r['cells'])) for r in rows if r['type'] == 'clump' and r['pattern'] == ONE_LOST]
    G = [(idx[r['t0']], tuple(r['cells'])) for r in rows if r['type'] == 'clump' and r['pattern'] == ONE_GAINED]
    used = set()
    for i, (a, b) in sorted(L):
        A = frames[i]
        for gi, (j, (c, d)) in sorted(enumerate(G), key=lambda x: x[1][0]):
            if gi in used or j < i: continue
            B = frames[j + 1]
            if not ({c, d} <= A.nb[a] & A.nb[b] and {a, b} <= B.nb[c] & B.nb[d]): continue
            if all(any({a, b, c, d} <= set(J) for J in (frames[f].junctions or [])) for f in range(i + 1, j + 1)):
                used.add(gi); out.append(dict(iA=i, iB=j + 1, lost=(a, b), gained=(c, d), via='four-fold')); break
    return sorted(out, key=lambda s: (s['iA'], s['iB']))

def persistent(frames, swaps, k, lmin=0, lengths=None):
    """(count, censored): swaps passing the two-sided persistence rule for k Myr (and the length filter lmin when lengths, a list
    with one {pair: [boundary lengths]} per frame, is given)."""
    M = _mult(frames); n = len(frames)
    step = abs(frames[1].t - frames[0].t) if n > 1 else 1
    cnt = cen = 0
    for s in swaps:
        p, q, iA, iB = s['lost'], s['gained'], s['iA'], s['iB']
        mA, mB = M[iA][p], M[iB][q]
        f = iA
        while f >= 0 and M[f][p] >= mA: f -= 1
        before, cb = (iA - f), f < 0
        g = iB
        while g < n and M[g][q] >= mB: g += 1
        after, ca = (g - iB), g >= n
        okb, oka = before * step >= k or cb, after * step >= k or ca
        if lmin and lengths is not None:
            short = lambda fi, pr: min(lengths[fi].get(pr, [0]))
            okb = okb and max(short(x, p) for x in range(f + 1, iA + 1)) >= lmin
            oka = oka and max(short(x, q) for x in range(iB, g)) >= lmin
        if okb and oka:
            cnt += 1; cen += ((before * step < k and cb) or (after * step < k and ca))
    return cnt, cen
