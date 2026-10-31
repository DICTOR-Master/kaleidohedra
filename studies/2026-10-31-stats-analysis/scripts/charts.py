# Three charts for the stats analysis of 31 October 2026 (data from ~/dicto-stats/history.json, exported to fig/data.json).
import json, sys, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.dates as md
from datetime import date
d = json.load(open(sys.argv[1])); OUT = sys.argv[2]; LOGO = plt.imread(sys.argv[3])
dt = lambda s: date.fromisoformat(s)
INK, MUTED, GRID = '#1d1d24', '#6b6b76', '#e3e3e8'
COL = {'dictospheres': '#b8962e', 'kaleidohedra': '#c8502a', 'polyhedraverse': '#2e8b3a', 'rhombiverse': '#2a6fb8'}
def style(ax, title):
    ax.set_title(title, loc='left', fontsize=11, color=INK); ax.grid(axis='y', color=GRID, lw=0.8); ax.set_axisbelow(True)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.spines['left'].set_color(GRID); ax.spines['bottom'].set_color(GRID); ax.tick_params(colors=MUTED, labelsize=8.5)
    ax.xaxis.set_major_formatter(md.DateFormatter('%d %b'))
def mark(fig): a = fig.add_axes([0.93, 0.02, 0.055, 0.055 * fig.get_figwidth() / fig.get_figheight()]); a.imshow(LOGO); a.axis('off')
fig, ax = plt.subplots(figsize=(7.2, 3.2)); x = [dt(a) for a, _ in d['zen']]; y = [b for _, b in d['zen']]
ax.plot(x, y, color='#2a6fb8', lw=2); ax.scatter(x[-1:], y[-1:], s=40, color='#2a6fb8', zorder=3)
ax.annotate(f'{y[-1]}', (x[-1], y[-1]), xytext=(-28, 6), textcoords='offset points', fontsize=9, color=INK)
style(ax, 'Zenodo: unique views of all DICTO records, running total'); mark(fig); fig.tight_layout(); fig.savefig(f'{OUT}/zenodo.png', dpi=220); plt.close(fig)
fig, ax = plt.subplots(figsize=(7.2, 3.2))
for s, pts in d['sites'].items():
    x = [dt(a) for a, _ in pts]; y = [b for _, b in pts]; ax.plot(x, y, color=COL[s], lw=2, label=s)
    ax.annotate(s, (x[-1], y[-1]), xytext=(4, 0), textcoords='offset points', fontsize=8, color=INK, va='center')
style(ax, 'Visitors per day on the sites'); ax.legend(frameon=False, fontsize=8, loc='upper left'); mark(fig); fig.tight_layout(); fig.savefig(f'{OUT}/sites.png', dpi=220); plt.close(fig)
fig, ax = plt.subplots(figsize=(7.2, 2.8)); x = [dt(a) for a, _ in d['tet']]; y = [b for _, b in d['tet']]
ax.bar(x, y, color='#8e5bd6', width=0.7)
style(ax, 'Tetrapods dropped per day (no drops recorded after 26 October)'); mark(fig); fig.tight_layout(); fig.savefig(f'{OUT}/tetrapods.png', dpi=220); plt.close(fig)
print('ok')
