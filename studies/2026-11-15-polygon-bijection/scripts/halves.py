"""Local count of the c/h difference from half-structure tables (study 2026-11-15-polygon-bijection).  Exact integers only.

A HALF is the part of the network on one side of the vertical bonds of bilayer kf.  In half coordinates an atom is (j, X, t):
level j = 0 has only the boundary atoms F0 (t = 1) at the points X of the lattice of letter c[0]; level j >= 1 has a near atom
N_j (t = 0, bonded by slanted bonds to F_{j-1}) and a far atom F_j (t = 1, vertical bond to N_j), at the points of letter c[j].
Upper half from U_kf: F0 = U_kf, N1 = L_kf+1, F1 = U_kf+1, ...  (c[j] = s[kf + j]).
Lower half from L_kf: F0 = L_kf, N1 = U_kf-1, F1 = L_kf-1, ...  (c[j] = s[kf - j]).
The vertical bonds of F0 are not in the half.  An ARC is a simple path in the half between two boundary atoms.

For a crossing set S of 4 points (up to translation) and a pairing M of S into two pairs:
  bad(S, M, F)  = number of pairs of arcs (one per pair of M, total F bonds) that SHARE an atom,
  badw(S, M, R) = the same pairs weighted by the number of atoms of the root's type on the two arcs.
Theorem (see README):  Delta = p(G2) - p(G) = - 1/2 * sum_{S, M != M', R + F = l - 4} A_w(S, M, R) * A(S, M', F)
  with A(S, M, F) = bad(gS, gM, F) - bad(S, M, F) for the far half, A_w likewise for the root half (weights), g = the half-turn
  x -> -x (any toggle: it exchanges the two letters other than c[0]).  Only 4-crossing terms are included here; the run checks
  that the result equals the coefficient found by direct enumeration (6-crossing terms are checked separately in bij runs).
Usage: halves.py LMAX [BASE_INDEX]   -> Delta for the lower atom of bilayer 0 (root) and flips kf = -2..1 (3C base and other bases), l <= LMAX.
"""
import sys, itertools, time
from collections import defaultdict
out = lambda *a: print(*a, flush=True)
D1 = ((1, 1), (-2, 1), (1, -2)); D2 = ((-1, -1), (2, -1), (-1, 2))
def nbrs(c, a):
    j, x, y, t = a
    res = []
    if t == 1:
        if j >= 1: res.append((j, x, y, 0))
        dd = D1 if (c[j + 1] - c[j]) % 3 == 1 else D2
        res += [(j + 1, x + dx, y + dy, 0) for dx, dy in dd]
    else:
        res.append((j, x, y, 1))
        dd = D1 if (c[j - 1] - c[j]) % 3 == 1 else D2
        res += [(j - 1, x + dx, y + dy, 1) for dx, dy in dd]
    return res
def arcs_from_origin(c, amax):
    """all arcs of length <= amax starting at the boundary atom over (c0, c0); returns list of (end point offset, length, atoms)."""
    o = (0, c[0], c[0], 1); res = []; path = [o]; on = {o}
    def rec(a):
        ln = len(path) - 1
        if ln >= 1 and a[0] == 0 and a[3] == 1:
            res.append(((a[1] - c[0], a[2] - c[0]), ln, tuple(path)))
        if ln == amax: return
        for b in nbrs(c, a):
            if b in on: continue
            if a == o and b[0] == 0: continue
            on.add(b); path.append(b); rec(b); path.pop(); on.discard(b)
    rec(o); return res
def tables(c, fmax, wtype):
    """bad (wtype None) or badw (wtype = (j, t)) as dict[(S, M, F)] -> count, S and M normalised by translation."""
    arcs = arcs_from_origin(c, fmax - 2)
    by_len = defaultdict(list)
    for e, ln, at in arcs: by_len[ln].append((e, ln, at))
    seen = set(); tab = defaultdict(int)
    def norm(pts):
        x0, y0 = min(pts); return lambda p: (p[0] - x0, p[1] - y0)
    for la in by_len:
        for lb in by_len:
            if la + lb > fmax: continue
            for ea, _, A in by_len[la]:
                Aset = set(A)
                for eb, _, B in by_len[lb]:
                    # translations t (lattice vectors, multiples of 3 in both coordinates) that make B + t meet A
                    ts = set()
                    for a in A:
                        for b in B:
                            if a[0] == b[0] and a[3] == b[3]: ts.add((a[1] - b[1], a[2] - b[2]))
                    for t in ts:
                        p1, p2, p3, p4 = (0, 0), ea, t, (t[0] + eb[0], t[1] + eb[1])
                        if len({p1, p2, p3, p4}) < 4: continue
                        Bt = tuple((b[0], b[1] + t[0], b[2] + t[1], b[3]) for b in B)
                        if not Aset.intersection(Bt): continue
                        nf = norm([p1, p2, p3, p4])
                        sa = tuple(sorted([tuple((q[0], *nf(q[1:3]), q[3]) for q in A)], key=lambda z: z)[0])
                        sb = tuple((q[0], *nf(q[1:3]), q[3]) for q in Bt)
                        ca = min(sa, sa[::-1]); cb = min(sb, sb[::-1])
                        key = (ca, cb) if ca <= cb else (cb, ca)
                        if key in seen: continue
                        seen.add(key)
                        S = frozenset(nf(p) for p in (p1, p2, p3, p4))
                        M = frozenset((frozenset((nf(p1), nf(p2))), frozenset((nf(p3), nf(p4)))))
                        wgt = 1 if wtype is None else sum(1 for q in A + Bt if (q[0], q[3]) == wtype)
                        tab[(S, M, la + lb)] += wgt
    return tab, len(arcs), len(seen)
import os
WRONG = os.environ.get('WRONG') == '1'   # negative control: a class-PRESERVING mirror (x, y) -> (y, x) in place of the toggle
def g_shape(S, M):
    """the half-turn x -> -x (or, under WRONG=1, the mirror (x, y) -> (y, x)), then translation to the normal position"""
    if WRONG:
        pts = [(y, x) for x, y in S]; x0, y0 = min(pts); f = lambda p: (p[1] - x0, p[0] - y0)
        return frozenset(f(p) for p in S), frozenset(frozenset(f(p) for p in e) for e in M)
    pts = [(-x, -y) for x, y in S]; x0, y0 = min(pts); f = lambda p: (-p[0] - x0, -p[1] - y0)
    return frozenset(f(p) for p in S), frozenset(frozenset(f(p) for p in e) for e in M)
def matchings(S):
    p = sorted(S); a = p[0]
    return [frozenset((frozenset((a, b)), frozenset(set(p) - {a, b}))) for b in p[1:]]
def asym(tab):
    A = defaultdict(int)
    for (S, M, F) in list(tab):
        gS, gM = g_shape(S, M)
        A[(S, M, F)] = tab.get((gS, gM, F), 0) - tab[(S, M, F)]
        A[(gS, gM, F)] = tab[(S, M, F)] - tab.get((gS, gM, F), 0)
    return A
CACHE = {}
def cached(c, fmax, wtype):
    # a translation by (1,1)/3 of the plane shifts every letter by 1 and maps the half onto the shifted half; tables are taken
    # up to translation, so they depend only on the letters relative to c[0], and only on the levels an arc can reach
    # an arc of at most fmax - 2 <= 10 bonds returns to level 0, so it reaches at most N_3 (4j - 2 <= 10): the tables depend on
    # c[0..3] only; the key keeps c[0..4], and the letters beyond are continued in any valid way (here: cubic)
    assert fmax <= 12
    cn = tuple((x - c[0]) % 3 for x in c[:5])
    k = (cn, fmax, wtype)
    if k not in CACHE:
        ext = list(cn)
        while len(ext) < 9: ext.append((2 * ext[-1] - ext[-2]) % 3)
        tab, na, nb = tables(ext, fmax, wtype); CACHE[k] = tab
        A = asym(tab)
        out('SIZES letters', ''.join(map(str, k[0])), 'fmax', fmax, 'weight', wtype, 'arcs from a boundary atom', na,
            'meeting arc pairs', nb, 'configurations (S,M,F)', len(tab), 'with A != 0', sum(1 for v in A.values() if v),
            'first F with A != 0', min([F for (S, M, F), v in A.items() if v], default=None))
    return CACHE[k]
def delta(cr, cf, wtype, lmax):
    """cr: letters of the root half, cf: letters of the far half; returns {l: Delta contribution of 4-crossings}"""
    fmax = lmax - 8          # 4 crossing bonds + at least 4 bonds on the other side (two arcs of >= 2)
    Ar = asym(cached(cr, fmax, wtype)); Af = asym(cached(cf, fmax, None))
    res = defaultdict(int)
    byS = defaultdict(list)
    for (S, M, F), v in Af.items():
        if v: byS[S].append((M, F, v))
    for (S, M, R), vr in Ar.items():
        if not vr: continue
        for (Mp, F, vf) in byS.get(S, ()):
            if Mp != M and R + F + 4 <= lmax: res[R + F + 4] += vr * vf
    return {l: -v // 2 if v % 2 == 0 else ('ODD', v) for l, v in res.items()}

if __name__ == '__main__':
    LMAX = int(sys.argv[1]); T0 = time.time(); allok = True
    # c/h word -> letters: bilayers -4..4 around 0, root = lower atom of bilayer 0
    def letters(word):      # word for bilayers -7..7 (index 0 -> bilayer -7); returns s for bilayers -8..8
        s = [0, 1]
        for x in word:
            k = len(s) - 1; d = (s[k] - s[k - 1]) % 3; s.append((s[k] + d) % 3 if x == 'c' else s[k - 1])
        h = len(word) // 2 + 1
        return {b: s[b + h] for b in range(-h, h + 1)}
    EXPECT = {18: {-2: -12, -1: -30, 0: -42, 1: -24}, 20: {-2: -30, -1: -114, 0: -204, 1: -12}}
    bases = ['c' * 15, 'h' * 15, 'ch' * 7 + 'c', 'hhcc' * 3 + 'hhc']
    if len(sys.argv) > 2 and sys.argv[2] == 'all':
        # flips kf = -4..3 (expected 0 outside -2..1); every c/h pattern of the six bilayers kf-3..kf+3 other than kf, c elsewhere
        jobs = []
        for kf in (-4, -3, -2, -1, 0, 1, 2, 3):
            for pat in itertools.product('ch', repeat=6):
                w = ['c'] * 19; pos = [b for b in range(kf - 3, kf + 4) if b != kf]
                for b, x in zip(pos, pat): w[b + 9] = x
                jobs.append((''.join(w), kf))
        nok = 0
        for n, (base, kf) in enumerate(jobs):
            w = list(base); w[kf + 9] = 'c'; s = letters(''.join(w))
            if kf >= 0: cr = [s[kf - j] for j in range(7)]; cf = [s[kf + j] for j in range(7)]; wtype = (kf, 1)
            else: cr = [s[kf + j] for j in range(7)]; cf = [s[kf - j] for j in range(7)]; wtype = (-kf, 0)
            d = delta(cr, cf, wtype, LMAX)
            ok = all(d.get(l, 0) == EXPECT[l].get(kf, 0) for l in EXPECT if l <= LMAX) and all(d.get(l, 0) == 0 for l in range(4, 17))
            nok += ok; allok &= ok
            if not ok or n % 32 == 0: out('DELTA word', base, 'flip', kf, d, 'ok' if ok else 'FAIL')
            if n % 16 == 0: out(f'PROGRESS {round(n / len(jobs), 3)} words {n}/{len(jobs)} ({time.time() - T0:.0f} s)')
        out('ALLWORDS', nok, 'of', len(jobs), 'agree with Theorem 5 (and 0 for l <= 16)')
        out('ALLCHECKS', 'ok' if allok else 'FAIL'); sys.exit(0)
    if len(sys.argv) > 2: bases = [bases[int(sys.argv[2])]]
    for bi, base in enumerate(bases):
        for kf in (-2, -1, 0, 1):
            w = list(base); w[kf + 7] = 'c'          # Delta = p(bilayer kf h) - p(bilayer kf c), other letters = base
            s = letters(''.join(w))
            if kf >= 0:   # root (lower atom of bilayer 0) lies on the lower side of kf
                cr = [s[kf - j] for j in range(7)]; cf = [s[kf + j] for j in range(7)]; wtype = (kf, 1)
            else:
                cr = [s[kf + j] for j in range(7)]; cf = [s[kf - j] for j in range(7)]; wtype = (-kf, 0)
            d = delta(cr, cf, wtype, LMAX)
            line = ' '.join(f'l{l}:{d.get(l, 0)}' for l in range(12, LMAX + 1, 2))
            exp_ok = all(d.get(l, 0) == EXPECT[l][kf] for l in EXPECT if l <= LMAX)
            allok &= exp_ok
            out('DELTA base', base, 'flip', kf, line, 'expected', {l: EXPECT[l][kf] for l in EXPECT if l <= LMAX}, 'ok' if exp_ok else 'FAIL', f'({time.time() - T0:.0f} s)')
        out(f'PROGRESS {round((bi + 1) / len(bases), 3)} base {base}')
    out('ALLCHECKS', 'ok' if allok else 'FAIL')
