"""Exact six- and eight-crossing contributions to the c/h difference (study 2026-11-15-polygon-bijection, section 8).

A polygon through the root v that crosses the vertical bonds of bilayer kf exactly n times is a cyclic chain
    p0 -a1- p1 -b1- p2 -a2- ... -b_{n/2}- p0
of n/2 root arcs a_i (pairwise vertex-disjoint, in the root half) and n/2 far arcs b_i (pairwise disjoint, in the far half), plus the
n vertical bonds at the crossing points.  Counted up to translation, a shape is weighted by its atoms of the root's type (that is the
number of its translates through v); each shape has n representations with p0 at the origin (choice of the first root arc and its
direction), so the weighted chain count is divided by n (checked).  This is the product structure p = sum w f of README section 3,
evaluated directly, for G (bilayer kf c) and G' (bilayer kf h); Delta_n = count(G') - count(G).  Exact integers, finite: with n crossing
bonds and every arc of at least 2 bonds, one arc has at most l - n - 2(n - 1) bonds, and all such arcs are enumerated.

Usage: six.py LMAX [KF ...]   -> per flip kf = -3..2 and every c/h pattern of bilayers kf-1, kf+1:
                              DELTA6 / DELTA8 per length and per split (R, F) for every l <= LMAX.
"""
import sys, os, itertools, time
from collections import defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import halves24 as H
out = lambda *a: print(*a, flush=True)
T0 = time.time()

def prep(c, amax, wtype):
    A = H.arcs(c, amax)
    lv = {(q[0], q[3]) for _, _, at in A for q in at}
    assert max(j for j, t in lv) <= 2 and (2, 1) not in lv, ('reach', lv)   # so the half depends on c[0..2] only
    res = []
    for e, ln, at in A:
        w = sum(1 for q in at if (q[0], q[3]) == wtype) if wtype else 0
        res.append((e, ln, at, w))
    byl = defaultdict(list); byend = defaultdict(list)
    for z in res: byl[z[1]].append(z); byend[(z[0], z[1])].append(z)
    return byl, byend

def place(at, p):
    return {(q[0], q[1] + p[0], q[2] + p[1], q[3]) for q in at}

def count(cr, cf, wtype, n, lmax):
    """weighted number of n-crossing polygon shapes, by (l, R, F); root arcs in half cr (weights), far arcs in half cf."""
    k = n // 2; tot_max = lmax - n
    amax = tot_max - 2 * (2 * k - 1)            # every other arc has at least 2 bonds
    rbyl, _ = prep(cr, amax, wtype); fbyl, fbyend = prep(cf, amax, None)
    res = defaultdict(int)
    # sequence: a1 b1 a2 b2 ... a_k b_k ; b_k found by lookup from its end point back to the origin
    def rec(i, p, used_r, used_f, rem, R, F, w):
        # i = index of the next arc (0..2k-1), even = root, odd = far
        left = 2 * k - i                         # arcs still to place (including this one)
        if i == 2 * k - 1:
            e = (-p[0], -p[1])
            for ln in range(2, rem + 1, 2):
                for (eb, lb, at, _) in fbyend.get((e, ln), ()):
                    if used_f.isdisjoint(place(at, p)):
                        res[(R + F + ln + n, R, F + ln)] += w
            return
        root = i % 2 == 0
        byl = rbyl if root else fbyl
        for ln in range(2, rem - 2 * (left - 1) + 1, 2):
            for (e, _, at, wa) in byl.get(ln, ()):
                q = (p[0] + e[0], p[1] + e[1])
                if q == (0, 0): continue
                pl = place(at, p)
                if root:
                    if not used_r.isdisjoint(pl): continue
                    rec(i + 1, q, used_r | pl, used_f, rem - ln, R + ln, F, w + wa)
                else:
                    if not used_f.isdisjoint(pl): continue
                    rec(i + 1, q, used_r, used_f | pl, rem - ln, R, F + ln, w)
    rec(0, (0, 0), set(), set(), tot_max, 0, 0, 0)
    for key, v in res.items(): assert v % n == 0, (key, v)
    return {key: v // n for key, v in res.items()}

if __name__ == '__main__':
    LMAX = int(sys.argv[1]); NS = (6, 8) if LMAX >= 24 else (6,)
    allok = True; cases = []
    # positive control: absolute numbers of polygons through the lower atom of bilayer 0 that cross bilayer kf exactly 6 times, in 3C
    # and in 2H, from the direct enumeration of study 2026-11-15-ring-counts-stackings (data/full/diag.txt, profiles {0: 6}, {-1: 6})
    for word, name in (('c' * 19, '3C'), ('h' * 19, '2H')):
        for kf, exp in ((0, {18: 180, 20: 3198}), (-1, {18: 90, 20: 1722})):
            cr, cf, wt = H.halves_of(word, kf); a = count(cr, cf, wt, 6, 20)
            got = {l: sum(v for key, v in a.items() if key[0] == l) for l in exp}
            ok = got == exp; allok &= ok
            out(f'CONTROL six-crossing count {name} flip {kf}: {got} expected {exp}', 'ok' if ok else 'FAIL')
    KFS = [int(x) for x in sys.argv[2:]] or [-3, -2, -1, 0, 1, 2]
    for kf in KFS:
        for pat in itertools.product('ch', repeat=2):      # arcs of at most 8 bonds see only c[0..2]: bilayers kf-1, kf+1 (asserted)
            w = ['c'] * 19; pos = [kf - 1, kf + 1]
            for b, x in zip(pos, pat): w[b + 9] = x
            cases.append((kf, ''.join(pat), w))
    for ci, (kf, pat, w) in enumerate(cases):
        w[kf + 9] = 'c'; cr, cf, wt = H.halves_of(''.join(w), kf)
        w2 = list(w); w2[kf + 9] = 'h'; cr2, cf2, wt2 = H.halves_of(''.join(w2), kf)
        # the root half is the same in G and G' up to the toggle (for kf < 0 the letter construction runs upward, so the root's
        # letters come out exchanged by the toggle, a global isometry): compare normalised letters up to x -> -x
        n1 = [(x - cr[0]) % 3 for x in cr]; n2 = [(x - cr2[0]) % 3 for x in cr2]
        same_root = (n1 == n2 or n1 == [(-x) % 3 for x in n2]) and wt == wt2
        if not same_root: out('ROOT HALF DIFFERS', kf, pat, n1, n2)
        allok &= same_root
        for n in NS:
            a = count(cr, cf, wt, n, LMAX); b = count(cr2, cf2, wt, n, LMAX)
            keys = sorted(set(a) | set(b))
            byl = defaultdict(int); split = []
            for key in keys:
                d = b.get(key, 0) - a.get(key, 0)
                byl[key[0]] += d
                split.append(f'(l{key[0]},R{key[1]},F{key[2]}):{a.get(key, 0)}->{b.get(key, 0)}')
            # Lemma 7 (by hand): a side with exactly 6 bonds (n = 6) or 8 bonds (n = 8, four 2-bond arcs) has no asymmetry
            hand = all(b.get(key, 0) == a.get(key, 0) for key in keys if (n == 6 and 6 in key[1:]) or n == 8)
            allok &= hand
            out(f'DELTA{n} flip {kf} pattern {pat}', ' '.join(f'l{l}:{byl.get(l, 0)}' for l in range(n * 2 + 6, LMAX + 1, 2)),
                'hand-lemma', 'ok' if hand else 'FAIL', '| splits', ' '.join(split) if len(split) < 40 else f'{len(split)} keys')
        out(f'PROGRESS {round((ci + 1) / len(cases), 3)} cases {ci + 1}/{len(cases)} ({time.time() - T0:.0f} s)')
    out('ALLCHECKS', 'ok' if allok else 'FAIL')
