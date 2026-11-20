"""Step 2. Local angle test (exact) with fixed-point pruning.
At a generic point of an edge of a piece, the pieces around it fill the full turn: their dihedral angles sum to 2*pi, or to
pi when the point lies inside a face of another piece. Angles are exact vectors (q, a, b, c) meaning
q*pi + a*alpha + b*beta + c*gamma (data/angles.json, all proved); pi, alpha, beta, gamma are independent over Q (proved), so
a sum equals 2*pi exactly iff its vector is (2,0,0,0).
Modes:  strict    : only the listed pieces; sum must be (1,0,0,0) or (2,0,0,0).
        +rational : also ANY convex pieces whose dihedrals are all rational multiples of pi (cubes, every prism, rhombic
                    dodecahedron, rhombic triacontahedron and their centre pyramids, ...). Then a listed-piece sum
                    (q,0,0,0) with q <= 2 can be completed, so the test is: irrational part 0 and q <= 2.
Pruning: a piece kind can occur in a tiling only if every one of its edge kinds closes using pieces that can occur.
Repeat until nothing changes. If a lead piece is pruned, no tiling of space (face-to-face or not, any scales, mirror
images allowed) by the allowed pieces contains it."""
import json, math, sys
from fractions import Fraction as Fr
A = json.load(open('data/angles.json'))
log = []
def say(s):
    print(s, flush=True); log.append(s)
BAS = [math.pi, math.atan((1 + 5 ** .5) / 2), math.acos(1 / 6 ** .5), math.acos((2 / 3) ** .5)]
def kinds(piece):
    K = {}
    for k in A['pieces'][piece]:
        v = tuple(Fr(x) for x in k['coords'])
        K.setdefault((tuple(k['faces']), v), 0)
        K[(tuple(k['faces']), v)] += k['count']
    return [{'faces': f, 'v': v, 'count': c} for (f, v), c in K.items()]
def val(v): return sum(float(x) * b for x, b in zip(v, BAS))
def vs(v):
    q, a, b, c = v; t = [f'{q}π' if q else '']
    for x, n in ((a, 'α'), (b, 'β'), (c, 'γ')):
        if x: t.append(f'{"+" if x > 0 else "−"}{abs(x) if abs(x) != 1 else ""}{n}')
    return ''.join(t) or '0'

def closes(target, angles, mode, bound=2.0, want_all=False):
    """angles: list of (label, vec). Find multisets containing target with exact closure."""
    angles = sorted(set(angles), key=lambda t: -val(t[1]))
    vals = [val(v) for _, v in angles]
    lim = bound * math.pi + 1e-9
    sols = []
    def rec(i, cur, s, picks):
        if i == len(angles):
            if picks.get(target, 0) < 1: return
            irr = cur[1:] == (0, 0, 0)
            if not irr: return
            q = cur[0]
            ok = (q in (1, 2)) if mode == 'strict' else (0 < q <= bound)
            if ok: sols.append((q, dict(picks)))
            return
        lab, v = angles[i]
        n = 0
        while s + n * vals[i] <= lim:
            if n: picks[(lab, v)] = n
            rec(i + 1, tuple(cur[k] + n * v[k] for k in range(4)), s + n * vals[i], picks)
            n += 1
        picks.pop((lab, v), None)
    rec(0, (Fr(0),) * 4, 0.0, {})
    return sols

def minimal_rational_sum(target, angles):
    """smallest q such that target + others has zero irrational part (searched up to 4*pi)."""
    s = closes(target, angles, 'gen', bound=4.0)
    return min((q for q, _ in s), default=None), s

def run(name, pieces, mode, must_keep=None, expect=None):
    alive = list(pieces)
    removed = []
    while True:
        angs = [(p, k['v']) for p in alive for k in kinds(p)]
        kill = None
        for p in alive:
            for k in kinds(p):
                sols = closes((p, k['v']), angs, mode)
                if not sols:
                    kill = (p, k); break
            if kill: break
        if not kill: break
        p, k = kill
        removed.append((p, k))
        alive.remove(p)
        say(f"   [{name}] prune {p}: edge {k['faces']} angle {vs(k['v'])} has no closure "
            f"({'sum π or 2π' if mode == 'strict' else 'irrational part 0 and sum ≤ 2π'}) using {alive + [p]}")
    verdict = 'all pieces survive the angle test' if len(alive) == len(pieces) else f'survivors: {alive}'
    res = {'set': name, 'pieces': pieces, 'mode': mode, 'removed': [(p, list(k['faces']), vs(k['v'])) for p, k in removed],
           'alive': alive}
    ok = True
    if expect is not None:
        ok = (expect == 'pass') == (len(alive) == len(pieces))
    if must_keep is not None:
        res['leads_survive'] = all(m in alive for m in must_keep)
    say(f"{'ok  ' if ok else 'FAIL'} {name} [{mode}]: {verdict}" + (f"  (expected {expect})" if expect else ''))
    return res, ok

def main():
    allok = True; results = []
    say('== controls ==')
    for nm, ps, md, ex in [('octet', ['tetrahedron', 'octahedron'], 'strict', 'pass'),
                           ('cube alone', ['cube'], 'strict', 'pass'),
                           ('B3 permutohedron alone', ['B3 permutohedron'], 'strict', 'fail'),
                           ('truncated cuboctahedron + cube', ['truncated_cuboctahedron', 'cube'], 'strict', 'pass'),
                           ('truncated octahedron alone', ['truncated_octahedron'], 'strict', 'pass'),
                           ('dodecahedron alone', ['dodecahedron'], 'strict', 'fail'),
                           ('regular tetrahedron alone', ['tetrahedron'], 'strict', 'fail')]:
        r, ok = run(nm, ps, md, expect=ex); allok &= ok; results.append(r)
    # the octet's tetrahedron edge must close with 2 tetra + 2 octa exactly
    oc = closes(('tetrahedron', kinds('tetrahedron')[0]['v']), [(p, k['v']) for p in ['tetrahedron', 'octahedron'] for k in kinds(p)], 'strict')
    say(f"     octet closures at a tetrahedron edge: {[(str(q), {f'{a}': n for (a, _), n in d.items()}) for q, d in oc]}")
    say('== leads ==')
    L1 = ['dodecahedron centre pyramid', 'truncated_icosahedron']
    L2 = ['icosahedron centre pyramid', 'truncated_dodecahedron']
    for lead, L in (('lead 1', L1), ('lead 2', L2)):
        say(f'-- {lead}: {L}')
        for p in L:
            for k in kinds(p):
                say(f"     {p:28s} edge {str(k['faces']):18s} x{k['count']:3d}  {vs(k['v']):14s} = {val(k['v'])*180/math.pi:.6f}°")
        angs = [(p, k['v']) for p in L for k in kinds(p)]
        for p in L:
            for k in kinds(p):
                if k['v'][1:] == (0, 0, 0): continue
                qmin, s = minimal_rational_sum((p, k['v']), angs)
                ex = [d for q, d in s if q == qmin][:2]
                say(f"     cheapest closure of the irrational part at {p} edge {k['faces']}: {qmin}π  e.g. "
                    f"{[{f'{a} {vs(v)}': n for (a, v), n in d.items()} for d in ex]}")
        extras = {
            'pair alone': [],
            '+ dodecahedron + icosahedron': ['dodecahedron', 'icosahedron'],
            '+ truncated octahedron + truncated cuboctahedron + cube': ['truncated_octahedron', 'truncated_cuboctahedron', 'cube'],
            '+ truncated icosidodecahedron': ['truncated_icosidodecahedron'],
            '+ all of these': ['dodecahedron', 'icosahedron', 'truncated_octahedron', 'truncated_cuboctahedron', 'cube',
                               'truncated_icosidodecahedron'],
        }
        for en, ex in extras.items():
            for md in ('strict', 'rational'):
                r, ok = run(f'{lead} {en}', L + ex, md, must_keep=L); allok &= ok
                r['lead'] = lead; results.append(r)
                say(f"     -> lead pieces {'SURVIVE' if r['leads_survive'] else 'cannot occur in any tiling'}")
    json.dump(results, open('data/angle_test.json', 'w'), indent=1, ensure_ascii=False)
    say('FINAL ok' if allok else 'FINAL FAIL')
main()
