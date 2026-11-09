"""Reliefs (plate tops/bottoms) and lean menus used by 02 and 03."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from leanplates import *
from escher import bottoms_for, c3_top, top_from, battery

HERE = os.path.dirname(os.path.abspath(__file__))
NAMED = {
    'E1': top_from([(2 * s + 2, 2 * s + 1, 2 * s + 3) for s in range(6)]),
    'E3': c3_top(2, 1, 3, 4, 3, 5),
    'E3p': c3_top(9, 1, 3, 9, 3, 5),
    'E6': top_from([(6, 5, 7)] * 6),
    'RDE': c3_top(9, 3, 6, 9, 6, 9),
    'RDE2': c3_top(9, 3, 6, 9, 0, 3),
}


def canon(P):
    return min(place(P, g) for g in G_ALL)


def from_json_relief(r):
    return tuple(tuple(sorted((tuple(v), x) for v, x in s)) for s in r)


def reliefs():
    """name -> (top, bottom) of plate pieces that tile in the vertical model (checked again in 02)."""
    out = {'FLAT': (flat_relief(6), flat_relief(-6)), 'RD': rd_piece(), 'TRD': trd_piece()}
    st = json.load(open(os.path.join(HERE, '..', 'data', 'escher_04_stack.json')))
    out['E1h'] = (from_json_relief(st['piece'][0]), from_json_relief(st['piece'][1]))
    seen = {canon(P) for P in out.values()}
    for name, top in NAMED.items():
        k = 0
        for b, info in sorted(bottoms_for(top).items(), key=lambda t: str(t[1])):
            if info[3] != 'uniform':
                continue
            P = (top, b)
            if not valid(P) or thickness_sum(P) != 216:
                continue
            c = canon(P)
            if c in seen:
                continue
            seen.add(c)
            out[f'{name}u{k}'] = P
            k += 1
    return out


EPS = (1, 1, -1, -1, -1, 1)        # stripe: corners 5,0,1 lean +D0, corners 2,3,4 lean -D0 (doubled units)


def stripe(u):
    return tuple(add(scal(EPS[s], D[0]), u) for s in range(6))


def shear(u):
    return tuple(tuple(u) for _ in range(6))
