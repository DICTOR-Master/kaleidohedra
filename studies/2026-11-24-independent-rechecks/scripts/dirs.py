# The 122 frame directions, rebuilt exactly in Q(sqrt5) from the family definitions in the README of study
# 2026-11-19-aequi-complete (C6, O8, RD12; D12, I12, RT24; the quarter-turned placement D12', I12', RT24').
# The catalogue stores face directions as indices into a list; the order inside each family is not stated in any
# README, so it is fixed here by trying the natural conventions and keeping the one under which a sample of
# catalogued dice is fair (checked by numerical solid angles in die_num.py). Own code throughout.
import itertools, json, gzip, os
from fractions import Fraction as F
from qr import Q

phi = Q(F(1, 2), F(1, 2)); iphi = phi - 1; z = Q(0); one = Q(1)
REPS = [('C6', (one, z, z)), ('O8', (one, one, one)), ('RD12', (one, one, z)),
        ('D12', (z, phi, one)), ('I12', (z, iphi, phi)), ('RT24', (one, phi, iphi)),
        ('D12p', (z, one, phi)), ('I12p', (z, phi, iphi)), ('RT24p', (phi, one, iphi))]
ST = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def family(v, conv):
    shift, outer, sfirst = conv
    sh = [v, (v[1], v[2], v[0]), (v[2], v[0], v[1])] if shift == 'L' else [v, (v[2], v[0], v[1]), (v[1], v[2], v[0])]
    signs = list(itertools.product((1, -1) if sfirst == '+' else (-1, 1), repeat=3))
    out = []
    if outer == 'perm':
        it = ((p, s) for p in sh for s in signs)
    else:
        it = ((p, s) for s in signs for p in sh)
    for p, s in it:
        w = tuple(si * x for si, x in zip(s, p))
        if w not in out: out.append(w)
    return out


CONVS = list(itertools.product('LR', ['perm', 'sign'], '+-')) + ['set']


def directions(conv):
    D, FAM = [], []
    for name, v in REPS:
        fam = family_setorder(v) if conv == 'set' else family(v, conv)
        for w in fam: D.append(w); FAM.append(name)
    assert len(D) == 122
    return D, FAM


def family_setorder(v):
    """The catalogue's index convention: iteration order of a Python set of float tuples (sign patterns, then
    the three cyclic shifts), with phi = (1 + 5**.5)/2 in double precision. Only the ORDER is taken from it; each
    float vector is matched to its exact Q(sqrt5) vector below."""
    import numpy as np
    pf = (1 + 5 ** .5) / 2
    fl = lambda q: {phi: pf, iphi: 1 / pf, one: 1, z: 0}[q]
    t = tuple(fl(x) for x in v); S = set()
    for s in itertools.product((1, -1), repeat=3):
        q = tuple(a * b for a, b in zip(s, t))
        for k in range(3): S.add(tuple(np.roll(q, k)))
    exact = family(v, ('L', 'perm', '+'))
    out = []
    for p in S:
        u = np.array(p) / np.linalg.norm(p)
        if any(np.abs(u - np.array([float(x) for x in w]) / np.linalg.norm([float(x) for x in w])).max() < 1e-9 for w in out): continue
        m = [w for w in exact if np.abs(np.array([float(x) for x in w]) - np.array(p)).max() < 1e-9]
        assert len(m) == 1; out.append(m[0])
    assert sorted(map(str, out)) == sorted(map(str, exact))
    return out


def catalogue():
    """All 15192 catalogued dice as (src, sid, idx list, per-face depth list, N)."""
    out = []
    for f in sorted(os.listdir(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice'))):
        r = json.load(open(os.path.join(ST, '2026-11-19-aequi-complete', 'data', 'dice', f)))
        dep = [float(d) for d, k in zip(r['depths_60_digits'], r['orbit_sizes']) for _ in range(k)]
        out.append(('2026-11-19-aequi-complete', r['sid'], r['face_directions'], dep, r['N'], r['depths_60_digits'], r['orbit_sizes']))
    for r in json.load(open(os.path.join(ST, '2026-11-20-aequi-two-placements', 'data', 'aequi.json'))):
        dep = [float(d) for d, k in zip(r['depths_60_digits'], r['orbit_sizes']) for _ in range(k)]
        out.append(('2026-11-20-aequi-two-placements', r['sid'], r['face_directions'], dep, r['N'], r['depths_60_digits'], r['orbit_sizes']))
    for p in ['aequi2a', 'aequi2caps', 'aequi2caps2', 'aequi2caps3']:
        D = json.load(gzip.open(os.path.join(ST, '2026-11-24-aequi-certify-extend', 'data', p + '.json.gz')))
        for r in D['new']:
            dep = [float(d) for d, k in zip(r['depths'], r['sizes']) for _ in range(k)]
            out.append(('2026-11-24-aequi-certify-extend/' + p, r['sid'], r['idx'], dep, r['N'], [repr(d) for d in r['depths']], r['sizes']))
    return out
