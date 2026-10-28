# Figure of #69: the first 34 layers of the Fibonacci stacking (types c -> ch, h -> c), coloured by type, with their letters,
# and the shares of the three kinds of piece present (cc, ch, hc; never hh).
import os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
C_C, C_H, INK = '#2f6db0', '#a9862a', '#1a1a1a'
def fib(n):
    w = 'c'
    while len(w) < n: w = ''.join('ch' if x == 'c' else 'c' for x in w)
    return w[:n]
t = fib(34); s = [1]
for x in t[1:]: s.append(s[-1] if x == 'c' else -s[-1])
pos = [0]
for x in s[:-1]: pos.append((pos[-1] + x) % 3)
fig, ax = plt.subplots(figsize=(12, 2.9), dpi=200); ax.set_axis_off()
for k, (ty, p) in enumerate(zip(t, pos)):
    ax.add_patch(plt.Rectangle((k, 1), 0.9, 0.9, color=C_C if ty == 'c' else C_H, ec='white'))
    ax.text(k + 0.45, 1.45, 'ABC'[p], ha='center', va='center', color='white', fontsize=8, weight='bold')
    ax.text(k + 0.45, 0.75, ty, ha='center', va='center', color=INK, fontsize=7)
ax.text(0, 2.25, 'The Fibonacci stacking: layer types by c → ch, h → c (first 34 layers); hexagonal share → 1/φ² ≈ 0.382; hexagonal layers never touch',
        fontsize=10, color=INK)
ax.text(0, 0.15, 'pieces between neighbouring layers: cubic–cubic 1/φ³ ≈ 0.236,  cubic–hexagonal 1/φ² ≈ 0.382,  hexagonal–cubic 1/φ² ≈ 0.382,  hexagonal–hexagonal 0',
        fontsize=9, color=INK)
ax.set_xlim(-0.2, 34.2); ax.set_ylim(0, 2.5)
fig.text(0.99, 0.02, 'DICTO', color='#b8962e', fontsize=11, ha='right', family='serif', weight='bold')
out = os.path.expanduser('~/kres-tmp/fig69'); os.makedirs(out, exist_ok=True)
fig.savefig(os.path.join(out, 'fibonacci-stacking.png'), bbox_inches='tight', facecolor='white'); print('ok')
