# The cards of the Star Cores book: one page per shape, the picture from cards.py (study 2026-11-01-star-cores-book) and the facts of the
# studies behind Chapters 2 to 5, each row citing the chapter (paper) that states or measures it. Used by assemble.py.
import json, os, re, html
CHAP = {78: 1, 79: 2, 81: 3, 80: 4, 85: 5}
SIDES = {3: 'triangles', 4: 'quadrilaterals', 5: 'pentagons', 6: 'hexagons', 7: 'heptagons', 8: 'octagons', 9: 'nonagons', 10: 'decagons', 11: 'hendecagons', 12: 'dodecagons', 15: 'pentadecagons'}
ECC = ['D77', 'D80', 'D82', 'D6', 'D71', 'D81', 'D86']                     # the seven pieces of #85, in its order
CORE_LIN = {'1/5 + (4/45)*sqrt(5)': '(5 + 2√5)/15', '1/9': '1/3', '1/81': '1/9', '207/3362 + (-85/3362)*sqrt(5)': '(17 − 5√5)/82', '1/100': '1/10'}
GAINS = {'D40': '35 − 15√5 = 10/φ⁴ ≈ 1.458980', 'D41': '35 − 15√5 = 10/φ⁴ ≈ 1.458980', 'D31': '35 − 15√5 = 10/φ⁴ ≈ 1.458980',
         'D89': '293 − 652√5/5 ≈ 1.416736 (norm 41·101/5)', 'D30': '939725/9 − 140084√5/3 ≈ 1.440036 (norm 5·2081·2341/3⁴)',
         'D71': 'a cubic number of ℚ(∛2) ≈ 3.855518 (entering after one step)'}
SLOPE6 = {'D77': ('18 / 18', '0 / 12', '×1.3346', '6.154', '1.971'), 'D80': ('24 / 24', '0 / 3', '×1.4356', '5.383', '2.575'),
          'D82': ('12 / 24', '0 / 0', '×1.3859', '5.350', '1.859'), 'D6': ('12 / 12', '1 / 6', '×1.4838 (valley rule ×1.4701)', '5.128', '2.793'),
          'D71': ('12 / 24', '0 / 0', '×1.2600', '4.934', '1.922'), 'D81': ('12 / 12', '0 / 9', '×1.3720', '4.743', '2.519')}
def ex(s):
    """exact strings of the data set as typeset: 85/2 + (-15/2)*sqrt(5) -> 85/2 − (15/2)√5"""
    s = str(s).replace(' ', '')
    s = re.sub(r'\*\*\(1/3\)', '^(1/3)', s)
    s = re.sub(r'\(-([0-9/]+)\)\*sqrt\((\d+)\)', r'-(\1)√\2', s); s = re.sub(r'\(([0-9/]+)\)\*sqrt\((\d+)\)', r'(\1)√\2', s)
    s = re.sub(r'(\d)\*sqrt\((\d+)\)', r'\1√\2', s); s = re.sub(r'sqrt\((\d+)\)', r'√\1', s); s = s.replace('2^(1/3)', '∛2').replace('*', '·')
    s = s.replace('+-', ' − ').replace('+', ' + ').replace('-', ' − ').strip()
    s = re.sub(r'\((\d+)\)√', r'\1√', s)
    return s[2:].join(['−', '']) if s.startswith('− ') else s
def field(f):
    return {'Q(sqrt(5))': 'ℚ(√5)', 'Q': 'ℚ', 'Q(sqrt(2))': 'ℚ(√2)', 'Q(sqrt(3))': 'ℚ(√3)', 'Q(2**(1/3))': 'ℚ(∛2)'}.get(f, 'a cubic field' if f == 'Q(t)' else f)
def faces_txt(fb):
    return ', '.join(f'{n} {SIDES.get(int(k), str(k) + "-gons")}' for k, n in sorted(fb.items(), key=lambda kv: int(kv[0])))
def short(name): return re.sub(r'^DICTO ', '', name)
def load(p): return json.load(open(p, encoding='utf8'))
def table3(P):
    s = open(os.path.join(P, 'star-cores-a', 'paper.html'), encoding='utf8').read(); s = s[s.index('<h2>8. The cards'):s.index('<h2>9.')]
    out = {}
    for row in re.findall(r'<tr>(.*?)</tr>', s, re.S)[1:]:
        c = [html.unescape(re.sub('<[^>]+>', '', x)).strip() for x in re.findall(r'<td[^>]*>(.*?)</td>', row, re.S)]
        out[c[0]] = dict(zip(['D', 'shape', 'sym', 'V', 'F', 'group', 'halo', 'pieces', 'core', 'chain', 'vphi', 'v2'], c))
    return out
GROUP = {'star fills; core returns (period two)': 'A', 'star fills; core does not return': 'B', 'star inside halo, layer does not fill': 'C', 'star outside its halo': 'D'}
GROUPTXT = {'A': 'the star fills its halo and the core comes back to the shape', 'B': 'the star fills its halo; the core does not come back to the shape itself',
            'C': 'the star lies inside its halo, but corner and edge pieces do not fill the layer', 'D': 'the star sticks out of its halo'}
NEWDELTA = {'D106': 120.0, 'D107': 125.264, 'D108': 160.151, 'D109': 161.095}   # dihedral_new4.py (book study)
def valley_growth(rec):
    st = rec['steps']
    if len(st) < 3: return None
    g = st[1]['volume_over_last'] * st[2]['volume_over_last']
    return 'freezes' if st[2]['volume_over_last'] < 1.001 else f'×{g:.2f}'
def build(ST, HERE):
    P = os.path.dirname(HERE)
    a = os.path.join(ST, '2026-10-30-star-cores', 'data'); x = os.path.join(ST, '2026-10-30-star-cores-exact', 'data')
    d = os.path.join(ST, '2026-11-01-star-cores-d', 'data'); b = os.path.join(ST, '2026-11-01-star-cores-book', 'data')
    meta = load(os.path.join(b, 'meta-v7.json'))
    sc = load(os.path.join(a, 'star-cores.json')) + load(os.path.join(b, 'star-cores-new4.json'))
    pol = {r['D']: r for r in load(os.path.join(a, 'polar-spikes.json'))}
    # D106-D109: halo and layer volumes from polar_quick.py; the overlap counts from polar_spikes.py (polar-new4.log) where it has finished
    ov = {l.split()[0]: (None if l.split('| phi ')[1].split()[1] == 'None' else int(l.split('| phi ')[1].split()[1])) for l in open(os.path.join(b, 'polar-new4.log')) if '| phi ' in l}
    for r in load(os.path.join(b, 'polar-quick-new4.json')):
        r['phi']['overlaps'] = r['2']['overlaps'] = ov.get(r['D']); pol[r['D']] = r
    slo = {r['D']: r for r in load(os.path.join(a, 'sloping-bases.json'))}
    val = {}
    for r in load(os.path.join(a, 'star-valley.json')) + (load(os.path.join(b, 'valley-new4', 'star-valley.json')) if os.path.exists(os.path.join(b, 'valley-new4', 'star-valley.json')) else []):
        if 'steps' in r: val[(r['D'], r['t'])] = r
    cor = {r['D']: r for r in load(os.path.join(x, 'study2b.json')) + (load(os.path.join(b, 'study2b-new4.json')) if os.path.exists(os.path.join(b, 'study2b-new4.json')) else []) if r.get('D')}
    law = {r['D']: r for r in load(os.path.join(d, 'valley-law-predict.json'))}
    t3 = table3(P)
    bymeta = {os.path.basename(r['file'])[:-5]: r for r in sc}
    main, ecc, names = [], [], []
    def card(slug, r):
        m = meta[slug]; D = m['D'] or r['D']; nm = short(m['name']); anchor = 'card-' + D
        conv = m.get('convex') in (True, 'True', 'true'); NEW = D in ('D106', 'D107', 'D108', 'D109')
        fv = m['f_vector']; g = GROUP.get(r['verdict'], '?')
        key = (f"{m['symmetry']} (order {m['order']}) · {fv['vertices']} corners, {fv['edges']} edges, {fv['faces']} faces: {faces_txt(m['faces_by_sides'])} · "
               f"{'convex' if conv else 'non-convex'} · exact in {field(m['field'])} · {'first in ' + m['paper'] if m.get('paper') else ''}"
               f"{(', ' + m['doi'].replace('DICTO DOI: ', 'DICTO DOI ')) if m.get('doi') else ''}")
        rows = []
        vol = m['volume']; edges = m.get('sq_edges') or []
        ed = ('; '.join(f"{ex(e['exact'])} (×{e['count']})" for e in edges) if len(edges) <= 4 else
              f"{len(edges)} kinds, from {float(edges[0]['decimal']):.4f} to {float(edges[-1]['decimal']):.4f}" if edges else '')
        vx = ex(vol['exact']); rows.append(('Exact data', (f"volume {vx} ≈ {float(vol['decimal']):.6f}" if len(vx) < 90 else f"volume ≈ {float(vol['decimal']):.6f} (exact value in DICTO Solids v7, too long to print here)") + (f"; squared edge lengths {ed}" if ed else '') + ' (DICTO Solids v7)'))
        ph, tw = r.get('phi', {}), r.get('2', {})
        if r.get('pyramids_add_up'):
            rows.append(('Centre rule (Ch. 2, Table 1)' if not NEW else 'Centre rule (Ch. 2, run for this book)', f"group {g}: {GROUPTXT.get(g, '')}. Halo of the tips {ph.get('halo_over_solid', 0):.4f} × the solid at t = φ, "
                         f"{tw.get('halo_over_solid', 0):.4f} × at t = 2; {r['face_families']} face famil{'y' if r['face_families'] == 1 else 'ies'}"))
        else:
            rows.append(('Centre rule (Ch. 2)', 'the centre is not inside every face pyramid: no star from the centre'))
        p = pol.get(D)
        if p:
            q = p['phi']; rows.append(('Polar spikes (Ch. 2, Main theorem)' if not NEW else 'Polar spikes (Ch. 2 theorem, run for this book)', f"ρ² = φR²: the halo is the polar, {q['halo_over_solid']:.3f} × the solid; the layer is "
                                       f"{fv['vertices'] + fv['edges']} pieces, one pyramid per corner and one tetrahedron per edge, {(str(q['overlaps']) + ' overlaps') if q.get('overlaps') is not None else 'overlap test not run (polar_spikes.py tests layers of fewer than 1200 pieces)'}, volumes adding up "
                                       f"(ρ² = 2R²: halo {p['2']['halo_over_solid']:.3f} ×)"))
        elif not conv:
            rows.append(('Polar spikes (Ch. 2)', 'not decided for non-convex shapes: the layer pieces can cut into the solid (Chapter 2, Section 9)'))
        s = slo.get(D)
        if s:
            q = s['phi']; rows.append(("DICTO's sloping bases (Ch. 2, Table 2)", f"t = φ: {q['corner_pyramids']} corner pyramids and {q['edge_tetrahedra']} edge tetrahedra, no overlaps; "
                                       + ('they fill the halo exactly' if q['fills_hull'] else f"they close into a skin of its own, {q['volume_over_solid']:.4f} × the solid against the halo's {q['hull_of_tips_over_solid']:.4f}")))
        c = cor.get(D); t = t3.get(D)
        if c:
            if c.get('period'):
                k = c['enters_cycle_at_turn']; lin = CORE_LIN.get(c['gain_radius_squared_t1'])
                when = 'at once' if k == 0 else f'from turn {k}'
                thm = 'the Theorem' if D != 'D37' else 'the one exception to the Theorem, computed'
                rows.append(('Core (Ch. 3)' if not NEW else 'Core (Ch. 3 rule, exact, run for this book)', f"period two {when} ({thm}); two turns scale the core by {('t²/' + lin[2:]) if lin and lin.startswith('1/') else 't²·' + str(lin)} in length"
                             + ('' if lin else f" (squared radius {ex(c['gain_radius_squared_t1'])})")))
            else:
                o = c.get('outcome') or c.get('error', '')
                rows.append(('Core (Ch. 3)', re.sub(r':.*', '', o) + (' (Proposition 3: the families of tips lie in a plane)' if 'no core' in o else '')))
        elif g in 'AB' and r.get(('phi')) and r['phi'].get('core'):
            co = r['phi']['core']; rows.append(('Core (study, float)', f"first core: {co['V']} corners, {faces_txt(co['faces'])}; corners on one sphere"))
        elif not conv:
            rows.append(('Core (Ch. 3)', 'not run: Chapter 3 treats the convex shapes'))
        ch = (t or {}).get('chain')
        NEWCH = {'D106': 'period four: the cube with its edges cut back closes at the depth s = 3/5 (Ch. 4, Sect. 6)',
                 'D107': 'period four, while the Archimedean truncated cuboctahedron does not close (Ch. 4, Sect. 6; study 3)',
                 'D108': 'step five of the chain of the Ogdoecontahedron, after KRE, PHE, TPP and DPHP; that chain does not close within nine steps (Ch. 4, Sect. 6)',
                 'D109': 'step six of the chain of the Ogdoecontahedron, after Hamlet; that chain does not close within nine steps (Ch. 4, Sect. 6)'}
        if D in NEWCH: rows.append(('Chain of T (Ch. 4)', NEWCH[D]))
        if D in GAINS: rows.append(('Chain of T (Ch. 4, Table 1)', f"period four, radius gain {GAINS[D]}"))
        elif ch:
            rows.append(('Chain of T (Ch. 2, Table 3)', {'open (8 steps)': 'not closed in eight steps (screened)', 'period 4': 'period four', '–': 'not run',
                                                        'no centre': 'not run: no centre fixed by every symmetry'}.get(ch, ch)))
        vp, v2 = val.get((D, 'phi')), val.get((D, '2'))
        if t and t['vphi'] != '–': gp, g2 = t['vphi'], t['v2']
        else: gp, g2 = (valley_growth(vp) if vp else None), (valley_growth(v2) if v2 else None)
        if gp or g2:
            rows.append(("Building on the star (Ch. 2, Sect. 7)", f"DICTO's valley rule, volume added over steps two and three: {gp or 'not run'} at t = φ, {g2 or 'not run'} at t = 2"
                         + (' (freezes: less than 0.1 per cent at step three)' if 'freezes' in (gp or '') + (g2 or '') else '')))
        else:
            rows.append(("Building on the star (Ch. 2, Sect. 7)", 'not run (over 200 faces)' if fv['faces'] > 200 else 'not run'))
        lw = law.get(D) or ({'delta_deg': [NEWDELTA[D]]} if D in NEWDELTA else None)
        if lw:
            dm = min(lw['delta_deg'])
            rows.append(('Valley law (Ch. 5, Theorem)', f"sharpest dihedral angle {dm:.2f}°: " + (('exactly 120°, the bound itself: ' if abs(dm - 120) < 1e-6 else 'at most 120°, so ') + 'a valley stays open through step two at t = 2' if dm <= 120 + 1e-9 else
                         'blunter than 120°, so every valley at t = 2 is closed by step two')))
        if D in SLOPE6:
            sh, used, s3, a2, ap = SLOPE6[D]
            rows.append(('Sloping bases at sharp edges (Ch. 5, added section)', f"sharp edges {sh} (t = 2 / φ); used / not possible at step 3, t = 2: {used}; step 3 {s3}; "
                         f"steps 1–3: ×{a2} at t = 2, ×{ap} at t = φ. No piece stops."))
        if D == 'D86':
            rows.append(('Notches (Ch. 5, Sect. 6)', "the faces at its five reflex edges never take a spike under the valley rule (notch open at 158.38° throughout); "
                         "it grows ×2.563 over three steps at t = 2 and ×2.607 at t = φ; with Maedate ×3.058 and ×2.656, with Kuwagata ×2.542 (stops at step three) and ×2.715"))
        rows.append(('Note (inventory)', html.escape(m.get('note') or '')))
        return D, nm, anchor, key, rows
    def html_card(D, nm, anchor, key, rows, img, alt):
        names.append((nm, D, anchor))
        return (f'<section class="card" id="{anchor}"><h2 class="cardt"><span class="dn">{D}</span>{html.escape(nm)}</h2><p class="pkey">{html.escape(key)}</p>'
                f'<figure><img src="{img}" alt="{html.escape(alt)}"></figure><table class="cd">' +
                ''.join(f'<tr><th>{h}</th><td>{v}</td></tr>' for h, v in rows) + '</table></section>\n')
    PANEL_C = 'Top: the solid (faces coloured by family) and its star by the centre rule at t = φ; bottom: its star with polar spikes at ρ² = φR² and the halo, the hull of their tips.'
    PANEL_N = 'Top: the solid and its star by the centre rule at t = φ; bottom: the star at t = 2 and the solid from below.'
    order = sorted(sc, key=lambda r: int(r['D'][1:]))
    for r in order:
        slug = os.path.basename(r['file'])[:-5]; D, nm, anc, key, rows = card(slug, r)
        conv = meta[slug].get('convex') in (True, 'True', 'true')
        h = html_card(D, nm, anc, key, rows, f'figures/cards/{slug}.png', f'{nm}: ' + (PANEL_C if conv else PANEL_N))
        h = h.replace('</h2>', '</h2>', 1).replace('<table class="cd">', f'<table class="cd"><tr><th>Picture</th><td>{PANEL_C if conv and "pyramids_add_up" in r and r["pyramids_add_up"] else PANEL_N}</td></tr>', 1)
        (ecc if D in ECC else main).append((ECC.index(D) if D in ECC else 0, h))
    ecc = [h for _, h in sorted(ecc, key=lambda x: x[0])]; main = [h for _, h in main]
    # the notch pieces (#85, Section 6; study 2026-11-01-star-cores-d)
    kv = load(os.path.join(d, 'kagemusha-variants.json')); kc = load(os.path.join(d, 'kuwagata-cycle.json'))
    for var, nm, jp, D in (('conjoined', 'Maedate', '前立, the front crest of a samurai helmet', 'Notch 1'), ('sloping', 'Kuwagata', '鍬形, the V-shaped horns of a samurai helmet', 'Notch 2')):
        R = {x['t']: x for x in kv if x['variant'] == var}
        st = {t: [s['volume_over_last'] for s in R[t]['steps']] for t in R}
        tot = {t: st[t][0] * st[t][1] * st[t][2] for t in st}
        s1 = R['2']['steps'][0]; cyc = kc[var]
        piece = ('one conjoined piece per notch, the hull of the notch edge, the two far corners of its faces and the two full step-one tips: a combinatorial octahedron (6 corners, 8 triangles), '
                 f"volume {R['2']['steps'][0]['notch_piece_volume'][0]:.4f} at t = 2 and {R['phi']['steps'][0]['notch_piece_volume'][0]:.4f} at t = φ (Kagemusha = 1); outer edges 0.507, 0.764, 0.851 and 1 at t = 2"
                 if var == 'conjoined' else
                 'DICTO\'s sloping bases read for a notch: each notch face keeps a pyramid whose apex lies where the line from its far corner to its tip meets the notch\'s mirror plane, '
                 f"so the two meet face to face; the pair is a triangular dipyramid, 2 × {R['2']['steps'][0]['notch_piece_volume'][0]:.4f} at t = 2 and 2 × {R['phi']['steps'][0]['notch_piece_volume'][0]:.4f} at t = φ (Kagemusha = 1); outer edges 0.729, 0.927 and 1 at t = 2")
        rows = [('Picture', 'Top: one piece (t = 2) and Kagemusha (gold) with its five notch pieces (teal); bottom: the star after step one at t = 2 and t = φ, cap spikes violet.'),
                ('The piece (Ch. 5, Sect. 6)', piece),
                ('Placed', f"in the five notches of Kagemusha (D86) at step one; no notch piece meets the solid or another piece; the surface after step one has {s1['corners']} corners, {s1['edges']} edges and {s1['faces']} faces, closed, Euler characteristic 2"),
                ('Growth (Ch. 5, Sect. 6)', f"steps one to three, volume over the step before: t = 2: ×{st['2'][0]:.4f}, ×{st['2'][1]:.4f}, ×{st['2'][2]:.4f} (×{tot['2']:.3f} in all); "
                 f"t = φ: ×{st['phi'][0]:.4f}, ×{st['phi'][1]:.4f}, ×{st['phi'][2]:.4f} (×{tot['phi']:.3f}); empty notches give ×2.563 and ×2.607"),
                ('Finished star' if var == 'sloping' else 'Star after three steps', (f"at t = 2 the star stops at step three (×{st['2'][2]:.10f}): {cyc['corners']} corners, {cyc['faces']} faces "
                 f"({faces_txt(cyc['faces_by_sides'])}), symmetry of order {cyc['symmetry_order']} (D5h, Kagemusha's own); similar to no solid of DICTO Solids v7"
                 if var == 'sloping' else f"at t = 2 it is still growing: {cyc['corners']} corners, {cyc['faces']} faces ({faces_txt(cyc['faces_by_sides'])}), symmetry of order {cyc['symmetry_order']}")),
                ('Core of the turn (study, not in a paper)', f"the core rule of Chapter 3 at t = 2 gives a decagonal prism ({faces_txt(cyc['core_sequence'][0]['faces'])}, all corners on one sphere); "
                 "the next turn has no core, its families of tips lying in planes: the sequence ends after one turn (study 2026-11-01-star-cores-d, kuwagata_cycle.py)"),
                ('Name', f"DICTO's name, 1 November 2026: {nm} ({jp}). {'Maedate makes Kagemusha grow most at t = 2' if var == 'conjoined' else 'With Kuwagata the star of mirrored spikes reaches a finished form'} (Chapter 5, #85).")]
        ecc.append(html_card(D, f'{nm} ({jp.split(",")[0]})', 'card-' + nm.lower(), f"DICTO's notch piece of Kagemusha (D86) · {'conjoined spikes' if var == 'conjoined' else 'sloping bases'} · float64 study (2026-11-01-star-cores-d, kagemusha_variants.py)",
                             rows, f'figures/cards/{nm.lower()}.png', f'{nm}: one piece, Kagemusha with five, and the star after step one'))
    names[:] = [(n.split(' (')[0] if n.startswith(('Maedate', 'Kuwagata')) else n, D, a) for n, D, a in names]
    return main, ecc, names
