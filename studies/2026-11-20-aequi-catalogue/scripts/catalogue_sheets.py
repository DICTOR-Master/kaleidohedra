# Contact sheets of the main catalogue, in catalogue order, each panel captioned by its catalogue name and number.
# Reuses the per-die renders (solid and Vacuus) made by render.py of study 2026-11-19-aequi-complete from its 80-digit
# corners, and that script's sheet layout and save_small.
# usage: catalogue_sheets.py catalogue.json DIE_FIG_DIR RENDER_PY OUT_DIR
import json, sys, os, glob, importlib.util, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.image as mpimg
spec = importlib.util.spec_from_file_location('render', sys.argv[3]); render = importlib.util.module_from_spec(spec); spec.loader.exec_module(render)
rows = json.load(open(sys.argv[1])); figdir, out = sys.argv[2], sys.argv[4]
def pics(r):
    return [glob.glob(os.path.join(figdir, '%04d-*-%s.png' % (r['study_row'], k))) for k in ('solid', 'vacuus')]
def caption(r):
    tail = [x for x in (r['D'], 'Mosaicus' if r['mosaicus'] == 'yes' else '', 'two hands' if r['hands'].startswith('two') else '') if x]
    return '%s\nm=%d  %s' % (r['name'], r['m'], '  '.join(tail))
PER, COLS = 40, 4
made, bad = [], []
for g in ['Ih', 'Oh', 'Td', 'Th', 'T']:
    L = [r for r in rows if r['group'] == g]
    pages = [L[i:i + PER] for i in range(0, len(L), PER)]
    for pi, page in enumerate(pages):
        rws = (len(page) + COLS - 1) // COLS; H = rws * 2.5 + 0.5
        fig = plt.figure(figsize=(COLS * 4.2, H), dpi=80)
        for i, r in enumerate(page):
            P = pics(r)
            if any(len(p) != 1 for p in P): bad.append(r['name']); continue
            for j in range(2):
                ax = fig.add_axes([(i % COLS + j * 0.5) / COLS, 1 - (i // COLS + 1) * (2.5 / H), 0.5 / COLS, 2.0 / H])
                ax.imshow(mpimg.imread(P[j][0])); ax.set_axis_off()
            fig.text((i % COLS + 0.5) / COLS, 1 - (i // COLS + 1) * (2.5 / H) + 2.02 / H, caption(r), ha='center', va='bottom', fontsize=8, linespacing=1.15)
        fig.suptitle('Main catalogue of the Aequi, symmetry %s: %d dice%s. Solid (orbit tones are labels only) and Vacuus (slate sloping, sand on a mirror)'
                     % (g, len(L), '' if len(pages) == 1 else ', page %d of %d' % (pi + 1, len(pages))), fontsize=10, y=0.999)
        p = os.path.join(out, 'catalogue-%s%s.png' % (g, '' if len(pages) == 1 else '-p%d' % (pi + 1)))
        render.save_small(fig, p, 128); plt.close(fig); made.append(p)
n = sum(1 for r in rows)
print('sheets', len(made), [os.path.basename(p) for p in made])
print('FINAL ok' if not bad and len(made) == 8 and all(os.path.exists(p) for p in made) and n == 149 else 'FINAL FAIL: missing pictures %s' % bad)
