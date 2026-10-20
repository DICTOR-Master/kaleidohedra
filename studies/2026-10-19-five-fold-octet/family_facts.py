# DICTO 2026-10-20: extra exact facts for the OG family paper: the OG in this frame; which OG corners make faces of the KRE;
# whether the reverse step undoes the forward step from the OG (rev(KRE) == OG?); regular faces of each solid.
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'exact_upward.py')).read().split("names = ['DICTO KRE'")[0])
def rev(S):
    out = []
    for n, d in solid(S):
        k = d / dot(n, n); out.append(tuple(k * x for x in n))
    return list(dict.fromkeys(out))
C, F, K = kinds(OG); KRE = step(OG)[0]
H = solid(KRE); used = [v for v in OG if any(all((a * dot(v, v) - b * x) == Q5(0) for a, x in zip(n, v)) and (dot(n, v) - d) == Q5(0) for n, d in H for b in [d])]
tight = [v for v in OG if any((dot(n, v) - d) == Q5(0) for n, d in H)]
back = rev(KRE)
out = {'mark': 'DICTO OG family, extra exact facts, 2026-10-20',
       'OG': {'corners': len(OG), 'faces': len(F), 'volume': repr(volume(C, F)), 'volume_float': volume(C, F).f(),
              'face_kinds': [{'sides': q[0], 'count': c} for q, c in K.items()], 'corner_radii_float': sorted({round(dot(v, v).f() ** .5, 6) for v in OG})},
       'OG_corners_on_a_KRE_face': len(tight), 'OG_corners_strictly_inside_KRE': len(OG) - len(tight),
       'reverse_of_KRE': {'corners': len(back), 'equals_OG': set(back) == set(OG), 'subset_of_OG': set(back) <= set(OG)}}
# regular faces, exact: all sides equal and all corner angles equal (equal dot products of the two edges at each corner)
UPN = ['DICTO KRE', 'DICTO PHE', 'DICTO TPP', 'DICTO DPHP']; DN = ['DICTO TPH', 'DICTO TQH', 'DICTO TQP', 'DICTO TQHD']
ch = {'DICTO OG': OG}; T = OG
for nm in UPN: T = step(T)[0]; ch[nm] = T
T = OG
for nm in DN: T = rev(T); ch[nm] = T
reg = {}
for nm, T in ch.items():
    Cc, Ff = polytope(solid(T)); cnt = Counter()
    for o, _ in Ff:
        P = [Cc[j] for j in o]; n = len(P); e = [sub(P[(i + 1) % n], P[i]) for i in range(n)]
        sides = {dot(x, x) for x in e}; angs = {dot(e[i - 1], e[i]) for i in range(n)}
        cnt[(n, 'regular' if len(sides) == 1 and len(angs) == 1 else ('equal sides' if len(sides) == 1 else 'irregular'))] += 1
    reg[nm] = {f'{k[0]}-gon {k[1]}': c for k, c in sorted(cnt.items())}
out['faces_exact'] = reg
out['OG_five_fold_corners_are_KRE_corners'] = sum(a in set(KRE) for a in apex)
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(HERE, 'data', 'family_facts.json'), 'w'), indent=1)
