# s5_table.py -- the census table (CSV + JSON) of the 25 regular polytopes in 3D and 4D, from data/flags.json,
# s2_census3d.json, s3_census4d.json, s4_starturn.json. Study 2026-11-09-regular-stars-census.
# Usage: ~/geom/bin/python -u s5_table.py <data dir>
import sys, json, csv, os
D = sys.argv[1]
fl = json.load(open(os.path.join(D, 'flags.json'))); c3 = {r['symbol']: r for r in json.load(open(os.path.join(D, 's2_census3d.json')))}
c4 = {r['symbol']: r for r in json.load(open(os.path.join(D, 's3_census4d.json')))}; st = {r['symbol']: r for r in json.load(open(os.path.join(D, 's4_starturn.json')))}
def dual(sym): return '{' + ','.join(reversed(sym[1:-1].split(','))) + '}'
NAME = {r['symbol']: r['name'] for r in fl}
HULL3 = {'{3,5}': 'icosahedron', '{5,3}': 'dodecahedron', '{5/2,5}': 'icosahedron', '{5,5/2}': 'icosahedron', '{5/2,3}': 'dodecahedron', '{3,5/2}': 'icosahedron'}
KNOWN_STAR = {  # (symbol, t) -> what the star or its hull is (classical); every other star at 2 or phi: not named in the sources checked
    ('{4,3}', '2'): 'rhombic dodecahedron (the join; classical)',
    ('{4,3,3}', '2'): '24-cell (classical: tesseract + 8 cubic pyramids)',
    ('{3,3,4}', '2'): 'a stellation of the 16-cell (spike sides in its facet hyperplanes); hull the 24-cell',
    ('{3,4,3}', '2'): 'a stellation of the 24-cell (spike sides in its facet hyperplanes); hull = T(24-cell)'}
rows = []
order = ['{5,3}', '{3,5}', '{4,3}', '{3,3}', '{3,4}', '{5/2,5}', '{5,5/2}', '{5/2,3}', '{3,5/2}',
         '{5,3,3}', '{3,3,5}', '{4,3,3}', '{3,3,3}', '{3,3,4}', '{3,4,3}',
         '{3,5,5/2}', '{5/2,5,3}', '{5,5/2,5}', '{5,3,5/2}', '{5/2,3,5}', '{5/2,5,5/2}', '{5,5/2,3}', '{3,5/2,5}', '{3,3,5/2}', '{5/2,3,3}']
for sym in order:
    f = next(r for r in fl if r['symbol'] == sym); s = st[sym]; d = f['d']; convex = f['density'] == 1
    row = dict(dim=d, symbol=sym, name=f['name'], density=f['density'], counts='/'.join(map(str, f['counts'])),
               g_R2_over_h2=f['g'], g_f=round(f['g_float'], 6))
    if d == 3:
        c = c3[sym]; T = c['T_chain']
        row['T_chain'] = (f"period {T['period']}, gain {T['gain_radius']}" if convex else
                          f"corners only: the chain of its hull ({HULL3[sym]}), period {T['period']}, gain {T['gain_radius']}")
        co = c['core']
        row['star_core'] = (f"dual {NAME[dual(sym)]}; cycle period {co['period']} from turn {co['cycle_from_turn']}, two-turn radius scale t^2 x {co['scale_radius_t1']}"
                            if convex else f"first core: the convex hull of its face centres ({c['star_halo']['corners']} corners); then period {co['period']}, scale t^2 x {co['scale_radius_t1']}")
        row['star_halo'] = f"t x hull of face centres: {c['star_halo']['corners']} corners ({'the dual' if convex else 'a convex Platonic solid'})"
        row['polar_halo'] = f"the reciprocal {NAME[dual(sym)]}" + ('' if convex else f" (hull: {c['polar_halo']['corners']} corners)")
        ev = c['star_line_events']
        row['join_t'] = next(e['t'] for e in ev if e['what'].startswith('join'))
        row['edge_tangent_kis_t'] = '; '.join(e['t'] for e in ev if e['kind'] == 'metric')
        row['stellation_t'] = '; '.join(e['t'] for e in ev if 'stellation' in e['what'])
        for tn in ('2', 'phi'):
            x = c['stars'][tn]
            row[f'star_t{tn}'] = (KNOWN_STAR.get((sym, tn)) or ('not named in the sources checked; ' + x['state'])) + f"; {x['star_line_region']}; turned partner g/t = {x['turned_partner_f']:.6f}"
    else:
        c = c4[sym]; T = c['T_chain']
        row['T_chain'] = f"period 2, gain {T['gain_radius']}" if convex else T['note'] + ' (gain 28 - 12 sqrt5)'
        row['star_core'] = (f"dual {NAME[dual(sym)]}; period 2, two-turn radius scale t^2 x {c['core']['scale_radius_t1']}" if convex else c['core']['note'])
        row['star_halo'] = f"t x hull of the facet centres ({c['star_halo']['corners']} corners)"
        row['polar_halo'] = f"the reciprocal {NAME[dual(sym)]}"
        row['join_t'] = c['walls_t'][1]
        row['edge_tangent_kis_t'] = ''
        row['stellation_t'] = '; '.join(e['t'] for e in c['incidences'] if 'stellation' in e['what'])
        for tn in ('2', 'phi'):
            x = c['stars'][tn]
            row[f'star_t{tn}'] = (KNOWN_STAR.get((sym, tn)) or 'not named in the sources checked') + \
                f"; hop {x['hop']}{'; on a wall' if x['on_wall'] else ''}; turned partner g/t = {x['turned_partner_f']:.6f}"
    row['star_line_fixed_point_t'] = f"sqrt(g) = {f['g_float'] ** .5:.6f}"
    sc = s['scan']
    row['flag_line_tmin_at_turn'] = f"{s['turn_value_f']:.6f}"
    row['flag_line_tmin_at_ends'] = s['end_value']
    row['flag_line_peak'] = ('at the turn only (log-concave)' if convex else
                             ('global maximum at the turn, not log-concave' if s['turn_is_global_max'] else 'maximum at the two ends; the turn is not the maximum'))
    row['flag_local_turn_theorem'] = 'holds (closed form exact at every sample)' if all(e['unfolded_is_closed_form'] for e in s['exact']) else 'FAILS'
    row['known_or_new'] = ('Star Core, halos, cycle: classical duality; T gain known (#80)' if d == 3 and convex else
                           'Star Core, halos: classical (dual / hull of the reciprocal); values new as entries of DICTO\'s rules') + \
                          ('' if convex else '; flag-line peak result new')
    rows.append(row)
json.dump(rows, open(os.path.join(D, 'census_table.json'), 'w'), indent=1)
with open(os.path.join(D, 'census_table.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); [w.writerow(r) for r in rows]
ok = len(rows) == 25 and all(r['flag_local_turn_theorem'].startswith('holds') for r in rows)
for r in rows: print(r['symbol'], r['name'], r['g_f'], r['flag_line_peak'], '|', r['star_t2'][:90])
print('FINAL ok' if ok else 'FINAL FAIL: table incomplete or the flag-local turn theorem failed somewhere')
