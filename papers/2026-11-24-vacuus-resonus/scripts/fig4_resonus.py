#!/usr/bin/env python3
"""DICTO · dictospheres.com. Figure 4 of draft v1 of "The Vacuus and the Resonus" (24 Nov 2026): the 4D walls of the Queens (#110,
Figure 8) labelled as the Resonus. The drawing is that of study 2026-11-16-queens-shadows (scripts/render_shadows.py, data/shadows.json),
reused unchanged: the White Queen's (600-cell) corner-first shadow, with the 15 mirror walls and the 30 cross walls that stay flat in
this view. Only the words change: the 60 mirrors are the planes of Resonus(120-cell) and the 300 cross walls those of Resonus(600-cell)
(Theorem 8(e) of the paper). Usage, from the paper folder: python scripts/fig4_resonus.py   (ends FINAL ok)."""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
STUDY = os.path.normpath(os.path.join(ROOT, '..', '..', 'studies', '2026-11-16-queens-shadows'))
sys.path.insert(0, os.path.join(STUDY, 'scripts'))
import render_shadows as RS

js = json.load(open(os.path.join(STUDY, 'data', 'shadows.json')))
sh = next(s for s in js['shadows'] if (s['queen'], s['type']) == ('600', 'V'))
shapes = RS.vacuus_shapes(sh); size = 1100; s2 = int((size - 120 * size / 1100) / 2)
# the view of render_shadows.py, unchanged
m0 = np.array([w['n'] for w in sh['wall_normals_3d'] if w['kind'] == 'mirror'][0])
v0 = np.array(shapes[0]['X3'][0]); v0 = v0 / np.linalg.norm(v0)
ax = np.cross(v0, m0); ax = ax if np.linalg.norm(ax) > 1e-6 else np.cross(v0, [1, 0.3, 0.1])
vd = RS.rot(ax, 9) @ RS.rot(m0, 5) @ v0; up = m0 - (m0 @ vd) * vd; M = RS.look(vd, up)
main = RS.panel(sh, shapes, ('mirror', 'cross'), size, M)
pm = RS.panel(sh, shapes, ('mirror',), s2, M); pc = RS.panel(sh, shapes, ('cross',), s2, M)
W = sh['walls']; assert (W['mirror'], W['cross']) == (15, 30), W
names = [L['name'].split(' (')[0] for L in shapes]
title = ['The Resonus of the Queens, in the White Queen\'s corner-first shadow',
         f"{W['mirror'] + W['cross']} walls stay flat in this view: {W['mirror']} of Resonus(120-cell) (sky) + {W['cross']} of Resonus(600-cell) (apricot)"]
legend = ['All 60 mirrors of the 600-cell are the Resonus of the 120-cell; its 300 cross walls are the Resonus of the 600-cell.',
          'Inner outlines, inside out: ' + ', '.join(names) + ' (innermost opaque pink, the others see-through shells);',
          'every edge fin from the shadow\'s centre lies in a kept wall. Faint cage: the shadow\'s hull. Each disc is the trace of a wall.']
out = os.path.join(ROOT, 'figures', 'fig4-queens-resonus.png')
RS.sheet(main, [(pm, f"{W['mirror']} planes: Resonus(120-cell)", RS.WALLCOL['mirror']),
                (pc, f"{W['cross']} planes: Resonus(600-cell)", RS.WALLCOL['cross'])], title, legend, out)
print('wrote', os.path.relpath(out, ROOT), 'shapes', names); print('FINAL ok')
