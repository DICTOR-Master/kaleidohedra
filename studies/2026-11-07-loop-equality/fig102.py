# Paper #102 figures. Usage: python3 fig102.py data-loop-checks.txt OUTDIR
# fig1-proof.png: (a) the two step triangles D and -D between close-packed positions; (b) a closed walk on the level line.
# fig2-every-site.png: every tested site of the 42 stackings: shells n bonds away differ from diamond, loops do not.
import sys, re, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
GOLD, VIOL, BLUE, GREY = '#b8962e', '#7b4fa0', '#3a6ea5', '#8a8070'
data, outdir = sys.argv[1], sys.argv[2]
def mark(fig): fig.text(0.992, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=7.5, color=GREY)

# ---------- Figure 1 ----------
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.5), dpi=220, gridspec_kw={'width_ratios': [1, 1.25]})
a1 = np.array([1, 0.]); a2 = np.array([.5, 3 ** .5 / 2]); t = (a1 + a2) / 3
pts = {0: [], 1: [], 2: []}
for i in range(-3, 4):
    for j in range(-3, 4):
        for s in range(3):
            p = i * a1 + j * a2 + s * t
            if abs(p[0]) < 1.45 and abs(p[1]) < 1.15: pts[s].append(p)
for s, (c, lab) in enumerate(((GREY, 'A'), (GOLD, 'B'), (VIOL, 'C'))):
    P = np.array(pts[s]); a.scatter(P[:, 0], P[:, 1], s=22 if s == 0 else 30, color=c, zorder=3, label=f'{lab} positions')
D = [t, t - a1, t - a2]
for d in D:
    a.annotate('', xy=d, xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=GOLD, lw=1.6, shrinkA=3, shrinkB=4))
    a.annotate('', xy=-d, xytext=(0, 0), arrowprops=dict(arrowstyle='-|>', color=VIOL, lw=1.6, shrinkA=3, shrinkB=4))
a.scatter([0], [0], s=60, color='black', zorder=4)
a.text(0.05, -0.16, 'A', fontsize=8, ha='left', va='top')
a.text(0.98, 0.78, 'D: A to B\n(step +1)', color=GOLD, fontsize=7.4, ha='left')
a.text(-0.62, -0.62, '−D: A to C\n(step −1)', color=VIOL, fontsize=7.4, ha='right', va='top')
a.set_aspect('equal'); a.set_xlim(-1.45, 1.75); a.set_ylim(-1.15, 1.15); a.axis('off')
a.set_title('(a) The stacking picks D or its mirror −D', fontsize=9, loc='left')
# (b) level line: levels 0..7; gaps alternately bond inside a bilayer (thin) and bond layer between bilayers (gold band)
seq = [0, 1, 2, 3, 2, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]
for lev in range(0, 6):
    if lev % 2 == 1:
        b.axhspan(lev + 0.08, lev + 0.92, color=GOLD, alpha=0.18, lw=0)
        b.text(len(seq) - 0.4, lev + 0.5, f'bond layer {lev // 2}: g up, g* down', fontsize=6.6, va='center', ha='left', color='#6b5418')
    else:
        b.text(len(seq) - 0.4, lev + 0.5, 'bond inside a bilayer: 1', fontsize=6.6, va='center', ha='left', color=GREY)
    b.axhline(lev, color='#cccccc', lw=0.6)
b.plot(range(len(seq)), seq, '-o', color=BLUE, ms=3.2, lw=1.4)
for s in range(len(seq) - 1):
    lo = min(seq[s], seq[s + 1])
    if lo % 2 == 1:
        b.text(s + 0.5, lo + 0.5, 'g' if seq[s + 1] > seq[s] else 'g*', fontsize=7.2, ha='center', va='center',
               color='#6b5418', bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none', alpha=0.85))
b.set_yticks(range(6)); b.set_yticklabels(['0 lower', '0 upper', '1 lower', '1 upper', '2 lower', '2 upper'], fontsize=6.8)
b.set_xlabel('step of the walk'); b.set_xlim(-0.5, len(seq) + 4.6); b.set_ylim(-0.4, 5.6)
b.spines[['top', 'right']].set_visible(False)
b.set_title('(b) A closed walk crosses each bond layer\nas often up as down: |g|² per pair', fontsize=9, loc='left')
fig.tight_layout(); mark(fig); fig.savefig(os.path.join(outdir, 'fig1-proof.png')); plt.close(fig)

# ---------- Figure 2 ----------
shells, loops, closed, names = [], [], [], []
for line in open(data):
    m = re.match(r'\s+shells n=3\.\.8 per site: (.*)', line)
    if m: shells.append([[int(x) for x in s.split(',')] for s in m.group(1).split()])
    m = re.match(r'\s+per site NB L=(\d+) / closed L=(\d+): (.*)', line)
    if m:
        LN, LW = int(m.group(1)), int(m.group(2))
        loops += [int(x.split('/')[0]) for x in m.group(3).split()]; closed += [int(x.split('/')[1]) for x in m.group(3).split()]
dia = [24, 42, 64, 92, 124, 162]   # diamond (A008253), n = 3..8
allsites = [s for st in shells for s in st]
fig, (ax, bx) = plt.subplots(1, 2, figsize=(7.4, 3.2), dpi=220, sharey=True, gridspec_kw={'width_ratios': [1, 1.6]})
for k, n in enumerate(range(3, 9)):
    vals = np.array([100 * (s[k] - dia[k]) / dia[k] for s in allsites])
    u, cnt = np.unique(np.round(vals, 6), return_counts=True)
    ax.scatter(np.full(len(u), n), u, s=8 + 70 * cnt / cnt.max(), color=VIOL, alpha=0.75, zorder=3)
ax.set_xlabel('n (bonds away)'); ax.set_ylabel('difference from diamond, %'); ax.set_xticks(range(3, 9))
ax.set_title('(a) Atoms n bonds away', fontsize=9, loc='left')
ls = list(range(6, LN + 1, 2)); cw = list(range(2, LW + 1, 2))
bx.plot(cw, [0] * len(cw), 's', color=BLUE, ms=3.0, zorder=5, label=f'closed walks, length 2 to {LW}')
bx.plot(ls, [0] * len(ls), 'o', color=GOLD, ms=8, mec='white', mew=0.6, zorder=4, label=f'closed loops (non-backtracking), length 6 to {LN}')
bx.axhline(0, color=GREY, lw=0.6)
bx.set_xlabel('length'); bx.set_xticks(range(2, LW + 1, 4))
bx.set_title('(b) Walks and loops at every site: difference 0', fontsize=9, loc='left')
bx.legend(fontsize=7, frameon=False, loc='upper right')
for z in (ax, bx): z.spines[['top', 'right']].set_visible(False); z.grid(alpha=0.25, lw=0.5)
fig.suptitle(f'{len(allsites)} sites on {len(shells)} stackings: the shells see the stacking, the walks and loops do not', fontsize=9, x=0.01, ha='left')
fig.tight_layout(); mark(fig); fig.savefig(os.path.join(outdir, 'fig2-every-site.png')); plt.close(fig)
assert len(set(loops)) == 1 and len(set(closed)) == 1
print('sites', len(allsites), 'stackings', len(shells), 'loops L=%d' % LN, loops[0], 'closed L=%d' % LW, closed[0],
      'shell spread %:', [round(100 * (max(s[k] for s in allsites) - min(s[k] for s in allsites)) / dia[k], 2) for k in range(6)])
print('FINAL ok' if all(os.path.getsize(os.path.join(outdir, f)) > 20000 for f in ('fig1-proof.png', 'fig2-every-site.png')) else 'FINAL FAIL (figure missing or empty)')
