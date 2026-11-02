# Collects data/mech/*.json and data/flow/*.json into data/summary.json + data/tables.txt and draws figs/fig1-3.png.
import json, glob, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from lattice import word_from_labels, SEQ_LABELS
os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('../figs', exist_ok=True)
BLUE, ORANGE, AQUA, INK, MUTED = '#2a78d6', '#eb6834', '#1baf7a', '#222222', '#777777'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.edgecolor': '#999999', 'axes.grid': True, 'grid.color': '#e6e6e6', 'grid.linewidth': 0.6})
J = lambda p: json.load(open(p)); key = lambda s: s.replace('/', '_').replace(' ', '-')

def hagg(labels):
    """Hagg symbols of the 11 gaps (+1 for A->B, B->C, C->A, else -1); returns their mean."""
    w = word_from_labels(labels); nxt = {'A': 'B', 'B': 'C', 'C': 'A'}
    s = [1 if nxt[a] == b else -1 for a, b in zip(w, w[1:])]; return float(np.mean(s))

S = {}; seqs = list(SEQ_LABELS)
for s in seqs:
    k = key(s); r = dict(labels=SEQ_LABELS[s], word=word_from_labels(SEQ_LABELS[s]), hagg_mean=hagg(SEQ_LABELS[s]))
    for j in ('pin', 'frame'):
        for v in ('links', 'stiff', 'full'): r[f'block_{j}_{v}'] = J(f'../data/mech/block_{k}_{j}_{v}.json')
    for v in ('links', 'full'): r[f'rigidity_{v}'] = J(f'../data/mech/rigidity_{k}_{v}.json')
    for v in ('links', 'stiff', 'full'):
        for m in ('compress', 'compress_free', 'shear13', 'shear23'):
            e = J(f'../data/mech/energy_{k}_{v}_{m}.json'); e.pop('path'); r[f'energy_{v}_{m}'] = e
    for rr in ('0.05', '0.1'): f = J(f'../data/flow/{k}_h0.02_r{rr}.json'); f.pop('hist'); r[f'flow_r{rr}'] = f
    S[s] = r
P = {}
for s in ('3C', '2H', '4H', '6H'):
    for j in ('pin', 'frame'):
        for v in ('links', 'stiff', 'full'): P[f'{s}_{j}_{v}'] = J(f'../data/mech/periodic_{s}_{j}_{v}.json')
json.dump(dict(blocks=S, periodic=P), open('../data/summary.json', 'w'), indent=1, default=float)

# ---------- tables ----------
L = []; p = L.append; m3 = lambda x: f'{1e3 * x:8.3f}'
p('Stiffness in units of 1e-3 E_s (rod modulus); rods r = 0.05 a; 12 sheets, 6 x 6 nodes per sheet, in-plane periodic.')
for j, v, txt in (('frame', 'links', 'rigid joints, links only'), ('pin', 'full', 'pin joints, links + in-sheet members (3C = octet truss)'),
                  ('frame', 'full', 'rigid joints, links + in-sheet members')):
    p(f'\nBlock ({txt}): rho = {S["3C"][f"block_{j}_{v}"]["rho"]:.4f}')
    p(f'{"sequence":24s} {"<Hagg>":>7s} {"C33 bond":>8s} {"E3 free":>8s} {"G13 bond":>8s} {"G13 free":>8s} {"G23 free":>8s} {"E1 in":>8s} {"E2 in":>8s} {"G12 in":>8s}')
    for s in seqs:
        b = S[s][f'block_{j}_{v}']
        p(f'{s:24s} {S[s]["hagg_mean"]:7.3f} ' + ' '.join(m3(b[q]) for q in ('C33_bonded', 'E3_free', 'G13_bonded', 'G13_free', 'G23_free', 'E1_inplane', 'E2_inplane', 'G12_inplane')))
p('\nPeriodic bulk (3D-periodic 6 x 6 x 12 cell), 1/S55 = free transverse shear, C14 = shear-stretch coupling, units 1e-3 E_s')
for j in ('pin', 'frame'):
    for v in ('links', 'full'):
        for s in ('3C', '2H', '4H', '6H'):
            d = P[f'{s}_{j}_{v}']; C = np.array(d['C']); e = d['eng']
            p(f'{s:3s} {j:5s} {v:5s} C33 {m3(C[2,2])} C44 {m3(C[3,3])} C14 {m3(C[0,3])} C11 {m3(C[0,0])} C66 {m3(C[5,5])} ' +
              (f'E3 {m3(e["E3"])} 1/S55 {m3(e["G13"])} E1 {m3(e["E1"])}' if e else 'singular (3 zero-energy macro strains)'))
p('\nPin-jointed rigidity (compatibility-matrix rank): mechanisms / self-stress states / zero-energy macro strains')
for s in seqs:
    for v in ('links', 'full'):
        R = S[s][f'rigidity_{v}']
        p(f'{s:24s} {v:5s} block: {R["block"]["mechanisms_w"]:4d} / {R["block"]["self_stress"]:4d} / {R["block"]["soft_macro_strains"]}' +
          (f'   3D-periodic: {R["periodic"]["mechanisms_w"]:4d} / {R["periodic"]["self_stress"]:4d} / {R["periodic"]["soft_macro_strains"]} (bars - 3N = {R["periodic"]["maxwell_bars_minus_3N"]})' if 'periodic' in R else ''))
p('\nEnergy proxy (pin, links + in-sheet members, bonded platens): first buckling strain/stress (1e-3 E_s), work to 5 % strain (1e-6 E_s)')
for s in seqs:
    row = []
    for m in ('compress', 'compress_free', 'shear13', 'shear23'):
        e = S[s][f'energy_full_{m}']; fb = e['first_buckling']
        row.append(f'{m}: {fb["strain"]:.4f}/{1e3*fb["stress"]:.4f}/{1e6*e["work_to_end"]:.3f}')
    p(f'{s:24s} ' + '  '.join(row))
p('\nAirflow proxy: straight line-of-sight open fraction along the stacking axis (exact, capsule rods), porosity, tortuosity (voxel h = 0.02 a)')
for s in seqs:
    a, b = S[s]['flow_r0.05'], S[s]['flow_r0.1']
    p(f'{s:24s} {S[s]["word"]}  r=0.05: open {a["open_fraction_z"]:.4f} porosity {a["porosity"]:.4f} tau mean {a["tau_mean"]:.4f} straight {a["frac_tau_1"]:.3f} | '
      f'r=0.1: open {b["open_fraction_z"]:.4f} porosity {b["porosity"]:.4f} tau mean {b["tau_mean"]:.4f}')
for s in ('3C', '2H'):
    c = J(f'../data/flow/{s}_h0.0125_r0.05.json'); p(f'  resolution check {s} h = 0.0125: voxel open columns {c["voxel_open_columns"]:.4f}, tau mean {c["tau_mean"]:.4f}')
open('../data/tables.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))

# ---------- fig 1: line of sight ----------
fig, ax = plt.subplots(1, 4, figsize=(7.2, 2.3), gridspec_kw=dict(width_ratios=[1, 1, 1, 2.2]))
for a, s, c in zip(ax[:3], ('3C', '4H', '2H'), (BLUE, AQUA, ORANGE)):
    m = np.load(f'../data/flow/{s}_h0.02_r0.05_openmask.npy'); img = np.tile(m.T, (2, 3))
    a.imshow(img, origin='lower', cmap=matplotlib.colors.ListedColormap(['#d9d9d9', c]), extent=(0, 3, 0, 2 * np.sqrt(3)))
    a.set_title(f'{s}: {S[s]["flow_r0.05"]["open_fraction_z"]*100:.1f} % open', fontsize=8); a.set_xlabel('colour = see-through', fontsize=6.5, color=MUTED); a.set_xticks([]); a.set_yticks([]); a.grid(False)
rr = [0.03, 0.05, 0.08, 0.1, 0.12, 0.15, 0.2]
for s, c in (('2H', ORANGE), ('4H', AQUA), ('3C', BLUE)):
    y = [100 * S[s]['flow_r0.05']['open_fraction_vs_r'][str(x)] for x in rr]
    ax[3].plot(rr, y, '-o', color=c, lw=2, ms=4)
    ax[3].annotate({'2H': '2H', '4H': '4H', '3C': '3C, 6H, Fibonacci, graded'}[s], (rr[1] if s != '3C' else rr[2], y[1] if s != '3C' else y[2]), textcoords='offset points',
                   xytext={'2H': (8, 4), '4H': (8, 2), '3C': (0, 5)}[s], color=INK, fontsize=7)
ax[3].set_xlabel('rod radius r / a'); ax[3].set_ylabel('straight see-through area (%)'); ax[3].set_ylim(0, 60)
fig.tight_layout(); fig.savefig('../figs/fig1-line-of-sight.png', dpi=220); plt.close(fig)

# ---------- fig 2: sheet-stiffness sweep ----------
fs = ['0.0001', '0.001', '0.003', '0.01', '0.03', '0.1', '0.3', '1', '3', '10', '100']
fig, ax = plt.subplots(figsize=(3.5, 2.5))
for j, c, lab in (('frame', BLUE, 'rigid joints'), ('pin', ORANGE, 'pin joints')):
    y = [J(f'../data/mech/periodic_3C_{j}_sheet{f}.json')['eng']['G13'] / J(f'../data/mech/periodic_2H_{j}_sheet{f}.json')['eng']['G13'] for f in fs]
    ax.semilogx([float(f) for f in fs], y, '-o', color=c, lw=2, ms=4, label=lab)
ax.set_xlabel('in-sheet member stiffness / link stiffness'); ax.set_ylabel('free transverse shear  3C / 2H')
ax.set_ylim(0, 1.05); ax.legend(frameon=False, loc='lower right'); fig.tight_layout(); fig.savefig('../figs/fig2-sheet-sweep.png', dpi=220); plt.close(fig)

# ---------- fig 3: free transverse shear vs net Hagg sum ----------
fig, ax = plt.subplots(figsize=(3.6, 2.6)); pts = []
for f in sorted(glob.glob('../data/mech/blockL_*_frame_links.json')):
    d = J(f); pts.append((abs(hagg(d['labels'])), 1e3 * d['G13_free'], d['labels']))
for s in seqs:
    b = S[s]['block_frame_links']; pts.append((abs(S[s]['hagg_mean']), 1e3 * b['G13_free'], s))
x = np.array([q[0] for q in pts]); y = np.array([q[1] for q in pts])
ax.plot(x, y, 'o', color=BLUE, ms=5, mec='white', mew=0.8)
for q in pts:
    lab = {'3C': '3C', '2H': '2H, 4H, 6H, Fibonacci', 'Graded c-top/h-bottom': 'graded (both ways)'}.get(q[2])
    if lab: ax.annotate(lab, (q[0], q[1]), textcoords='offset points', xytext=(-8, 7) if q[2] == '3C' else (6, -4), fontsize=7, color=INK)
ax.set_xlabel('|mean Hägg symbol| (net c-twist of the stack)'); ax.set_ylabel('free transverse shear (1e-3 E_s)')
fig.tight_layout(); fig.savefig('../figs/fig3-hagg.png', dpi=220); plt.close(fig)
print('figs written')
