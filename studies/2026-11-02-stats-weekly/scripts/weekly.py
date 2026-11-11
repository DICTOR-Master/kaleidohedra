# DICTO stats, recent days and weeks compared (DICTO 2026-11-02). Reads ~/dicto-stats/history.json (copied), writes a 2-page PDF.
# Usage (compute-host): python3 weekly.py history.json dicto-logo.png out.pdf
import sys, json, datetime as dt
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
H = json.load(open(sys.argv[1])); LOGO = plt.imread(sys.argv[2]); OUT = sys.argv[3]
D = lambda s: dt.date.fromisoformat(s)
# Zenodo: snapshots are running totals per record; daily gain = rise of each record since its previous snapshot
zd = H['zenodo_daily']; days = sorted(zd); prev = {}; zv, zdl = {}, {}
for d in days:
    v = dl = 0
    for r, x in zd[d].items():
        p = prev.get(r, {'unique_views': 0, 'unique_downloads': 0})
        v += max(0, x['unique_views'] - p['unique_views']); dl += max(0, x['unique_downloads'] - p['unique_downloads']); prev[r] = x
    zv[d], zdl[d] = v, dl
first = days[0]; zv.pop(first); zdl.pop(first)       # first snapshot holds all history, not one day
site = {}
for proj, per in H['vercel'].items():
    for d, paths in per.items():
        site.setdefault(d, 0); site[d] += sum(p.get('visitors', 0) for p in paths.values())
tet = {d: sum(v.values()) for d, v in H['tetrapods']['days'].items()}
clones = {}
for repo, r in H['github'].items():
    for d, x in r['days'].items(): clones[d] = clones.get(d, 0) + x.get('clones', 0)
today = max(site); end = D(today) - dt.timedelta(days=1)   # last full day
def wk(series, k):
    a = end - dt.timedelta(days=7 * k + 6); b = end - dt.timedelta(days=7 * k)
    vals = [series.get(str(a + dt.timedelta(days=i)), 0) for i in range(7)]
    return sum(vals), (a, b)
rows = []
for name, s in [('Zenodo: new unique readers (views)', zv), ('Zenodo: new unique downloads', zdl), ('Website visitors (all sites)', site),
                ('Tetrapods dropped', tet), ('GitHub clones (mostly bots/CI)', clones)]:
    w0, (a0, b0) = wk(s, 0); w1, (a1, b1) = wk(s, 1); w2, _ = wk(s, 2)
    ch = '' if w1 == 0 else f'{(w0 - w1) / w1 * 100:+.0f}%'
    rows.append((name, w2, w1, w0, ch))
with PdfPages(OUT) as pdf:
    fig = plt.figure(figsize=(8.27, 11.69)); fig.text(0.07, 0.95, 'DICTO stats: the last three weeks compared', fontsize=18, weight='bold')
    fig.text(0.07, 0.925, f'Weeks ending {end - dt.timedelta(days=14)}, {end - dt.timedelta(days=7)} and {end} (last full day). Data: Zenodo, Vercel, GitHub, Supabase.', fontsize=9, color='#555')
    ax = fig.add_axes([0.07, 0.70, 0.86, 0.2]); ax.axis('off')
    t = ax.table(cellText=[[r[0], r[1], r[2], r[3], r[4]] for r in rows], colLabels=['', '2 weeks ago', 'last week', 'this week', 'change'], loc='center', cellLoc='center', colLoc='center', colWidths=[0.42, 0.14, 0.14, 0.14, 0.12])
    t.auto_set_font_size(False); t.set_fontsize(9); t.scale(1, 1.6)
    for (r, c), cell in t.get_celld().items():
        if c == 0: cell.set_text_props(ha='left'); cell._loc = 'left'
        if r == 0: cell.set_text_props(weight='bold')
    def plot(axp, s, title, col):
        ks = sorted(k for k in s if D(k) <= end and D(k) > end - dt.timedelta(days=28)); axp.bar([D(k) for k in ks], [s[k] for k in ks], color=col, width=0.8)
        axp.set_title(title, fontsize=10, loc='left'); axp.tick_params(labelsize=7); axp.spines[['top', 'right']].set_visible(False)
        for lbl in axp.get_xticklabels(): lbl.set_rotation(45)
    plot(fig.add_axes([0.08, 0.40, 0.38, 0.22]), zv, 'Zenodo new unique readers per day', '#3f7fc4')
    plot(fig.add_axes([0.56, 0.40, 0.38, 0.22]), zdl, 'Zenodo new unique downloads per day', '#7f6fc4')
    plot(fig.add_axes([0.08, 0.10, 0.38, 0.22]), site, 'Website visitors per day', '#c9a227')
    plot(fig.add_axes([0.56, 0.10, 0.38, 0.22]), tet, 'Tetrapods dropped per day', '#2e8b57')
    la = fig.add_axes([0.86, 0.015, 0.08, 0.06]); la.imshow(LOGO); la.axis('off')
    pdf.savefig(fig); plt.close(fig)
print(json.dumps(rows, default=str))
