"""Four-crossing half tables to F = 14 bonds per side (l <= 24) and the local Delta for every flip and letter pattern
(study 2026-11-15-polygon-bijection, section 8).  Exact integers only.

Same setting and theorem as halves.py (README section 3), written independently of halves.py:
  * arcs are simple paths in a half between two boundary atoms (half coordinates (j, x, y, t) as in halves.py);
  * bad(S, M, F) counts the unordered pairs of arcs, one per pair of M, F bonds in total, that SHARE an atom;
    here every such pair is counted through its 8 ordered representations (arc A from the origin, either end of either arc,
    either arc first) and the total is divided by 8 (the division is checked), so no dedup set is needed;
  * badw(S, M, R) is the same with each pair weighted by the atoms of the root's type on the two arcs (a shared atom counts twice,
    as in the product sum over all pairs, whose total is Tog-invariant);
  * A = bad(gS, gM) - bad(S, M), g the half-turn x -> -x;  Delta = -1/2 sum_{S, M != M', R + F + 4 = l} A_w(S, M, R) A_f(S, M', F).
At l <= 24 a side with A != 0 has at least 6 bonds (checked from the tables themselves: no A != 0 below F = 6), so F, R <= 14 and
every arc in a pair has at most 12 bonds; such an arc reaches at most the near atom N_3 (5 bonds down, 5 up; the far atom F_3 would
need the vertical bond twice), so a table depends on the letters c[0..3] of its half only (asserted below from the arcs).

Usage:
  halves24.py check12          -> tables to F = 12 must equal those of halves.py (independent code), for all 8 letter patterns
  halves24.py all LMAX         -> Delta at l <= LMAX for flips kf = -4..3 and every c/h pattern of bilayers kf-3..kf+3 (512 cases)
  halves24.py dump LMAX OUT    -> also write the nonzero A tables (gz) to OUT
  env WRONG=1                  -> negative control: class-preserving mirror in place of the half-turn
"""
import sys, os, itertools, time, gzip
from collections import defaultdict
out = lambda *a: print(*a, flush=True)
T0 = time.time()
D1 = ((1, 1), (-2, 1), (1, -2)); D2 = ((-1, -1), (2, -1), (-1, 2))
WRONG = os.environ.get('WRONG') == '1'
WTYPES = ((0, 1), (1, 1), (2, 1), (3, 1), (1, 0), (2, 0), (3, 0), (4, 0))   # (level j, t) of the root atom inside the root half

def nbrs(c, a):
    j, x, y, t = a
    if t == 1:
        res = [(j, x, y, 0)] if j >= 1 else []
        dd = D1 if (c[j + 1] - c[j]) % 3 == 1 else D2
        return res + [(j + 1, x + dx, y + dy, 0) for dx, dy in dd]
    dd = D1 if (c[j - 1] - c[j]) % 3 == 1 else D2
    return [(j, x, y, 1)] + [(j - 1, x + dx, y + dy, 1) for dx, dy in dd]

def arcs(c, amax):
    """arcs from the boundary atom at (c0, c0), at most amax bonds: list of (end offset, length, atoms relative to the start)."""
    o = (0, c[0], c[0], 1); res = []; path = [o]; on = {o}
    def rec(a):
        ln = len(path) - 1
        if ln >= 1 and a[0] == 0 and a[3] == 1:
            res.append(((a[1] - c[0], a[2] - c[0]), ln, tuple((q[0], q[1] - c[0], q[2] - c[0], q[3]) for q in path)))
            # no return: an arc may pass through other boundary atoms (their vertical bonds then stay unused)
        if ln == amax: return
        for b in nbrs(c, a):
            if b in on or (a == o and b[0] == 0): continue
            on.add(b); path.append(b); rec(b); path.pop(); on.discard(b)
    rec(o); return res

def norm(pts):
    x0, y0 = min(pts); return {p: (p[0] - x0, p[1] - y0) for p in pts}

def tables(c, fmax):
    """dict (S, M, F) -> [bad, badw for each of WTYPES]; S, M normalised by translation."""
    A = arcs(c, fmax - 2)
    lv = {(q[0], q[3]) for _, _, at in A for q in at}
    assert max(j for j, t in lv) <= 3 and (3, 1) not in lv, ('reach', lv)
    info = []
    for e, ln, at in A:
        idx = defaultdict(list)
        for q in at: idx[(q[0], q[3])].append((q[1], q[2]))
        w = tuple(sum(1 for q in at if (q[0], q[3]) == wt) for wt in WTYPES)
        info.append((e, ln, dict(idx), w))
    byl = defaultdict(list)
    for z in info: byl[z[1]].append(z)
    tab = defaultdict(lambda: [0] * (1 + len(WTYPES)))
    for la in byl:
        for lb in byl:
            if la + lb > fmax: continue
            F = la + lb
            for ea, _, ia, wa in byl[la]:
                for eb, _, ib, wb in byl[lb]:
                    ts = set()
                    for k, pa in ia.items():
                        pb = ib.get(k)
                        if pb:
                            for a in pa:
                                for b in pb: ts.add((a[0] - b[0], a[1] - b[1]))
                    for t in ts:
                        p3 = t; p4 = (t[0] + eb[0], t[1] + eb[1])
                        if p3 == (0, 0) or p3 == ea or p4 == (0, 0) or p4 == ea: continue
                        nf = norm(((0, 0), ea, p3, p4))
                        S = frozenset(nf.values())
                        M = frozenset((frozenset((nf[(0, 0)], nf[ea])), frozenset((nf[p3], nf[p4]))))
                        r = tab[(S, M, F)]; r[0] += 1
                        for i in range(len(WTYPES)): r[i + 1] += wa[i] + wb[i]
    for k, r in tab.items():
        assert all(v % 8 == 0 for v in r), ('not divisible by 8', k, r)
        tab[k] = [v // 8 for v in r]
    return dict(tab), len(A)

def g_shape(S, M):
    if WRONG: f0 = lambda p: (p[1], p[0])
    else: f0 = lambda p: (-p[0], -p[1])
    nf = norm([f0(p) for p in S])
    return frozenset(nf[f0(p)] for p in S), frozenset(frozenset(nf[f0(p)] for p in e) for e in M)

def asym(tab, col):
    A = {}
    for (S, M, F), r in tab.items():
        gS, gM = g_shape(S, M)
        other = tab.get((gS, gM, F))
        v = (other[col] if other else 0) - r[col]
        if v: A[(S, M, F)] = v; A[(gS, gM, F)] = -v
    return A

CACHE = {}
def cached(c, fmax):
    cn = tuple((x - c[0]) % 3 for x in c[:4])       # depends on c[0..3] only (asserted in tables)
    k = (cn, fmax)
    if k not in CACHE:
        ext = list(cn)
        while len(ext) < 8: ext.append((2 * ext[-1] - ext[-2]) % 3)
        t0 = time.time(); tab, na = tables(ext, fmax)
        Af = asym(tab, 0)
        CACHE[k] = (tab, Af)
        out('SIZES letters', ''.join(map(str, cn)), 'fmax', fmax, 'arcs', na, 'configurations', len(tab), 'A_far != 0', len(Af),
            'first F with A_far != 0', min([F for (S, M, F) in Af], default=None), f'({time.time() - t0:.0f} s)')
    return CACHE[k]

def delta(cr, cf, wtype, lmax, fmax):
    tab_r, _ = cached(cr, fmax); _, Af = cached(cf, fmax)
    Ar = asym(tab_r, 1 + WTYPES.index(wtype))
    byS = defaultdict(list)
    for (S, M, F), v in Af.items(): byS[S].append((M, F, v))
    res = defaultdict(int); low = []
    for (S, M, R), vr in Ar.items():
        if R < 6: low.append(('root', R))
        for (Mp, F, vf) in byS.get(S, ()):
            if Mp != M and R + F + 4 <= lmax: res[R + F + 4] += vr * vf
    for (S, M, F) in Af:
        if F < 6: low.append(('far', F))
    assert all(v % 2 == 0 for v in res.values()), res
    return {l: -v // 2 for l, v in res.items() if v}, low

def letters(word):
    """c/h word for bilayers -9..9 (index 0 -> bilayer -9) -> letters s for bilayers -10..10"""
    s = [0, 1]
    for x in word:
        k = len(s) - 1; d = (s[k] - s[k - 1]) % 3; s.append((s[k] + d) % 3 if x == 'c' else s[k - 1])
    h = len(word) // 2 + 1
    return {b: s[b + h] for b in range(-h, h + 1)}

def halves_of(word, kf):
    s = letters(word)
    if kf >= 0: return [s[kf - j] for j in range(7)], [s[kf + j] for j in range(7)], (kf, 1)
    return [s[kf + j] for j in range(7)], [s[kf - j] for j in range(7)], (-kf, 0)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'check12':
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import halves as H
        ok = True
        pats = [(0, a, b, c) for a in (1, 2) for b in range(3) for c in range(3) if b != a and c != b]
        for n, p in enumerate(pats):
            ext = list(p)
            while len(ext) < 9: ext.append((2 * ext[-1] - ext[-2]) % 3)
            mine, _ = tables(ext, 12)
            old, _, _ = H.tables(ext, 12, None)
            same = {k: v[0] for k, v in mine.items()} == dict(old)
            for wt in ((0, 1), (1, 1), (2, 1), (1, 0), (2, 0), (3, 0)):
                oldw, _, _ = H.tables(ext, 12, wt)
                same &= {k: v[1 + WTYPES.index(wt)] for k, v in mine.items() if v[1 + WTYPES.index(wt)]} == {k: v for k, v in oldw.items() if v}
            ok &= same
            out('CHECK12 letters', ''.join(map(str, p)), 'tables to F = 12 equal to halves.py (bad and 6 weights):', 'ok' if same else 'FAIL')
            out(f'PROGRESS {round((n + 1) / len(pats), 3)} patterns {n + 1}/{len(pats)} ({time.time() - T0:.0f} s)')
        out('ALLCHECKS', 'ok' if ok else 'FAIL'); sys.exit(0)
    LMAX = int(sys.argv[2]); FMAX = LMAX - 10
    EXPECT = {18: {-2: -12, -1: -30, 0: -42, 1: -24}, 20: {-2: -30, -1: -114, 0: -204, 1: -12}}
    jobs = []
    for kf in (-4, -3, -2, -1, 0, 1, 2, 3):
        for pat in itertools.product('ch', repeat=6):
            w = ['c'] * 19; pos = [b for b in range(kf - 3, kf + 4) if b != kf]
            for b, x in zip(pos, pat): w[b + 9] = x
            w[kf + 9] = 'c'
            jobs.append((''.join(w), kf, ''.join(pat)))
    allok = True; lowall = set()
    for n, (word, kf, pat) in enumerate(jobs):
        cr, cf, wt = halves_of(word, kf)
        d, low = delta(cr, cf, wt, LMAX, FMAX); lowall |= set(low)
        ok = all(d.get(l, 0) == EXPECT[l].get(kf, 0) for l in EXPECT if l <= LMAX) and all(d.get(l, 0) == 0 for l in range(4, 17))
        allok &= ok
        out('DELTA4 flip', kf, 'pattern', pat, 'word', word, ' '.join(f'l{l}:{d.get(l, 0)}' for l in range(18, LMAX + 1, 2)), 'ok' if ok else 'FAIL')
        if n % 16 == 0: out(f'PROGRESS {round(n / len(jobs), 3)} cases {n}/{len(jobs)} ({time.time() - T0:.0f} s)')
    out('LOWSIDES (sides with A != 0 below 6 bonds):', sorted(lowall) or 'none')
    allok &= not lowall
    if mode == 'dump':
        with gzip.open(sys.argv[3], 'wt') as fh:
            for (cn, fm), (tab, Af) in sorted(CACHE.items()):
                for (S, M, F), r in sorted(tab.items(), key=lambda z: (z[0][2], sorted(z[0][0]), sorted(map(sorted, z[0][1])))):
                    fh.write(f"T {''.join(map(str, cn))} F{F} S {sorted(S)} M {sorted(map(sorted, M))} bad {r[0]} badw {r[1:]}\n")
        out('DUMP written', sys.argv[3])
    out('ALLCHECKS', 'ok' if allok else 'FAIL')
