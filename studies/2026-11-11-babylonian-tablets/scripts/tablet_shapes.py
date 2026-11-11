"""Pilot (DICTO 11 Nov: "are there any special geometric properties of ancient Babylonian clay tablets ... of the tablets themselves";
"and pilot for babylonian"). Data: HeiCuBeDa Hilprecht (Mara, Bogacz, Bayer; heiDATA doi:10.11588/data/IE8CCN, CC BY-SA 4.0), the
catalogue HeiCuBeDa_B_Hilprecht_Database_240121.json: per tablet the 3D-measured bounding box (cm), surface area (cm2), volume (cm3),
and from CDLI period, genre, provenience. Shape numbers per tablet (L >= W >= T the box sides):
  aspect L/W, flatness T/W; fill f = V / (L W T) (box 1, cylinder-like 0.785, ellipsoid pi/6 = 0.524);
  compactness q = 36 pi V^2 / A^3 (sphere 1).
Grouped by period and genre; whole tablets only (CDLI remarks/genre without 'fragment', and fill >= 0.35 to drop broken pieces).
Control: the numbers are dimensionless and unit-free; a check that L W T >= V for every tablet."""
import json, sys, re, math, statistics as st
from collections import defaultdict
D = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'hilprecht_db.json'))
rows = []; bad = 0
for k, r in D.items():
    g = r.get('from_gigamesh_info_file', {}); c = r.get('from_cdli_search_view', {}) or {}
    try:
        L, W, T = sorted(map(float, g['bounding_box_in_cm']), reverse=True); A = float(g['area_in_cm2']); V = float(g['volume_dx_in_cm3'])
    except Exception: bad += 1; continue
    if V <= 0 or A <= 0: bad += 1; continue
    text = ' '.join(str(c.get(x, '')) for x in ('remarks', 'genre', 'object_type')).lower()
    per = re.sub(r'\s*\(.*', '', str(c.get('period', '') or 'unknown')).strip() or 'unknown'
    gen = (str(c.get('genre', '') or 'unknown').split(';')[0].strip() or 'unknown')
    rows.append(dict(id=k, L=L, W=W, T=T, A=A, V=V, f=V / (L * W * T), q=36 * math.pi * V ** 2 / A ** 3, asp=L / W, flat=T / W,
                     per=per, gen=gen, frag='fragment' in text))
whole = [r for r in rows if not r['frag'] and r['f'] >= 0.35]
print(f'tablets with measures {len(rows)} (unusable {bad}); whole for the pilot {len(whole)}')
box_ok = all(r['f'] <= 1.0001 for r in rows)   # control: no tablet's volume exceeds its box
def summ(rs, label):
    if len(rs) < 8: return
    q = lambda key: (st.median(r[key] for r in rs), st.quantiles([r[key] for r in rs], n=4))
    a, aq = q('asp'); f, fq = q('f'); t, tq = q('flat'); c, cq = q('q')
    print(f'  {label:38s} n={len(rs):4d}  L/W {a:.3f} [{aq[0]:.2f}-{aq[2]:.2f}]  T/W {t:.3f}  fill {f:.3f} [{fq[0]:.3f}-{fq[2]:.3f}]  compact {c:.3f}')
summ(whole, 'ALL whole tablets')
by = defaultdict(list)
for r in whole: by[('period', r['per'])].append(r); by[('genre', r['gen'])].append(r)
for key in sorted(by, key=lambda k: (k[0], -len(by[k]))): summ(by[key], f'{key[0]}: {key[1][:28]}')
# aspect ratio histogram: any preference for simple ratios?
H = defaultdict(int)
for r in whole: H[round(r['asp'] / 0.05) * 0.05] += 1
print('  L/W histogram (bins of 0.05):', ' '.join(f'{b:.2f}:{H[b]}' for b in sorted(H) if H[b] >= 5))
# size law: thickness against width (log-log slope)
xs = [math.log(r['W']) for r in whole]; ys = [math.log(r['T']) for r in whole]; mx, my = st.mean(xs), st.mean(ys)
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
print(f'  size law: thickness ~ width^{slope:.3f} (1 = same shape at every size)')
json.dump(rows, open('tablet_shapes.json', 'w'))
print('FINAL ok' if box_ok and len(whole) > 100 else 'FINAL FAIL (a volume exceeds its box, or too few whole tablets)')
