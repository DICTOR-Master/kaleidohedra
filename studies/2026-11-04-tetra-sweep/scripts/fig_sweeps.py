#!/usr/bin/env python3
"""Figure 1 of paper #100: the three sweeps with their exact Dehn lines (Theorems 1.1, 1.2, Proposition 1.3).
Solids from their half-spaces; Dehn coefficients are the exact formulas, and each is checked here against the
hull at every station drawn (edge lengths x dihedral, reduced to beta or alpha)."""
import sys, numpy as np, itertools
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
sys.path.insert(0, 'scripts'); import figlib as F

r2 = 2**.5; beta = np.arccos(1/3**.5); alpha = np.arccos(1/3)
I3 = np.eye(3); S8 = np.array(list(itertools.product([-1, 1], repeat=3)), float)
v = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], float)

def co_oct(mu):   # C ∩ μC*
    A = np.vstack([I3, -I3, S8]); b = np.r_[np.ones(6), mu*np.ones(8)]; return F.hull_from_halfspaces(A, b)
def co_rd(mu):    # CO ∩ μRD
    pairs = [s*np.eye(3)[i] + t*np.eye(3)[j] for i, j in [(0, 1), (0, 2), (1, 2)] for s in (-1, 1) for t in (-1, 1)]
    A = np.vstack([I3, -I3, S8, pairs]); b = np.r_[np.ones(6), 2*np.ones(8), mu*np.ones(12)]; return F.hull_from_halfspaces(A, b)
def tet(mu):      # T ∩ μ(−T), T = {−v·x ≤ 1}, corners v_i, edge a = 2√2
    A = np.vstack([-v, v]); b = np.r_[np.ones(4), mu*np.ones(4)]; return F.hull_from_halfspaces(A, b)

def dehn_coeffs(P):
    """Σ L ⊗ θ split into multiples of beta and alpha (alpha = π − 2β); rational-π angles dropped."""
    fs = F.faces(P); E = {}
    for Q, n in fs:
        for i in range(len(Q)):
            k = tuple(sorted([tuple(np.round(Q[i], 8)), tuple(np.round(Q[(i+1) % len(Q)], 8))])); E.setdefault(k, []).append(n)
    cb = 0.0
    for (a, b), ns in E.items():
        L = np.linalg.norm(np.subtract(a, b)); th = np.pi - np.arccos(np.clip(ns[0] @ ns[1], -1, 1))
        # write th = p·π + q·β with q ∈ {−2,−1,0,1,2} and p rational with small denominator
        for q in (0, 1, -1, 2, -2):
            p = (th - q*beta)/np.pi
            if abs(p*12 - round(p*12)) < 1e-7: cb += q*L; break
        else: raise ValueError('angle not in Qπ + Zβ: %r' % th)
    return cb   # D = cb ⊗ β ; note α = π − 2β ≡ −2β

def D_A(mu): return np.where(mu <= 2, 24*r2*(3 - 2*mu), -24*r2*(3 - mu))
def D_B(mu): return np.where(mu <= 4/3, 0*mu, np.where(mu <= 1.5, 72*r2*(mu - 4/3), 24*r2*(5 - 3*mu)))
def D_C(mu): return 6*(mu - 2)          # per unit edge, ⊗ α ; t = (3 − μ)/4, 6a(1 − 4t) = 6a(μ − 2)

rows = [
    ('A', 'Cube–octahedron sweep   S(μ) = C ∩ μC*', co_oct, D_A, (1, 3), '⊗ β',
     [(1, 'octahedron', 'b'), (1.25, '', 'b'), (1.5, 'Kelvin\'s cell\nμ = 3/2', 'g'), (2, 'cuboctahedron', 'b'), (2.5, '', 'b'), (3, 'cube\nμ = 3', 'g')]),
    ('B', 'CO–RD sweep   CO ∩ μRD', co_rd, D_B, (1, 2), '⊗ β',
     [(1, 'rhombic\ndodecahedron', 'g'), (7/6, 'trimmed RD', 'v'), (4/3, 'μ = 4/3', 'v'), (1.5, '', 'b'), (5/3, 'B3 permutohedron\nμ = 5/3', 'v'), (2, 'cuboctahedron', 'b')]),
    ('C', 'Tetrahedron sweep   T ∩ μ(−T)', tet, D_C, (1, 3), '⊗ α  (per edge a)',
     [(1, 'octahedron', 'b'), (4/3, '', 'b'), (5/3, 'Archimedean\ntrunc. tetrahedron', 'b'), (2, 'μ = 2: cuts 1/4\n(β-tin tiler)', 'g'), (2.5, '', 'b'), (3, 'tetrahedron', 'b')]),
]
COL = {'g': F.GOLD, 'v': F.VIOLET, 'b': F.BLUE}

# exact-formula check against the hulls
for tag, title, fn, D, rng, unit, st in rows:
    for mu, _, _ in st:
        cb = dehn_coeffs(fn(mu))
        if tag == 'C': got = -cb/2 / (2*r2)          # cb ⊗ β = (−cb/2) ⊗ α ; per unit edge a = 2√2
        else: got = cb
        assert abs(got - float(D(np.array(mu)))) < 1e-5, (tag, mu, got, float(D(np.array(mu))))
print('Dehn formulas agree with the hulls at all stations', flush=True)

fig = plt.figure(figsize=(11, 12.4), dpi=170); fig.patch.set_facecolor('white')
R = F.view(24, 30); RC = F.look((0.22, -0.12, 1.0), up=(1, 1, 0))
H = 1/3
for r, (tag, title, fn, D, rng, unit, st) in enumerate(rows):
    y0 = 1 - (r + 1)*H
    axP = fig.add_axes([0.10, y0 + 0.13*H, 0.86, 0.25*H])
    x0, x1 = rng; span = x1 - x0
    xl = (x0 - 0.07*span, x1 + 0.07*span)
    axS = fig.add_axes([0.10, y0 + 0.40*H, 0.86, 0.52*H]); axS.axis('off')
    wi, hi = 11*0.86, 12.4*0.52*H            # strip size in inches
    upi = (xl[1] - xl[0])/wi                  # μ-units per inch, same in y
    axS.set_xlim(*xl); yr = hi*upi; axS.set_ylim(-0.50*yr, 0.50*yr)
    size = {'A': 0.042, 'B': 0.046, 'C': 0.036}[tag]*span   # solid scale in μ-units
    for mu, label, c in st:
        P = fn(mu)*size; P = P - P.mean(0)
        s = F.Solid(P, color=COL[c], lw=0.6, edge='#3a3326')
        F.draw(axS, [s], RC if tag == 'C' else R, offset=(mu, 0.08*yr))
        if label: axS.text(mu, -0.17*yr, label, ha='center', va='top', fontsize=8.2, color='#333', linespacing=1.15)
    axS.text(xl[0] - 0.05*span, 0.50*yr, f'{tag}   {title}', fontsize=11.5, weight='bold', color='#3d3220', va='top')
    # Dehn line
    mu = np.linspace(x0, x1, 2001); d = D(mu)
    axP.axhline(0, color='#999', lw=0.7)
    axP.plot(mu, d, color='#3d3220', lw=1.6)
    zero = np.abs(d) < 1e-9
    axP.fill_between(mu, 0, d, color=F.BLUE, alpha=0.10, lw=0)
    for m, _, c in st:
        dv = float(D(np.array(m)))
        axP.plot([m], [dv], 'o', ms=6.5, mfc=COL[c], mec='#3d3220', mew=0.8, zorder=5)
    if tag == 'B':
        axP.plot([1, 4/3], [0, 0], color=F.VIOLET, lw=5, solid_capstyle='round', alpha=0.55, zorder=3)
    axP.set_xlim(*xl)
    axP.set_xlabel('μ', fontsize=9, labelpad=1); axP.set_ylabel('D  ' + unit, fontsize=8.5)
    for sp in ('top', 'right'): axP.spines[sp].set_visible(False)
    axP.tick_params(labelsize=8)
    ticks = sorted({m for m, _, _ in st})
    lab = {1: '1', 7/6: '7/6', 1.25: '5/4', 4/3: '4/3', 1.5: '3/2', 5/3: '5/3', 2: '2', 2.5: '5/2', 3: '3'}
    axP.set_xticks(ticks); axP.set_xticklabels([lab.get(t, f'{t:g}') for t in ticks])
fig.text(0.98, 0.996, 'gold: Dehn zero and tiles alone   ·   violet: Dehn zero, fails the angle count   ·   blue: Dehn nonzero',
         fontsize=8.6, color='#444', va='top', ha='right')
F.mark(fig)
fig.savefig('figures/fig1-sweeps.png', facecolor='white'); print('OK figures/fig1-sweeps.png')
