# DICTO · dictospheres.com — the Fullerene-Amber Cell completed with scutoids only (DICTO's combined method, bcc mould at 6/5 s0, centroid
# seeds; geometry and checks from scenes2.py): complete (mould outline only) and exploded (each piece moved out by 1.7 x its centre; no mould). Writes renders/amber.html (p0 complete, p1 exploded, p2 exploded cutaway).
import os, sys
import numpy as np
import scenes2 as T
S = T.S; X = T.X; CP = T.CP; LOG = []
DIR = np.array([0.36, 0.30, 1.0]); u = DIR / np.linalg.norm(DIR)


def normal(c):
    bt = [t for t, l in zip(c['T'], c['lab']) if l == 'bottom'][0]
    n = np.cross(X[bt[1]] - X[bt[0]], X[bt[2]] - X[bt[0]]); n /= np.linalg.norm(n)
    return n if n @ X[bt[0]] > 0 else -n


NRM = {c['F']: normal(c) for c in CP}
outline = S.solid_part(T.mould, '#000000', rad=0.0022, edge_col=S.LIGHT, faces=[])
complete = [p for c in CP for p in T.combi_piece(c, np.zeros(3), 0.0016, dots=True)] + [outline]
for p in complete:
    if p['balls']: p['rad'] = 0.0016 * 3.0
F_ = 1.7                                            # pull: each piece moved by F_ x its centre (along its own direction from the cell centre)
def exploded(keep):
    parts = [S.c1_whole(0.0026)]
    for c in CP:
        if keep(NRM[c['F']]): parts += T.combi_piece(c, F_ * X[sorted({v for t_ in c['T'] for v in t_})].mean(0), 0.0024, dots=True)
    for p in parts:
        if p.get('balls') and not p['t']: p['rad'] = 0.0024 * 3.0
    return parts
ex_all = exploded(lambda n: True)
ex_cut = exploded(lambda n: n @ u < 0.35)           # cutaway: the pieces facing the viewer left out, so the star shows
n_cut = sum(1 for c in CP if NRM[c['F']] @ u < 0.35)
E1 = S.ext(complete, DIR, 1.06); E2 = max(S.ext(ex_all, DIR, 1.04), S.ext(ex_cut, DIR, 1.04))
write = T.write
write(os.path.join(S.OUT, 'amber.html'), [{'E': E1, 'dir': DIR.tolist(), 'parts': complete}, {'E': E2, 'dir': DIR.tolist(), 'parts': ex_all},
                                          {'E': E2, 'dir': DIR.tolist(), 'parts': ex_cut}])
LOG.append(f'amber.html: complete (80 scutoids, mould outline); exploded, all 80 moved by {F_} x their centres; cutaway, {n_cut} of 80 kept')
open(os.path.join(T.H, 'scenes4.log'), 'w').write('\n'.join(LOG) + '\nFINAL ok\n'); print('\n'.join(LOG)); print('FINAL ok')
