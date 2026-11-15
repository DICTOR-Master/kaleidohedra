#!/usr/bin/env python3
"""Crochet pattern for Narcissus (and the cube) from the exact faces, with the geometry check.
All HexOct faces at lambda = 3/8 are of three kinds only (data/faces.json, scripts/faces.py):
  square of side L (Narcissus x3, cube x6), regular hexagon of side L*sqrt(2/3) (Narcissus x1),
  right triangle with legs L/sqrt(3), L*sqrt(2/3) and hypotenuse L (Narcissus x6),  where L = a/sqrt(2), a = ball spacing.
Every face is worked flat in rows of single crochet (sc); slanted sides by evenly spread increases/decreases at one or both edges.
GAUGE ASSUMPTION (state it, swatch it): sc in DK cotton on a 4.0 mm hook, 18 sts and 20 rows to 10 cm (1.8 st/cm, 2.0 rows/cm).
The script picks the square side L (6.0 to 10.0 cm in 0.5 cm steps) whose whole-stitch counts give the smallest worst error,
then computes every side and corner angle back from the counts and compares with the true values."""
import json, math, sys
GS, GR = float(sys.argv[1]) if len(sys.argv) > 1 else 1.8, float(sys.argv[2]) if len(sys.argv) > 2 else 2.0
R23 = math.sqrt(2/3)
def plan(L):
    t = L*R23; p = L/math.sqrt(3); q = L*R23
    sq = {'sts': round(L*GS), 'rows': round(L*GR)}
    sq_chk = {'width': sq['sts']/GS, 'height': sq['rows']/GR}
    nb = round(t*GS); rt = round(t*math.sqrt(3)*GR); rt += (rt % 2 == 0)   # odd total: one widest middle row
    rh = (rt - 1)//2                            # rows below (and above) the middle row
    nm = 2*nb                                   # widest row = twice the bottom row (regular hexagon)
    hx = {'bottom_sts': nb, 'middle_sts': nm, 'total_rows': rt, 'rows_each_half': rh, 'increases_each_edge': (nm - nb)//2}
    sl = math.hypot((nm - nb)/2/GS, rt/2/GR)       # slanted side spans half the total height
    hx_chk = {'bottom/top side': nb/GS, 'slanted side': sl, 'width': nm/GS, 'height': rt/GR,
              'corner angle at bottom': math.degrees(math.pi - math.atan2(rt/2/GR, (nm - nb)/2/GS))}
    nq = round(q*GS); rp = round(p*GR)
    tr = {'first_row_sts': nq, 'rows': rp, 'decreases_on_slanted_edge': nq - 1}
    hyp = math.hypot(nq/GS, rp/GR)
    tr_chk = {'long leg': nq/GS, 'short leg': rp/GR, 'hypotenuse': hyp, 'angle at long leg end': math.degrees(math.atan2(rp/GR, nq/GS))}
    true = {'square side': L, 'hexagon side': t, 'triangle short leg': p, 'triangle long leg': q, 'triangle hypotenuse': L}
    got = {'square side': (sq_chk['width'], sq_chk['height']), 'hexagon side': (hx_chk['bottom/top side'], hx_chk['slanted side']),
           'triangle short leg': (tr_chk['short leg'],), 'triangle long leg': (tr_chk['long leg'],), 'triangle hypotenuse': (tr_chk['hypotenuse'],)}
    err = {k: [round(100*(g/true[k] - 1), 2) for g in got[k]] for k in true}
    worst = max(abs(e) for v in err.values() for e in v)
    return {'L_cm': L, 'a_cm': L*math.sqrt(2), 'square': sq, 'square_check_cm': sq_chk, 'hexagon': hx, 'hexagon_check': hx_chk,
            'triangle': tr, 'triangle_check': tr_chk, 'true_cm': true, 'error_percent': err, 'worst_percent': worst,
            'true_angles': {'hexagon corner': 120.0, 'triangle acute angle at long leg end': math.degrees(math.atan(1/math.sqrt(2)))}}
cands = [plan(6 + 0.5*k) for k in range(9)]
for c in cands: print(f"L = {c['L_cm']:.1f} cm: worst error {c['worst_percent']:.2f} %")
best = min(cands, key=lambda c: c['worst_percent'])
def spread(n_events, n_rows):
    """rows (1-based) on which to place n_events evenly over n_rows (Bresenham)"""
    return [r for r in range(1, n_rows + 1) if (r*n_events)//n_rows > ((r - 1)*n_events)//n_rows]
hx = best['hexagon']; tr = best['triangle']
inc, rh = hx['increases_each_edge'], hx['rows_each_half']
best['hexagon']['increase_rows'] = [2*k for k in range(1, inc + 1)] if 2*inc == rh + 1 else [r + 1 for r in spread(inc, rh)]   # rows 2..rh+1 (the middle row is rh+1); every second row when it fits
best['hexagon']['decrease_rows'] = sorted(hx['total_rows'] + 2 - r for r in best['hexagon']['increase_rows'])
best['triangle']['decrease_schedule'] = [((r*tr['decreases_on_slanted_edge'])//(tr['rows'] - 1)) - (((r - 1)*tr['decreases_on_slanted_edge'])//(tr['rows'] - 1)) for r in range(1, tr['rows'])]
best['gauge'] = {'sts_per_10cm': GS*10, 'rows_per_10cm': GR*10}
areas = {'Narcissus': 3*best['L_cm']**2 + 3*math.sqrt(3)/2*(best['L_cm']*R23)**2 + 6*0.5*(best['L_cm']/math.sqrt(3))*(best['L_cm']*R23), 'cube': 6*best['L_cm']**2}
best['face_area_cm2'] = {k: round(v, 1) for k, v in areas.items()}
json.dump(best, open('data/pattern.json', 'w'), indent=1)
print(json.dumps(best, indent=1))
