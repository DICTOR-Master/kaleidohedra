#!/usr/bin/env python3
"""Read data/census-*.json and write data/summary.json and data/tables.md (light: runs anywhere in seconds)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DATA = os.path.join(HERE, '..', 'data')
GROUPS = ['A3', 'B3', 'H3', 'A4', 'B4', 'D4', 'F4', 'H4']
LAB = {'A3': [3, 3], 'B3': [3, 4], 'H3': [5, 3], 'A4': [3, 3, 3], 'B4': [3, 3, 4], 'F4': [3, 4, 3], 'H4': [5, 3, 3]}

def dynkin(G, pat, t='t'):
    s = ['x' if c == '1' else ('o' if c == '0' else t) for c in pat]
    if G == 'D4': return f'{s[0]}3{s[1]}3{s[2]} *b3{s[3]}'
    out = s[0]
    for m, c in zip(LAB[G], s[1:]): out += str(m) + c
    return out

NAMES = {('A3', '111'): 'truncated octahedron (A3 omnitruncated)', ('A3', '101'): 'cuboctahedron', ('A3', '010'): 'octahedron',
         ('A3', '110'): 'truncated tetrahedron', ('A3', '100'): 'tetrahedron',
         ('B3', '001'): 'cube', ('B3', '100'): 'octahedron', ('B3', '010'): 'cuboctahedron', ('B3', '011'): 'truncated cube',
         ('B3', '110'): 'truncated octahedron (Kelvin)', ('B3', '101'): 'rhombicuboctahedron', ('B3', '111'): 'great rhombicuboctahedron (B3 permutohedron)',
         ('H3', '100'): 'dodecahedron or icosahedron', ('H3', '001'): 'icosahedron or dodecahedron', ('H3', '010'): 'icosidodecahedron',
         ('H3', '110'): 'truncated (first node)', ('H3', '011'): 'truncated (last node)', ('H3', '101'): 'rhombicosidodecahedron',
         ('H3', '111'): 'great rhombicosidodecahedron (H3 permutohedron)'}

def main():
    summ = {}; lines = []
    tot_f = tot_raw = tot_inv = 0
    law_rows = []; cross_rows = []; coinc_rows = []
    for G in GROUPS:
        fn = os.path.join(DATA, f'census-{G}.json')
        if not os.path.exists(fn): print('missing', G); continue
        d = json.load(open(fn)); fams = d['families']
        tot_f += len(fams); tot_raw += sum(f['raw_patterns'] for f in fams)
        ninv = sum(1 for f in fams if f['involution']); tot_inv += ninv
        nsym = sum(1 for f in fams if f['pointwise_symmetric'])
        ntz = sum(len(v) for f in fams for v in f['tones'].values() if not isinstance(v, str))
        nm = sum(len(f.get('mahler_critical', [])) for f in fams)
        niq = sum(len(f['iq_critical']) for f in fams if isinstance(f.get('iq_critical'), list))
        iqerr = [f['pattern'] for f in fams if isinstance(f.get('iq_critical'), str) and f['iq_critical'].startswith('error')]
        dz = [(f['pattern'], f['dehn']['zero_at']) for f in fams if f.get('dehn') and f['dehn']['zero_at'] != 'none']
        summ[G] = {'families': len(fams), 'raw_patterns': sum(f['raw_patterns'] for f in fams), 'with_involution': ninv,
                   'pointwise_symmetric': nsym, 'tone_zeros': ntz, 'mahler_critical': nm, 'iq_critical': niq, 'iq_errors': iqerr,
                   'dehn_zeros': dz, 'checks': d['checks'], 'fails': d['fails'], 'seconds': d['seconds'], 'kmax': d['kmax']}
        for f in fams:
            pat = f['pattern']; uni = pat.replace('t', '1')
            if f['involution']:
                fp = f['fixed_point']
                killed = [k.replace('tone', '') for k, v in fp.items() if isinstance(v, dict) and v.get('zero_at_fixed_point')]
                tmax = [k.replace('tone', '') for k, v in fp.items() if isinstance(v, dict) and v.get('second_derivative_sign') == -1]
                tmin = [k.replace('tone', '') for k, v in fp.items() if isinstance(v, dict) and v.get('second_derivative_sign') == 1]
                ms = fp.get('mahler_second_derivative_sign')
                law_rows.append((G, dynkin(G, pat), dynkin(G, uni, 'x'), NAMES.get((G, uni), ''), 't -> 1/t (' + f['involution'].split('automorphism ')[1] + ')',
                                 ','.join(killed) or '-', ','.join(tmax) or '-', ','.join(tmin) or '-', {1: 'min', -1: 'max', 0: 'flat'}.get(ms, '?')))
            for k, v in f['tones'].items():
                if isinstance(v, str): continue
                for r in v: cross_rows.append((G, dynkin(G, pat), f'T{k}', r['value'][:16], r['deg']))
            for r in f.get('mahler_critical', []): cross_rows.append((G, dynkin(G, pat), 'Mahler crit', r['value'][:16], r['deg']))
            if isinstance(f.get('iq_critical'), list):
                for r in f['iq_critical']: cross_rows.append((G, dynkin(G, pat), 'IQ crit', r['value'][:16], r['deg']))
            for c in f['coincidences']:
                if 'same point' in c['what']: coinc_rows.append((G, dynkin(G, pat), c['what'], c['value'][:16], c['minpoly']))
    summ['_total'] = {'families': tot_f, 'raw_patterns': tot_raw, 'with_involution': tot_inv}
    json.dump({'summary': summ, 'law_rows': law_rows, 'coincidences': coinc_rows, 'n_crossings': len(cross_rows)}, open(os.path.join(DATA, 'summary.json'), 'w'), indent=1, default=str)
    L = ['| group | families (raw patterns) | with involution | whole family symmetric | tone zeros | Mahler crit. | IQ crit. | Dehn zeros (3D) | checks / FAIL | s |', '|---|---|---|---|---|---|---|---|---|---|']
    for G in GROUPS:
        if G not in summ: continue
        s = summ[G]
        L.append(f"| {G} | {s['families']} ({s['raw_patterns']}) | {s['with_involution']} | {s['pointwise_symmetric']} | {s['tone_zeros']} | {s['mahler_critical']} | {s['iq_critical']}{' (errors ' + ','.join(s['iq_errors']) + ')' if s['iq_errors'] else ''} | {', '.join(f'{a}: {b}' for a, b in s['dehn_zeros']) if G in ('A3', 'B3', 'H3') else 'n/c'} | {s['checks']} / {len(s['fails'])} | {s['seconds']} |")
    L += ['', '| group | family | fixed member | name | involution | tones killed at the fixed point | tones max there | tones min there | Mahler |', '|---|---|---|---|---|---|---|---|---|']
    for r in law_rows: L.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    L += ['', '| group | family | coincidence | value | minimal polynomial |', '|---|---|---|---|---|']
    for r in coinc_rows: L.append('| ' + ' | '.join(str(x) for x in r) + ' |')
    open(os.path.join(DATA, 'tables.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L[:12])); print(f'{len(law_rows)} fixed-point rows, {len(coinc_rows)} coincidences, {len(cross_rows)} crossings')

if __name__ == '__main__': main()
