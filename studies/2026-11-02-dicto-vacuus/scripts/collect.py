# DICTO Vacuus census: collects data/shapes/*.json (vacuus.py) into data/vacuus-census.json and data/collect.log.
#  - one summary row per solid; flags: all fins congruent, accidental congruences (fewer congruence classes than symmetry orbits),
#    rational-pi apex and wedge angles (exact test), right-triangle fins, not well defined (O outside a face plane), non-convex but
#    well defined;
#  - solids with the same fin set up to similarity (multiset of (|OA|^2, |OB|^2, |AB|^2) / R^2, R = largest corner distance, 1e-8);
#  - the polar check, for every well-defined solid P: P* = polar reciprocal about the same centre O (numerical, float64); verified
#    (1) apex angles of P* = pi - edge dihedrals of P, (2) wedges of P* = pi - face angles of P, (3) the fin of e and the fin of its
#    dual edge e* lie in perpendicular planes that meet along the line from O through the foot of the perpendicular on e.
# Usage: collect.py <shapes dir> <index.csv> <out dir>
import sys, os, json, glob, math, csv, collections, numpy as np
SH, IDX, OUT = sys.argv[1:4]
D = {}
for r in csv.DictReader(l for l in open(IDX) if not l.startswith('#')):
    if r.get('dataset_file'): D[os.path.basename(r['dataset_file'])] = r['universal_number']
log = open(os.path.join(OUT, 'collect.log'), 'w')
def P(*a): print(*a, flush=True); print(*a, file=log)
S = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(SH, '*.json')))]
ORDER = {'Platonic': 0, 'Archimedean': 1, 'Catalan': 2, 'DICTO Solids v7': 3}
S.sort(key=lambda r: (ORDER[r['family']], r['name']))
rows = []
def polar_check(r):
    V = np.array(r['points']); F = r['faces']; NF = []
    for f in F:
        n = np.zeros(3)
        for k in range(len(f)): n += np.cross(V[f[k]], V[f[(k + 1) % len(f)]])
        NF.append(n)
    Pp = np.array([n / (n @ V[f[0]]) for n, f in zip(NF, F)])            # poles of the face planes (unit sphere)
    E = {}
    for i, f in enumerate(F):
        for k in range(len(f)): a, b = f[k], f[(k + 1) % len(f)]; E[(a, b)] = i
    e1 = e2 = e3 = 0.0
    for (a, b), i in E.items():
        if a > b: continue
        j = E[(b, a)]                                                      # i: face with a->b, j: face with b->a
        A, B = Pp[i], Pp[j]; apex = math.atan2(np.linalg.norm(np.cross(A, B)), A @ B)
        n1, n2 = NF[i] / np.linalg.norm(NF[i]), NF[j] / np.linalg.norm(NF[j]); dih = math.pi - math.atan2(np.linalg.norm(np.cross(n1, n2)), n1 @ n2)
        e1 = max(e1, abs(apex - (math.pi - dih)))
        m1, m2 = np.cross(V[a], V[b]), np.cross(A, B)                        # normals of fin(e) and fin(e*)
        e3 = max(e3, abs(m1 @ m2) / np.linalg.norm(m1) / np.linalg.norm(m2))
    # wedges of P*: face of P* = corner v of P; corners of that face = poles of the faces at v; wedge at the ray to pole f* between the
    # fins (f*, g1*) and (f*, g2*), g1, g2 the faces across the two edges of f at v
    for i, f in enumerate(F):
        m = len(f)
        for k in range(m):
            u, v, w = f[k - 1], f[k], f[(k + 1) % m]
            g1, g2 = E[(v, u)], E[(w, v)]
            X = Pp[i]; p1 = Pp[g1] - (Pp[g1] @ X) / (X @ X) * X; p2 = Pp[g2] - (Pp[g2] @ X) / (X @ X) * X
            wedge = math.atan2(np.linalg.norm(np.cross(p1, p2)), p1 @ p2)
            x, y = V[u] - V[v], V[w] - V[v]; fa = math.atan2(np.linalg.norm(np.cross(x, y)), x @ y)
            e2 = max(e2, abs(wedge - (math.pi - fa)))
    return e1, e2, e3
def sig(r): return tuple(sorted((round(f['OA2'] / r['R2'], 8), round(f['OB2'] / r['R2'], 8), round(f['AB2'] / r['R2'], 8)) for f in r['fin_list']))
groups = collections.defaultdict(list); cgroups = collections.defaultdict(list)
for r in S:
    r['D'] = D.get(r['src'], '')
    for c in r['classes']: c['OA2n'], c['OB2n'], c['AB2n'] = c['OA2'], c['OB2'], c['AB2']
    rat = sorted({c['apex_rational_pi'] for c in r['classes'] if c['apex_rational_pi']})
    wrat = sorted({w['rational_pi'] for w in r['wedge_classes'] if w['rational_pi']})
    right = sorted({(''.join(c['right_angle']), round(c['apex_deg'], 4)) for c in r['classes'] if c['right_angle']})
    pc = polar_check(r) if r['well_defined'] else None
    row = dict(src=r['src'], name=r['name'], family=r['family'], D=r['D'], field=r['field'], exact=r['exact'], convex=r['convex'],
               V=r['V'], E=r['E'], F=r['F'], symmetry_order=r['symmetry_order'], well_defined=r['well_defined'], faces_O_not_inside=r['faces_O_not_inside'],
               fins=r['fins'], fin_classes=r['fin_classes'], fin_orbits=r['fin_orbits'], all_congruent=r['all_congruent'],
               accidental=r['accidental_congruence'], apex_deg=sorted({round(c['apex_deg'], 4) for c in r['classes']}),
               apex_rational=rat, wedge_rational=wrat, wedge_classes=len(r['wedge_classes']), right=right, right_fins=r['right_fins'],
               polar_check=pc, classes=r['classes'], wedge_list=r['wedge_classes'], face_patterns=r['face_patterns'], corner_patterns=r['corner_patterns'],
               corner_sum_err=r['corner_sum_err'], struts=r['struts'], strut_lengths=r['strut_lengths'], strut_classes=r['strut_classes'],
               strut_min_angle_deg=r['strut_min_angle_deg'], edge_lengths=r['edge_lengths'], fin_planes=r['fin_planes'], flat_sheets=r['flat_sheets'], sheet_sizes=r['sheet_sizes'], central_discs=r['central_discs'], frame_lengths=r['frame_lengths'], solid_angle_err=r['solid_angle_err'])
    rows.append(row)
    groups[sig(r)].append(r['name'])
    cgroups[tuple(sorted({(round(c['OA2'] / r['R2'], 8), round(c['OB2'] / r['R2'], 8), round(c['AB2'] / r['R2'], 8)) for c in r['classes']}))].append(r['name'])
P('solids', len(rows), '| exact', sum(r['exact'] for r in rows), '| well defined', sum(r['well_defined'] for r in rows))
P('\nALL FINS CONGRUENT:', [r['name'] for r in rows if r['all_congruent']])
P('\nACCIDENTAL CONGRUENCE (classes < symmetry orbits):', [(r['name'], r['fin_classes'], r['fin_orbits']) for r in rows if r['accidental']])
P('\nRATIONAL-PI APEX ANGLES:'); [P('  ', r['name'], r['apex_rational'], 'of', r['apex_deg']) for r in rows if r['apex_rational']]
P('\nRATIONAL-PI WEDGES:'); [P('  ', r['name'], r['wedge_rational']) for r in rows if r['wedge_rational']]
P('\nRIGHT-TRIANGLE FINS:'); [P('  ', r['name'], r['right'], r['right_fins'], 'of', r['fins']) for r in rows if r['right']]
P('\nSTRUTS: ONE CENTRE-STRUT LENGTH:', [r['name'] for r in rows if r['strut_lengths'] == 1])
P('STRUTS: TWO CENTRE-STRUT LENGTHS:', [r['name'] for r in rows if r['strut_lengths'] == 2])
P('FRAME (centre struts + edges) IN AT MOST TWO LENGTHS:', [(r['name'], r['frame_lengths']) for r in rows if r['frame_lengths'] <= 2])
P('FRAME IN THREE LENGTHS:', [r['name'] for r in rows if r['frame_lengths'] == 3])
P('\nFINS JOINING INTO FLAT SHEETS (coplanar fins on a common ray; sheets < fins):', [(r['name'], r['fins'], r['flat_sheets'], r['sheet_sizes']) for r in rows if r['flat_sheets'] < r['fins']])
P('\nCENTRAL DISCS (a flat sheet closing all round O: a central polygon of the solid, sides = fins):', [(r['name'], r['central_discs']) for r in rows if r['central_discs']])
P('\nNOT WELL DEFINED:', [(r['name'], r['faces_O_not_inside']) for r in rows if not r['well_defined']])
P('\nNON-CONVEX, WELL DEFINED:', [r['name'] for r in rows if r['well_defined'] and r['convex'] is False])
P('\nSAME FIN MULTISET (up to similarity):'); [P('  ', g) for g in groups.values() if len(g) > 1]
P('\nSAME FIN CLASSES (ignoring counts), not already above:'); [P('  ', g) for k, g in cgroups.items() if len(g) > 1 and not any(set(g) == set(h) for h in groups.values())]
pcs = [r['polar_check'] for r in rows if r['polar_check'] and r['convex'] is not False]
P('\nPOLAR CHECK over', len(pcs), 'convex', 'solids: max |apex(P*) - (pi - dihedral(P))| = %.1e; max |wedge(P*) - (pi - face angle(P))| = %.1e; max |cos(fin(e), fin(e*))| = %.1e'
  % tuple(max(x[i] for x in pcs) for i in range(3)))
pn = [(r['name'], r['polar_check']) for r in rows if r['polar_check'] and r['convex'] is False]
P('non-convex, well defined (polar not a convex solid): (1) max %.1e, (3) max %.1e; (2) fails, as expected:' % (max(x[1][0] for x in pn), max(x[1][2] for x in pn)), [x[0] for x in pn if x[1][1] > 1e-9])
json.dump(dict(rows=rows, same_fin_multiset=[g for g in groups.values() if len(g) > 1],
               same_fin_classes=[g for g in cgroups.values() if len(g) > 1]), open(os.path.join(OUT, 'vacuus-census.json'), 'w'), indent=1, default=str)
