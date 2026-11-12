"""fig_scan.py - figure for the hop 4D Vacuus scan (DICTO, study 2026-11-12): left, the 4D permutohedron scanned along a line through its
centre (number of distinct central slices N at each special height; the centre drops 150 -> 65); right, the hop's sweep: drop of N at
every special height INSIDE the solid, per level k. Reads ../data/hop-vacuus4d.json; writes ../figures/hop-vacuus4d-scan.png.
Checks the plotted numbers against the json (FINAL ok / FAIL)."""
import json, sys, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, '../data/hop-vacuus4d.json')))
pc = d['controls']['permutohedron']
fig, ax = plt.subplots(1, 2, figsize=(11, 4.2), dpi=150)
ts = [t for t, N in pc['inside_special']]; Ns = [N for t, N in pc['inside_special']]
ax[0].vlines(ts, Ns, pc['generic_N'], color='#7a3db8', lw=1.2)
ax[0].plot(ts, Ns, 'o', color='#7a3db8', ms=3)
ax[0].axhline(pc['generic_N'], color='0.6', lw=0.8)
ax[0].set_xlabel('position of the centre on the line'); ax[0].set_ylabel('distinct central slices N')
ax[0].set_title('4D permutohedron: 150 two-faces, N = 65 at the centre', fontsize=10)
ok = min(Ns) == 65 and pc['generic_N'] == 150
for L in [L for L in d['levels'] if 'skipped' not in L]:
    hs = L['inside_heights']
    x = [h['t_over_maxb'] for h in hs]; y = [h['drop'] / L['N_generic'] for h in hs]
    ax[1].plot(x, y, 'o', ms=4, label=f"k = {L['k']} (N = {L['N_generic']})")
    ok &= all(h['drop'] <= L['max_drop_inside'] for h in hs)
ax[1].axhline(85 / 150, color='#7a3db8', ls='--', lw=1); ax[1].text(0.02, 85 / 150 + 0.01, 'permutohedron centre: 85 / 150', color='#7a3db8', fontsize=8,
                                                                  transform=ax[1].get_yaxis_transform())
ax[1].set_xscale('symlog', linthresh=1); ax[1].set_ylim(0, 0.62)
ax[1].set_xlabel('height of the centre above the floor / max b'); ax[1].set_ylabel('share of slices merged (drop / N)')
ax[1].set_title("the hop's sweep: special heights inside the solid", fontsize=10); ax[1].legend(fontsize=7, ncol=2)
fig.text(0.995, 0.01, 'DICTO · dictospheres.com', ha='right', va='bottom', fontsize=8, color='0.35')
fig.tight_layout(rect=(0, 0.03, 1, 1))
out = os.path.join(here, '../figures/hop-vacuus4d-scan.png'); fig.savefig(out)
print('wrote', out)
print('FINAL ok' if ok else 'FINAL FAIL: plotted numbers disagree with the json')
