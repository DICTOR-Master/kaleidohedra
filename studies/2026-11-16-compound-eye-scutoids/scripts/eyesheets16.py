#!/usr/bin/env python3
"""Contact sheets of every flagged neighbour change of the gw16 trace, for sorting by eye (kept on the compute machine: derived
crops of unlicensed data, never in git). Each change is one strip of three crops (top, middle, bottom plane of its segment,
2.4 lattice periods wide): the pair in red with a line, the two opposite columns in blue, other trusted columns green. The
frame colour gives the rule call of eyesum16.py (red true, yellow near-tie, grey artefact); the label is the change key.
Usage: eyesheets16.py RUN_DIR SUM16_JSON OUT_DIR"""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eyetrace as et

RUN, SUMF, OUT = sys.argv[1:4]; os.makedirs(OUT, exist_ok=True)
SU = json.load(open(SUMF)); S = json.load(open(f'{RUN}/summary.json'))
info = {}
for p in S['patches']:
    for g in p.get('segments', []):
        for li in g.get('lost_info', []): info[f"{p['patch']}:{g['depth_um'][0]}:{li['pair'][0]}-{li['pair'][1]}"] = li
COL = {'true': (230, 57, 70), 'near-tie': (240, 200, 40), 'artefact': (130, 130, 130)}
W = 64; strips = {'true': [], 'near-tie': [], 'artefact': []}; planes = {}
for key, c in sorted(SU['calls'].items()):
    pt, s0, pr = key.split(':'); i, j = map(int, pr.split('-'))
    if (pt, s0) not in planes:                       # band-passed planes computed once per segment
        Z = dict(np.load(f'{RUN}/p{pt}_{s0}_planes.npz')); per = float(Z['period']); et.BANDPASS = True
        for nm in ('top', 'mid', 'bot'): Z[nm] = et.norm_img(np.asarray(Z[nm], np.float32), 0.15 * per, 1.2 * per)
        planes = {(pt, s0): Z}
    Z = planes[(pt, s0)]; sm = Z['sm']; inter = Z['inter']; per = float(Z['period']); K = len(sm); h = int(1.2 * per)
    li = info.get(key, {}); opp = li.get('opposite', [])
    row = []
    for img, k in ((Z['top'], 0), (Z['mid'], K // 2), (Z['bot'], K - 1)):
        z = img
        cc = ((sm[k, i] + sm[k, j]) / 2).round().astype(int); a0, b0 = cc - h
        cr = np.pad(z, h, mode='edge')[a0 + h:a0 + 3 * h, b0 + h:b0 + 3 * h]
        im = Image.fromarray((np.clip((cr + 2.5) / 5, 0, 1) * 255).astype(np.uint8)).convert('RGB').resize((W, W)); dr = ImageDraw.Draw(im); f = W / (2 * h)
        for q in np.flatnonzero(np.linalg.norm(sm[k] - cc, axis=1) < 1.3 * h):
            y, x = (sm[k, q] - (a0, b0)) * f; col = (230, 57, 70) if q in (i, j) else (60, 120, 255) if q in opp else (123, 211, 137) if inter[q] else (90, 90, 90)
            dr.ellipse([x - 2, y - 2, x + 2, y + 2], outline=col)
        yi, xi = (sm[k, i] - (a0, b0)) * f; yj, xj = (sm[k, j] - (a0, b0)) * f; dr.line([xi, yi, xj, yj], fill=(230, 57, 70))
        row.append(np.asarray(im))
    st = Image.fromarray(np.concatenate(row, 1)); fr = Image.new('RGB', (3 * W + 4, W + 14), COL[c['call']]); fr.paste(st, (2, 2))
    ImageDraw.Draw(fr).text((3, W + 2), key, fill=(0, 0, 0)); strips[c['call']].append(fr)
for cl, L in strips.items():
    for n in range(0, len(L), 60):
        part = L[n:n + 60]; cols = 6; rows = (len(part) + cols - 1) // cols
        sh = Image.new('RGB', (cols * (3 * W + 6), rows * (W + 16)), (255, 255, 255))
        for m, fr in enumerate(part): sh.paste(fr, ((m % cols) * (3 * W + 6), (m // cols) * (W + 16)))
        sh.save(f'{OUT}/{cl}_{n // 60:02d}.png')
    print(cl, len(L), 'strips')
print('SHEETS ok')
