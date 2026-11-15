# Paper #102 v5, Figure 3, from the raw outputs of this study. Usage: python3 fig102v5.py DATA_FULL_DIR OUT.png
# (a) the 18-cycle deficit 349236 - p18 at the lower atom of bilayer 0 for the 16 c/h patterns of bilayers -2..1;
# (b) every site of the 11 polytypes at length 18 (small dots) and their period average (large dots) against
#     the h-fraction f, on the line 349236 - 108 f.
# Checks first (exit 1 on any failure): every LOCALDATA line (2048 words x 2 atoms) obeys the local law at l = 18 and 20
# with the mirror rule for the upper atom; every period average at l = 18, 20 equals 3C - 108 f, 3C - 360 f.
import sys, re, os, glob, itertools
from fractions import Fraction as Fr
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
GOLD, VIOL, BLUE, GREY = '#b8962e', '#7b4fa0', '#3a6ea5', '#8a8070'
d, out = sys.argv[1], sys.argv[2]
def mark(fig): fig.text(0.992, 0.012, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=7.5, color=GREY)
C18 = {-2: 12, -1: 30, 0: 42, 1: 24}; C20 = {-2: 30, -1: 114, 0: 204, 1: 12}
def law(coef, base, h, u):   # h: dict bilayer -> 0/1; upper atom (u = 1): reflect j -> -j
    return base - sum(c * h[(-j if u else j)] for j, c in coef.items())
nchk = bad = 0
for f in sorted(glob.glob(os.path.join(d, 'local-*.txt'))):
    for line in open(f):
        if not line.startswith('LOCALDATA'): continue
        t = line.split(); u = int(t[6]); w = t[8]; cyc = list(map(int, t[10:18]))
        h = {j: (1 if w[j + 5] == 'h' else 0) for j in range(-5, 6)}
        nchk += 1
        if cyc[6] != law(C18, 349236, h, u) or cyc[7] != law(C20, 2362200, h, u) or cyc[:6] != [12, 24, 240, 1128, 8148, 50016]:
            bad += 1; print('MISMATCH', f, line[:80])
print(f'local law checked on {nchk} (word, atom) pairs, {bad} mismatches')
sites, avg = {}, {}
for f in glob.glob(os.path.join(d, 'named-*.txt')):
    txt = open(f).read()
    sec = txt.split('TABLE cycles through a site')[1].split('TABLE SP')[0]
    for m in re.finditer(r"\('([^']+)', (\d+), (\d+)\) \[([^\]]+)\]", sec):
        sites.setdefault(m.group(1), []).append(int(m.group(4).split(',')[6]))
    m = re.search(r'^\s+(\S+)\s+h-fraction (\S+)\s+12 24 (.*)$', txt, re.M)
    vals = [Fr(x) for x in m.group(3).split()]
    avg[m.group(1)] = (Fr(m.group(2)), vals[4], vals[5])
for n, (fh, a18, a20) in avg.items():
    nchk += 1
    if a18 != 349236 - 108 * fh or a20 != 2362200 - 360 * fh: bad += 1; print('AVERAGE MISMATCH', n)
    nchk += 1
    if Fr(sum(sites[n]), len(sites[n])) != a18: bad += 1; print('SITE MEAN MISMATCH', n)
print(f'{nchk} checks, {bad} failed');
if bad: sys.exit(1)

fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.3), dpi=220, gridspec_kw={'width_ratios': [1.35, 1]})
pats = list(itertools.product([0, 1], repeat=4))
pats.sort(key=lambda p: (sum(C18[j] * p[i] for i, j in enumerate([-2, -1, 0, 1])), p))
defs = [sum(C18[j] * p[i] for i, j in enumerate([-2, -1, 0, 1])) for p in pats]
cols = [VIOL if p[2] else GOLD for p in pats]
a.bar(range(16), defs, color=cols, width=0.72, zorder=3)
for i, v in enumerate(defs): a.text(i, v + 1.5, str(v), ha='center', va='bottom', fontsize=6.2)
a.set_xticks(range(16)); a.set_xticklabels([''.join('h' if x else 'c' for x in p) for p in pats], rotation=90, fontsize=6.8, family='DejaVu Sans Mono')
a.set_xlabel('c/h letters of bilayers −2, −1, 0, 1 (site: lower atom of bilayer 0)', fontsize=7.6)
a.set_ylabel('349236 − (18-cycles through the site)', fontsize=7.6)
a.set_ylim(0, 122); a.grid(axis='y', color='#eeeeee', zorder=0)
a.bar([0], [0], color=GOLD, label='own bilayer c'); a.bar([0], [0], color=VIOL, label='own bilayer h')
a.legend(fontsize=6.8, frameon=False, loc='upper left')
a.set_title('(a) The local law: 12, 30, 42, 24 per h bilayer', fontsize=9, loc='left')
for n, (fh, a18, a20) in sorted(avg.items(), key=lambda kv: kv[1][0]):
    b.scatter([float(fh)] * len(set(sites[n])), sorted(set(sites[n])), s=10, color=GREY, alpha=0.6, zorder=3)
    b.scatter([float(fh)], [float(a18)], s=34, color=BLUE, zorder=4)
b.plot([0, 1], [349236, 349128], color=BLUE, lw=0.9, zorder=2, label='349236 − 108 f')
b.scatter([], [], s=10, color=GREY, label='single sites'); b.scatter([], [], s=34, color=BLUE, label='period average')
for n, (fh, a18, _) in avg.items():
    if n in ('3C', '2H', '4H', '6H', '9R'):
        b.annotate(n, (float(fh), float(a18)), xytext=(5, 2), textcoords='offset points', fontsize=6.6, color=BLUE)
b.set_xlabel('fraction f of h bilayers', fontsize=7.6); b.set_xlim(-0.05, 1.08)
b.ticklabel_format(axis='y', useOffset=False, style='plain'); b.tick_params(axis='y', labelsize=6.8)
b.legend(fontsize=6.6, frameon=False, loc='upper right'); b.grid(color='#eeeeee', zorder=0)
b.set_title('(b) 11 polytypes, length 18', fontsize=9, loc='left')
for ax in (a, b): ax.spines[['top', 'right']].set_visible(False)
fig.suptitle('Self-avoiding polygons first see the stacking at length 18', fontsize=9, x=0.01, ha='left')
fig.tight_layout(); mark(fig); fig.savefig(out); print('wrote', out)
