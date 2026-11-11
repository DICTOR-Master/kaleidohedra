"""Chapter 3 figure: the weight d of the web of bonds as the spacing of four values. Four panels, one per stop (DICTO 1:2 at d = -1/3,
Kelvin at 0, golden bond at 1/tau^3, DICTO 2:1 at 1/3); each shows the four values of the cell (gaps g : m : g with d = (g - m)/(g + m))
on a line, drawn to scale with the middle gap fixed, and the stop's place on the d axis."""
import sys, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
tau = (1 + 5 ** .5) / 2
stops = [(-1/3, 'DICTO 1:2', 'd = −1/3', '1/2 : 1 : 1/2'), (0, 'Kelvin', 'd = 0', '1 : 1 : 1'),
         (1 / tau ** 3, 'golden bond', 'd = 1/τ³', 'τ : 1 : τ'), (1/3, 'DICTO 2:1', 'd = 1/3', '2 : 1 : 2')]
fig, axs = plt.subplots(2, 4, figsize=(12, 3.8), dpi=220, gridspec_kw={'height_ratios': [1, 1.2]})
for k, (dv, name, dl, gl) in enumerate(stops):
    a = axs[0, k]; a.plot([-1, 1], [0, 0], color='#444', lw=1); a.plot([dv], [0], 'o', color='#c9a227', ms=8)
    a.text(-1, -0.35, '−1', ha='center', fontsize=8); a.text(1, -0.35, '1', ha='center', fontsize=8); a.text(0, -0.35, '0', ha='center', fontsize=8, color='#888')
    a.set_title(f'{name}\n{dl}', fontsize=10); a.set_xlim(-1.1, 1.1); a.set_ylim(-0.6, 0.4); a.axis('off')
    x = (1 + dv) / (1 - dv); vals = [-(0.5 + x), -0.5, 0.5, 0.5 + x]
    b = axs[1, k]; b.plot([vals[0], vals[-1]], [0, 0], color='#bbb', lw=1)
    for v in vals: b.plot([v], [0], 'o', color='#222', ms=6)
    b.text(0, -0.5, f'gaps {gl}', ha='center', fontsize=9.5); b.set_xlim(-3, 3); b.set_ylim(-0.8, 0.4); b.axis('off')
fig.text(0.01, 0.52, 'the weight', fontsize=9, color='#555', rotation=90, va='center'); fig.text(0.01, 0.18, 'the values', fontsize=9, color='#555', rotation=90, va='center')
fig.text(0.99, 0.01, 'DICTO · dictospheres.com', ha='right', fontsize=6, color='#999')
fig.savefig(sys.argv[1], bbox_inches='tight'); print('FINAL ok' if os.path.getsize(sys.argv[1]) > 20000 else 'FINAL FAIL')
