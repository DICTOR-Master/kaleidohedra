"""Escher stepped-hexagon pieces and the standard test battery (used by 02_named.py and 03_scan.py)."""
import itertools
from plates import *


def top_from(triples):
    return relief(triples)


def c3_top(c0, u0, w0, c1, u1, w1):
    """even sectors (from a D_even corner to a D_odd corner) = (c0,u0,w0), odd sectors = (c1,u1,w1)."""
    return relief([(c0, u0, w0) if s % 2 == 0 else (c1, u1, w1) for s in range(6)])


def rim_climb(top):
    """sum over the 6 plates of (leading rim corner - trailing rim corner), ccw = the staircase's rise per turn."""
    return sum(dict(top[s])[D[(s + 1) % 6]] - dict(top[s])[D[s]] for s in range(6))


def risers(top):
    """jump at each rim corner D_s from plate s-1 (leading value) to plate s (trailing value); centre jumps too."""
    rim = [dict(top[s])[D[s]] - dict(top[(s - 1) % 6])[D[s]] for s in range(6)]
    cen = [dict(top[s])[O] - dict(top[(s - 1) % 6])[O] for s in range(6)]
    return rim, cen


def bottoms_for(top, c3=False):
    """'matching bottoms': (a) reassembled from the tops of the 3 lower cells, each upright and turned by a multiple
    of 60 deg (lean below 1 or 2); (b) the top turned over by a C2 about a horizontal axis (bottom = -top(P v) + d,
    P a reflection, d fixed by the volume): the helicoid turned end over end, the screw's own symmetry."""
    out = {}
    rr = range(2) if c3 else range(6)
    for lean in (1, 2):
        for rots in itertools.product(rr, repeat=3):
            b = reassembled_bottom(top, lean, rots)
            if b is not None:
                kind = 'uniform' if len(set(rots)) == 1 else 'mixed'
                out.setdefault(b, ('reasm', lean, rots, kind))
    st = sum(dict(top[s])[v] for s in range(6) for v in dict(top[s]))
    num = 2 * st - 216
    if num % 18 == 0:
        d = num // 18
        for r in range(6):
            b = map_relief(top, planar(r, 1), True)
            b = tuple(tuple(sorted((v, x + d) for v, x in s)) for s in b)
            out.setdefault(b, ('C2', r, d, 'turned'))
    return out


def battery(pieces, mirrors=False, patch=(4, 2), maxidx=3, words_len=None):
    """returns dict: verdict in {'INVALID','NO PATCH','PERIODIC-k','CANDIDATE'} + data."""
    for P in pieces:
        if not valid(P) or thickness_sum(P) != 216:
            return {'verdict': 'INVALID'}
    sts, _ = states(pieces, mirrors)
    C = compat_table(sts)
    n = len(sts)
    res = {'states': n}
    K, R = patch
    adm = []
    for w in itertools.product((1, 2), repeat=K - 1):
        if w[0] != 1:
            continue
        cells, con = patch_contacts(w, R)
        if sat_solve(len(cells), n, con, C)[0]:
            adm.append(''.join('c' if w[i] == w[i - 1] else 'h' for i in range(1, len(w))))
    res['patch_words'] = adm
    if not adm:
        res['verdict'] = 'NO PATCH'
        return res
    for M in hnf(maxidx):
        if n ** (M[0] * M[2]) > 300000:
            continue
        alive, edges, conf = periodic_alive(C, n, M)
        if alive:
            res['verdict'] = f'PERIODIC-{M[0]*M[2]}'
            res['M'] = M
            res['periodic_words'] = ch_words_from_edges(edges, words_len or 4)
            return res
    res['verdict'] = 'CANDIDATE'
    return res
