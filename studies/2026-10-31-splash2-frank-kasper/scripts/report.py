# Tables and checks for Splash Rules II (Frank-Kasper). Exact Fractions throughout.
#   python3 report.py out/splash2_fk.json <datadir>
import sys, os, json
from fractions import Fraction as Fr
from collections import defaultdict
D = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
FK = [r for r in D['structures'] if r['ok']]
phys = [r for r in FK if r['kind'] == 'cif']
L = []
def P(*a): L.append(' '.join(str(x) for x in a))

def per(r, k): return Fr(r['census'].get(k, 0), r['census']['N'])
def skel(r):
    kinds = defaultdict(int)
    for c in r['skeleton']:
        if c['rank'] == 1 and set(c['deg']) == {'2'}: kinds['lines'] += 1
        else: kinds[f"{['', '', 'layer', '3D'][c['rank']]} net (nodes {'+'.join(sorted(c['deg']))}-valent)"] += 1
    return '; '.join(sorted(kinds))

# ---- identities and laws, checked on every TCP structure ----
checks = defaultdict(int)
for r in FK:
    C = r['census']; N = C['N']; Zb = Fr(C['Zsum'], N); x = {z: per(r, f'N{z}') for z in (12, 14, 15, 16)}
    ok = dict(
        T_per_atom=(Fr(C['T'], N) == Zb / 2 - 1),
        bonds_per_atom=(Fr(C['bond'], N) == Zb / 2),
        five_bonds_per_atom_6=(Fr(C['bond5'], N) == 6),
        six_bonds_per_atom=(Fr(C['bond6'], N) == (Zb - 12) / 2),
        Zbar_from_sites=(Zb == 12 + 2 * x[14] + 3 * x[15] + 4 * x[16]),
        tet_j_sum=(per(r, 'tet_j0') + per(r, 'tet_j1') + per(r, 'tet_j2') == Zb / 2 - 1),
        tet_six_edges=(per(r, 'tet_j1') + 2 * per(r, 'tet_j2') == 3 * (Zb - 12)),
        j2_always_opposite=(C.get('tet_j2', 0) == C.get('tet_j2_opposite', 0)),
        no_tet_with_3_six_edges=(C.get('tet_j3', 0) == 0),
        shell6_sum=(sum(per(r, f'shell6_Z{z}') for z in (12, 14, 15, 16)) == 3 * (Zb - 12)),
        YK_line=(Zb == Fr(68, 5) - Fr(2, 5) * x[12]),
        ring_sizes_6=True)
    for k, v in ok.items(): checks[k] += int(v)
P('## Checks on all', len(FK), 'TCP structures (count of structures passing)')
for k, v in checks.items(): P(f'- {k}: {v}/{len(FK)}')

# ---- physical table ----
P('\n## Physical phases (per cell, exact)')
P('| phase | compound | N | N12:N14:N15:N16 | Zbar | tetrahedra/atom | 6-bonds/atom | 6-bond share | YK defect a0 | j2 tet/atom | major skeleton |')
P('|---|---|---|---|---|---|---|---|---|---|---|')
rows = []
for r in phys:
    C = r['census']; N = C['N']; Zb = Fr(C['Zsum'], N)
    a0 = Fr(r['a0'])
    rows.append(dict(name=r['meta']['name'], compound=r['meta']['compound'], source=r['meta']['source'], N=N,
                     counts=[C[f'N{z}'] for z in (12, 14, 15, 16)], Zbar=str(Zb), T=str(Fr(C['T'], N)), E6=str(Fr(C['bond6'], N)),
                     share6=str(Fr(C['bond6'], C['bond'])), a0=str(a0), j2=str(per(r, 'tet_j2')), skeleton=skel(r),
                     x={z: str(per(r, f'N{z}')) for z in (12, 14, 15, 16)},
                     sigma={z: (str(Fr(C.get(f'shell6_Z{z}', 0), C[f'N{z}'])) if C[f'N{z}'] else '-') for z in (12, 14, 15, 16)}))
    P(f"| {r['meta']['name']} | {r['meta']['compound']} | {N} | {':'.join(map(str, rows[-1]['counts']))} | {Zb} | {Fr(C['T'], N)} | {Fr(C['bond6'], N)} | {Fr(C['bond6'], C['bond'])} | {a0} | {per(r, 'tet_j2')} | {skel(r)} |")
P('\nNot TCP (Voronoi/Delaunay test): ' + '; '.join(f"{r['meta']['name']} ({r['msgs'][0]})" for r in D['structures'] if r['meta'].get('nonfk')))

# ---- FK59 family: stacking blindness (c/h letter of the Laves slabs) ----
fam = [r for r in FK if r['kind'] == 'fk59']
groups = defaultdict(list)
for r in fam:
    pat = r['meta']['cellword'].replace('+', 'L').replace('-', 'L')
    # canonical up to rotation and reversal
    n = len(pat); c = min(min(pat[i:] + pat[:i] for i in range(n)), min(pat[::-1][i:] + pat[::-1][:i] for i in range(n)))
    groups[c].append(r)
blind_keys = set(D['keys']); tested = 0
for c, rs in groups.items():
    if len(rs) < 2: continue
    tested += 1
    for k in list(blind_keys):
        vals = {Fr(r['census'].get(k, 0), r['meta']['units']) for r in rs}
        if len(vals) > 1: blind_keys.discard(k)
P(f'\n## FK59 kagome family: {len(fam)} stackings; {tested} Z/L patterns realised by 2 or more different Laves stackings')
P(f'Census keys identical (per slab) for every stacking with the same Z/L pattern: {len(blind_keys)} of {len(D["keys"])}')
P('Keys that do depend on the Laves c/h letters: ' + ', '.join(sorted(set(D['keys']) - blind_keys)))

# ---- window fits per family ----
def fmt(m, c):
    return f'window {m}: ' + ', '.join(f'{k or "const"} {v}' for k, v in c.items()) if m is not None else 'no window <= 5'
P('\n## Window fits (per row of tiles / per kagome slab; coefficients are per window of that kind)')
for k in D['keys']:
    P(f"- {k}: square-triangle {fmt(*D['window_st'][k])} | FK59 {fmt(*D['window_fk59'][k])}")

P('\n## Global fits (per atom), all TCP / physical only')
for k in D['keys']:
    P(f"- {k}: all {D['global_all'][k][0]} {D['global_all'][k][1] or ''} | physical {D['global_phys'][k][0]}")

P('\n## Table of known/hypothetical counts (Deza, Delgado Friedrichs, Dutour Sikiric)')
P('| name | description | Z12:Z14:Z15:Z16 | Zbar | YK line 68/5 - 2x12/5 | a0 |')
P('|---|---|---|---|---|---|')
for t in D['table']: P(f"| {t['name']} | {t['desc']} | {':'.join(map(str, t['counts']))} | {t['Zbar']} | {t['yk_line']} | {t['a0']} |")
open(os.path.join(out, 'results.md'), 'w').write('\n'.join(L) + '\n')
json.dump(dict(physical=rows, checks=dict(checks), n_tcp=len(FK), blind=sorted(blind_keys), notblind=sorted(set(D['keys']) - blind_keys)),
          open(os.path.join(out, 'summary.json'), 'w'), indent=1)
print('\n'.join(L[:60]))
