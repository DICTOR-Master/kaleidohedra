# Fable review 2026-10-18 -- fill the REPORT.md placeholders from data/fable-node.json (run after the dicto-node job).
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); D = json.load(open(os.path.join(HERE, '..', 'data', 'fable-node.json')))
rep = open(os.path.join(HERE, '..', 'REPORT.md')).read()
S = D['sampling']; P = D['pieces']
def row(kind, kit):
    r = S[kind][kit]; return f"| {kind} | {kit} | {r['points']:,} | {r['none']} | {r['exactly_one']} | {r['two_or_more']} |"
tab = ["| points | kit | n | in no piece | in exactly one | in two or more |", "|---|---|---|---|---|---|"]
for kind in ('uniform', 'boundary'):
    for kit, lab in (('keyed', 'keyed kit'), ('full', 'full kit (M whole)'), ('full_split', 'full kit (core + rest)'), ('noKey', 'kit B, no keys (I1)')): tab.append(row(kind, kit).replace(f'| {kit} |', f'| {lab} |'))
tab.append(f"\nUniform points: uniform in the lattice cell. Boundary points: uniform points moved onto a random piece face plane and pushed off it by 10^−6…10^−2 (log-uniform), folded back into the cell. Middle pieces found overlapping each other: {S['uniform']['middle_pieces_overlapping']} (uniform), {S['boundary']['middle_pieces_overlapping']} (boundary).")
rep = rep.replace('@@SAMPLING_TABLE@@', '\n'.join(tab))
def summ(kit):
    u, b = S['uniform'][kit], S['boundary'][kit]; return f"{u['points']:,} uniform + {b['points']:,} near-face points, {u['none'] + b['none']} uncovered, {u['two_or_more'] + b['two_or_more']} double"
rep = rep.replace('@@S_KEYED@@', summ('keyed')).replace('@@S_FULL@@', summ('full') + ' (same with core + rest split: ' + summ('full_split').split(', ', 1)[1] + ')').replace('@@S_B@@', summ('noKey'))
names = [('bare_OCD', 'bare OCD'), ('keyed_OCD', 'keyed OCD'), ('cap', 'cap (keyed kit)'), ('dented_tet_plus', 'dented tetrahedron (keyed kit)'), ('notched_cap', 'notched cap'),
         ('middle', 'middle piece M'), ('penrose_core', 'Penrose core'), ('middle_rest', 'middle rest'), ('notched_tet_plus', 'notched tetrahedron'),
         ('A_keyed_OCD', 'A: OCD + 8 hexagonal-plug keys'), ('A_key_hex', 'A: plug key alone'), ('A_dented_tet', 'A: tetrahedron with 4 plug dents'),
         ('B_middle_nokeys', 'B: middle piece M₀ (no keys)'), ('B_rest', 'B: rest (no keys)'), ('B_notched_tet_nokeys', 'B: notched tetrahedron (no dents)')]
pt = ["| piece | volume | ψ | solid parts (>1e-9) | genus |", "|---|---|---|---|---|"]
for k, lab in names:
    p = P[k]; pt.append(f"| {lab} | {p['volume']:.6f} | {p['sphericity']:.3f} | {p['parts_over_1e_9']} | {p['genus']} |")
pt.append("\nPenrose core is unchanged in kit B (no key enters it). Cap ψ differs from step 17's 0.494 because of the area cleaning (R8).")
rep = rep.replace('@@PSI_TABLE@@', '\n'.join(pt))
g = lambda k: f"{P[k]['sphericity']:.3f}"
for tag, k in (('@@PSI_B_M@@', 'B_middle_nokeys'), ('@@PSI_M@@', 'middle'), ('@@PSI_B_T@@', 'B_notched_tet_nokeys'), ('@@PSI_T@@', 'notched_tet_plus'), ('@@PSI_B_R@@', 'B_rest'), ('@@PSI_R@@', 'middle_rest'),
               ('@@PSI_A_OCD@@', 'A_keyed_OCD'), ('@@PSI_A_T@@', 'A_dented_tet'), ('@@PSI_DT@@', 'dented_tet_plus')): rep = rep.replace(tag, g(k))
sol = []
for k, lab in names[:9]:
    p = P[k]; sol.append(f"{lab}: {p['parts_over_1e_9']} solid part(s), genus {p['genus']}, {p['parts_total'] - p['parts_over_1e_9']} zero-volume sliver(s)")
hd = D['handedness']
sol.append(f"Handedness (mesh): dented tetrahedron chiral = {hd['dented_tet']['chiral']} (smallest improper symmetric difference {hd['dented_tet']['smallest_improper_symdiff_volume']:.4f}); notched tetrahedron chiral = {hd['notched_tet']['chiral']} ({hd['notched_tet']['smallest_improper_symdiff_volume']:.4f}); T− = point reflection of T+: symmetric difference {hd['Tminus_is_point_reflection_of_Tplus_symdiff']:.1e} (dented), {hd['notched_Tminus_is_point_reflection_symdiff']:.1e} (notched).")
rep = rep.replace('@@SOLIDITY@@', '\n'.join('- ' + s for s in sol))
gr = P['middle_rest']['genus']
rep = rep.replace('@@REST_GENUS@@', (f"The middle rest has genus {gr}: it is a closed ring round the Penrose core (the rhombus footprint lies strictly inside H's footprint). Core and rest are each one solid, as step 15 says, but the core can only be inserted or removed along the five-fold axis, i.e. before the second OCD is placed. Kit B's rest has genus {P['B_rest']['genus']} too." if gr == 1 else f"The middle rest has genus {gr} (mesh); not a ring."))
assert '@@' not in rep, [l for l in rep.splitlines() if '@@' in l]
open(os.path.join(HERE, '..', 'REPORT.md'), 'w').write(rep); print('report filled')
