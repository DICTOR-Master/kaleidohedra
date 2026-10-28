# #74 figure: (a) loops vs shells on five stackings: closed non-backtracking walks per site (loops2.out) identical on all
# stackings, while the coordination shells (coordseq.out) differ; (b) kagome planes per Mn atom against h (a3b_counts.out).
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt, numpy as np, os, re
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9})
fig, (a, b) = plt.subplots(1, 2, figsize=(7.4, 3.1), dpi=200)
L, W = [], []
for line in open('loops2.out'):
    m = re.match(r'L=\s*(\d+): 3C (\d+)', line)
    if m: L.append(int(m.group(1))); W.append(int(m.group(2)))
a.axhline(0, color='#b8962e', lw=2.2, label='closed loops of length 6 to 34: 2H, 4H, 6H, 9R exactly equal to 3C')
sh = {'3C': [4, 12, 24, 42, 64, 92], '4H': [4, 12, 24.5, 43, 66.5, 96], '2H': [4, 12, 25, 44, 67, 96]}
for k, c in (('4H', '#7a7a7a'), ('2H', '#c0392b')):
    a.plot(range(1, 7), [100*(x - y)/y for x, y in zip(sh[k], sh['3C'])], 's--', color=c, lw=1, ms=4, label=f'atoms n bonds away, {k} against 3C')
a.set_xlabel('n (bonds away)'); a.set_ylabel('difference from cubic, %'); a.set_title('(a) Loops equal, shells differ', fontsize=9, loc='left')
a.set_ylim(-0.6, 5.6); a.legend(fontsize=6.3, frameon=False, loc='upper left')
H = {'3C\nMn$_3$Ir': 0, '6H': 1/3, '4H': 1/2, '9R': 2/3, '2H\nMn$_3$Sn': 1}
x = np.linspace(0, 1, 2); b.plot(x, 1 + 3*(1 - x), color='#b8962e', lw=1.6, label='1 + 3(1 − h)')
for k, h in H.items():
    b.plot(h, 1 + 3*(1 - h), 'o', color='#3a6ea5', ms=5.5, mec='white', mew=0.8)
    b.annotate(k, (h, 1 + 3*(1 - h)), textcoords='offset points', xytext=(6, 4) if h < 1 else (-30, 8), fontsize=7)
b.set_xlabel('hexagonality h'); b.set_ylabel('kagome planes through each Mn'); b.set_ylim(0.5, 4.6); b.set_xlim(-0.05, 1.12)
b.set_title('(b) Kagome magnets: from 3D to 2D kagome', fontsize=9, loc='left'); b.legend(fontsize=6.8, frameon=False, loc='upper right')
for ax in (a, b): ax.spines[['top', 'right']].set_visible(False); ax.grid(alpha=0.25, lw=0.5)
fig.tight_layout(); fig.savefig(os.path.expanduser('~/kres-tmp/magnets.png')); print('ok')
