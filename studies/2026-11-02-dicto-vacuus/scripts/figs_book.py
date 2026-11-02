# Two figures for #87 / The Centre Pyramids (DICTO): (1) pyramidise strip for the cube: centre pyramids, exploded, Star,
# Vacuus sheets, Vacuus struts; (2) census chart: fin apex angles over the well-defined solids of the census.
# Renderer imported from the Star Cores figure script (same look as the plates and Figure 8).
# Usage: figs_book.py <star-cores scripts dir> <census json> <out dir>
import sys, os, json, numpy as np
SC, CEN, OUT = [os.path.abspath(x) for x in sys.argv[1:4]]; sys.path.insert(0, SC)
sys.argv = [sys.argv[0], '.', OUT, os.path.expanduser('~/kres-tmp/book/dicto-logo.png')]
import figs_paper_a as A
import matplotlib.pyplot as plt

# ---- (1) strip ----
V = np.array([[x, y, z] for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)], float)
faces = A.hull_faces(V); M = A.rot(*A.VIEW); COLS = [A.GOLD, A.VIOLET, A.TEAL]
def fcol(n): return COLS[int(np.argmax(np.abs(n)))]           # opposite faces share a colour
def tris_scene(S, tris):
    TV, TF, TC = [], [], []
    for P, c in tris:
        k = len(TV); TV += list(P); TF.append(list(range(k, k + len(P)))); TC.append(c)
    S.tris(np.array(TV), TF, TC)
fig, axs = plt.subplots(1, 5, figsize=(12, 3.2), gridspec_kw=dict(wspace=0.02))
titles = ['1. centre pyramids', '2. exploded', '3. turned out: the Star', '4. Vacuus: SHEETS', '5. Vacuus: STRUTS']
O = np.zeros(3)
for k, ax in enumerate(axs):
    S = A.Scene(M); tris = []
    for Q, n in faces:
        d = float(n @ Q.mean(0)); c = fcol(n)
        if k in (0, 1):
            sh = 0.55 * n if k == 1 else 0
            for i in range(len(Q)):                              # both sides; the renderer culls the back one
                tris.append((np.array([O + sh, Q[(i + 1) % 4] + sh, Q[i] + sh]), c)); tris.append((np.array([O + sh, Q[i] + sh, Q[(i + 1) % 4] + sh]), c))
            tris.append((Q + sh, c))
        elif k == 2:
            tip = 2 * d * n
            for i in range(len(Q)): tris.append((np.array([Q[i], Q[(i + 1) % 4], tip]), c))
    if k == 3:                                                  # one fin per edge, both sides, coloured by its plane
        E = set()
        for Q, n in faces:
            for i in range(4): E.add(tuple(sorted((tuple(Q[i]), tuple(Q[(i + 1) % 4])))))
        for a, b in E:
            a, b = np.array(a), np.array(b); m = np.cross(a, b); c = COLS[[0, 1, 2][int(np.argmin(np.abs(m)))]]
            tris += [(np.array([O, a, b]), c), (np.array([O, b, a]), c)]
    if k in (0, 1, 2, 3): tris_scene(S, tris)
    if k == 4: S.shell(V)
    elif k == 3: S.shell(V)
    S.draw(ax, 2.05 if k in (1, 2) else 1.75)
    if k == 4:
        for p in V:
            P = np.array([O, p]) @ M.T; ax.plot(P[:, 0], P[:, 1], color=A.EDGE, lw=1.6)
        ax.plot(*(O @ M.T)[:2], 'o', color=A.EDGE, ms=4)
    ax.set_title(titles[k], fontsize=9)
fig.text(0.5, 0.02, "Pyramidise (DICTO): the cube split into its six centre pyramids, which can be exploded, turned out into the Star "
         "(twice the volume: the rhombic dodecahedron), or emptied to the walls they share", ha='center', fontsize=8)
A.mark(fig); fig.savefig(os.path.join(OUT, 'pyramidise-strip.png'), dpi=250, facecolor='white'); plt.close(fig)

# ---- (2) census chart ----
C = json.load(open(CEN)); ang = []; w = []
for r in C['rows']:
    if not r.get('well_defined'): continue
    for c in r['classes']: ang.append(c['apex_deg']); w.append(c['count'])
ang, w = np.array(ang), np.array(w)
fig, ax = plt.subplots(figsize=(8, 3.2))
ax.hist(ang, bins=np.arange(0, 181, 2.5), weights=w, color=A.VIOLET, edgecolor='white', lw=0.3)
for deg, lab in ((90, '90°'), (72, '72°'), (36, '36°'), (120, '120°'), (45, '45°')):
    ax.axvline(deg, color=A.GOLD, lw=0.8, ls='--'); ax.text(deg, ax.get_ylim()[1] * 0.95, lab, ha='center', fontsize=7, color='#8a6d00')
ax.set_xlabel('fin apex angle at the centre (degrees)'); ax.set_ylabel('number of fins'); ax.set_xlim(0, 125)
for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
ax.set_title(f'Fin apex angles over the census: {int(w.sum())} fins of {sum(1 for r in C["rows"] if r.get("well_defined"))} well-defined solids', fontsize=9.5)
fig.tight_layout(); A.mark(fig); fig.savefig(os.path.join(OUT, 'census-apex-angles.png'), dpi=250, facecolor='white')
print('written', OUT, int(w.sum()))
