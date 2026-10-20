# EXACT builds of the OG's downward family (DICTO 2026-10-20: "one paper both ways"): the reverse UP step run inward from the exact OG
#   reverse step: the new corners are the foot points of the last solid's face planes (the point of each plane nearest the centre);
#   it undoes the forward step (checked exactly here: step(rev(S)) == S for every solid).
# In Q(sqrt5), same frame, group and checks as exact_upward.py. For each solid: corners, faces, edges, exact face kinds (squared
# side lengths), exact volume, corner radii, full symmetry; nesting inside the solid above it (exact), and if nested, the shell's
# pieces (one per face of the inner solid, the cone over it cut by the outer solid), sum = gap, one symmetry orbit per kind.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'exact_upward.py')).read().split("names = ['DICTO KRE'")[0])      # OG, G, kinds, step, ...

def rev(S):
    """Exact reverse step: foot points of S's face planes."""
    out = []
    for n, d in solid(S):
        k = d / dot(n, n); out.append(tuple(k * x for x in n))
    return list(dict.fromkeys(out))

def inside(Sin, Sout):
    """Exact: every corner of Sin inside or on the hull of Sout; returns (all inside, corners outside, largest excess)."""
    H = solid(Sout); bad = []; worst = 0.0
    for v in Sin:
        ex = max(((dot(n, v) - d) / Q5(1)).f() / (sum(x.f() ** 2 for x in n) ** .5) for n, d in H)
        if any((dot(n, v) - d).sign() > 0 for n, d in H): bad.append(v); worst = max(worst, ex)
    return not bad, len(bad), worst

log = {'mark': 'DICTO OG downward family, exact builds, 2026-10-20', 'solids': {}, 'nesting': [], 'shells': []}
S = OG; chain = [OG]
for k in range(1, 5):
    T = rev(S); back = step(T)[0]; nm = f'down {k}'
    C, F, K = kinds(T); r2 = sorted({repr(dot(v, v)) for v in T})
    log['solids'][nm] = {'corners': len(T), 'faces': len(F), 'edges': sum(len(o) for o, _ in F) // 2,
                         'face_kinds': [{'sides': q[0], 'count': c, 'squared_sides': list(q[1])} for q, c in K.items()],
                         'volume': repr(volume(C, F)), 'volume_float': volume(C, F).f(), 'distinct_corner_radii': len(r2),
                         'corner_radii_float': sorted({round(dot(v, v).f() ** .5, 6) for v in T}),
                         'symmetric_under_60_rotations': all({app(M, v) for v in T} == set(T) for M in G),
                         'forward_step_returns_the_solid_above_exactly': set(back) == set(S)}
    ok, nbad, worst = inside(T, S)
    log['nesting'].append({'inner': nm, 'outer': 'OG' if k == 1 else f'down {k - 1}', 'nested_exactly': ok, 'corners_outside': nbad, 'largest_excess': worst})
    print(nm, {a: b for a, b in log['solids'][nm].items() if a != 'face_kinds'}, [(q[0], c) for q, c in K.items()], log['nesting'][-1], flush=True)
    if ok: log['shells'].append(shell(T, S, G, f"{nm} -> {'OG' if k == 1 else f'down {k - 1}'}"))
    S = T; chain.append(T)
json.dump(log, open(os.path.join(HERE, 'data', 'exact_downward.json'), 'w'), indent=1)
