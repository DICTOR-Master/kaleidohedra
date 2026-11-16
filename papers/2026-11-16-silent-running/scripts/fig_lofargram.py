#!/usr/bin/env python3
"""Figure 1, the lofargram of silences. Drawn like a sonar LOFAR display: degree k across (the frequencies), one band per
point set, a bright vertical line where the set rings (T_k > 0, brightness from log T_k) and darkness where it is silent.
Data: data/fig-tones.json from scripts/fig_tones.py (zero patterns asserted there against the exact signatures).
Colours: label colours only, as in Figure 2 (X teal, F apricot, R slate), dark app ground.
Usage: fig_lofargram.py tones.json out.png   (ends FINAL ok / FINAL FAIL)"""
import sys, json
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

GROUND = '#05050a'; BAND = np.array([11, 13, 20]) / 255; INK = '#e6e1d3'; DIM = '#8d8a82'
# Label colours (16 Nov 2026, DICTO: app colours only for the solid they stand for): labels only, no element or solid meaning;
# the same palette in Silent Running and Walls of Silence; chosen apart from the five app solid colours, colour-blind checked.
LABEL = {'teal': (32, 168, 158), 'apricot': (240, 168, 138), 'pink': (240, 150, 192), 'slate': (100, 112, 136), 'cream': (240, 230, 190),
         'sky': (120, 200, 240), 'taupe': (176, 150, 140), 'aqua': (110, 230, 226)}
c = lambda n: tuple(v / 255 for v in LABEL[n])
GREY = (0.78, 0.78, 0.76); WHITE = (0.93, 0.92, 0.88)
fails = []
def check(ok, msg):
    print(('CHECK ok   ' if ok else 'CHECK FAIL ') + msg, flush=True)
    if not ok: fails.append(msg)

d = json.load(open(sys.argv[1])); S = d['sets']; K = d['kmax']
ROWS = [  # (key, label line 1, label line 2, colour, degrees to mark as vanished)
    ('ctrl-X (3,3,3,2,0)', 'ordinary S5-orbit', 'perms of (3, 3, 3, 2, 0)', GREY, []),
    ('X', 'X, golden (20)', 'perms of (φ², φ², φ², φ, 0)', c('teal'), [5, 7]),
    ('ctrl-F (3,3,2,2,0)', 'ordinary S5-orbit', 'perms of (3, 3, 2, 2, 0)', GREY, []),
    ('F', 'F, golden (30)', 'perms of (φ², φ², 1, 1, 0)', c('apricot'), [3, 6]),
    ('R', 'R = C3, A4 roots (20)', 'silent in 2 and every odd degree', c('slate'), []),
    ('600-cell', '600-cell (120)', 'reference: an 11-design', WHITE, []),
]
check(S['X']['T'] == S['-X']['T'] or np.allclose(S['X']['T'], S['-X']['T'], atol=1e-12), '−X has the same tones as X')
check(np.allclose(S['F']['T'], S['-F']['T'], atol=1e-12), '−F has the same tones as F')
for key, *_r, marks in ROWS:
    for k in marks: check(k in S[key]['silent'], f'{key}: marked degree {k} is silent')
check(S['ctrl-X (3,3,3,2,0)']['silent'] == [1, 2] and S['ctrl-F (3,3,2,2,0)']['silent'] == [1, 2], 'controls ring in every degree from 3')

LO, HI = -3.0, np.log10(0.25)
def bright(t): return 0.0 if abs(t) < d['zero'] else float(np.clip((np.log10(t) - LO) / (HI - LO), 0, 1))
check(all(bright(t) > 0 for key, *_r in ROWS for t in S[key]['T'] if abs(t) >= d['zero']) and
      min(t for key, *_r in ROWS for t in S[key]['T'] if abs(t) >= d['zero']) > 10 ** LO, 'every ringing tone is above the display floor')

W_IN, H_IN, DPI = 10.0, 5.3, 220
fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI, facecolor=GROUND)
ax = fig.add_axes([0.235, 0.12, 0.70, 0.80]); ax.set_facecolor(GROUND)
nR = len(ROWS); bh = 0.78
rng = np.random.default_rng(16)
for r, (key, l1, l2, col, marks) in enumerate(ROWS):
    y0 = nR - 1 - r - bh / 2
    # the band: low-level sea noise (deterministic), so the silent degrees read as dark gaps in a live trace
    nx, ny = 400, 24; noise = rng.random((ny, nx)) * 0.035 + 0.01
    img = np.clip(BAND[None, None, :] + noise[..., None] * np.array([0.6, 0.8, 1.0]), 0, 1)
    ax.imshow(img, extent=(0.5, K + 0.5, y0, y0 + bh), aspect='auto', interpolation='nearest', zorder=1)
    for k in range(1, K + 1):
        t = S[key]['T'][k - 1]; b = bright(t)
        if b > 0:
            lc = tuple(np.clip(np.array(col) * (0.45 + 0.55 * b) + (1 - np.array(col)) * 0.35 * b ** 2, 0, 1))
            ax.add_patch(Rectangle((k - 0.11, y0 + 0.04), 0.22, bh - 0.08, color=lc, lw=0, zorder=3))
            ax.add_patch(Rectangle((k - 0.035, y0 + 0.04), 0.07, bh - 0.08, color=tuple(np.clip(np.array(lc) * 0.5 + 0.5, 0, 1)), lw=0, zorder=4))
    for k in marks:   # a vanished line: dashed outline where the ordinary orbit's line stands
        ax.add_patch(Rectangle((k - 0.3, y0 + 0.02), 0.6, bh - 0.04, fill=False, ec=col, lw=1.1, ls=(0, (3, 2)), zorder=5))
        ax.text(k, y0 + bh + 0.02, 'silent', color=col, fontsize=6.4, ha='center', va='bottom', zorder=6)
    fig.text(0.225, (y0 + bh / 2 + 0.5) / nR * 0.80 + 0.12 + 0.012, l1, color=col if col not in (GREY, WHITE) else INK, fontsize=8.6, ha='right', va='center')
    fig.text(0.225, (y0 + bh / 2 + 0.5) / nR * 0.80 + 0.12 - 0.030, l2, color=DIM, fontsize=7.0, ha='right', va='center')
ax.set_xlim(0.5, K + 0.5); ax.set_ylim(-0.5, nR - 0.5)
ax.set_xticks(range(1, K + 1)); ax.set_yticks([])
ax.tick_params(colors=INK, labelsize=7.6, length=2.5, width=0.8)
for s in ax.spines.values(): s.set_visible(False)
ax.set_xlabel('degree k (the frequency of the line)', color=INK, fontsize=8.6, labelpad=3)
fig.text(0.585, 0.955, r'Lines are the tones $T_k > 0$ (brighter = louder, log scale); dark = silent', color=DIM, fontsize=7.6, ha='center')
fig.text(0.985, 0.018, 'DICTO · dictospheres.com', color='#9a978f', fontsize=7.2, ha='right', va='bottom')
fig.savefig(sys.argv[2], dpi=DPI, facecolor=GROUND)
from PIL import Image
im = Image.open(sys.argv[2]); check(im.size == (int(W_IN * DPI), int(H_IN * DPI)), f'frame {im.size} at the asserted aspect {W_IN}:{H_IN}')
print('FINAL ok' if not fails else 'FINAL FAIL', flush=True)
