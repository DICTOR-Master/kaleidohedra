# Star Cores results report (2026-10-30): one typeset page set for DICTO from the six runs' data. Usage: report.py <star-cores data> <old-methods data> <out html>
import json, sys, os, html
SC, OM, OUT = sys.argv[1:4]
L = lambda f: json.load(open(os.path.join(SC, f)))
sc = L('star-cores.json'); pol = {r['D']: r for r in L('polar-spikes.json')}; sl = {r['D']: r for r in L('sloping-bases.json')}
bc = {(r['D'], r['t']): r for r in L('star-build.json')}; bl = {(r['D'], r['t']): r for r in L('star-build-local.json')}
va = {(r['D'], r['t']): r for r in L('star-valley.json')}; om = {r['D']: r for r in json.load(open(os.path.join(OM, 'old-methods.json')))}
e = html.escape
G = {'star fills; core returns (period two)': 'A', 'star fills; core does not return': 'B', 'star inside halo, layer does not fill': 'C', 'star outside its halo': 'D'}
def steps(r):
    if not r or 'error' in r: return '–'
    return ' · '.join(f"{x['volume_over_last']:.3f}" + ('' if x.get('overlaps_new', 0) == 0 else '✗') for x in r['steps'])
def vsteps(r):
    if not r: return 'running'
    if 'error' in r: return '–'
    return ' · '.join(f"{x['volume_over_last']:.3f}" for x in r['steps'])
rows = []
for r in sorted(sc, key=lambda r: int(r['D'][1:]) if r['D'][1:].isdigit() else 999):
    g = G.get(r['verdict'], '–'); D = r['D']; p = pol.get(D); s = sl.get(D); o = om.get(D, {}).get('ops', {})
    polar = '✓ fills' if p and abs(p['phi']['layer_over_needed'] - 1) < 1e-6 and p['phi']['overlaps'] == 0 else ('–' if not p else '✗')
    slope = '–' if not s else ('✓ fills halo' if s['phi']['fills_hull'] and s['phi']['overlaps'] == 0 else ('closed, own skin' if s['phi']['overlaps'] == 0 else '✗'))
    dual = o.get('d', {}).get('match') or ''
    rows.append(f"<tr><td>{D}</td><td>{e(r['name'].replace('DICTO ', ''))}</td><td class=c>{g}</td><td class=c>{polar}</td><td class=c>{slope}</td><td>{steps(bc.get((D, 'phi')))}</td><td>{steps(bl.get((D, 'phi')))}</td><td>{vsteps(va.get((D, 'phi')))}</td><td>{e(dual.replace('DICTO ', ''))}</td></tr>")
open(OUT, 'w').write(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'report-head.html')).read().replace('<!--ROWS-->', '\n'.join(rows)))
print(len(rows))
