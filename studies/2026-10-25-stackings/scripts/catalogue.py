# Catalogue step B (DICTO 2026-10-25): every piece that can occur in ANY close-packed stacking.
# reach.py: no piece is wider than R = 1/√2, so a site can be shaped only by sites within 2R + 3/8/(2R) ≈ 1.68 (2.06 layer spacings);
# the sites of gap k (between layers k and k+1) therefore see only gaps k−2..k+2, i.e. the six layers k−2..k+3. Up to relabelling
# A/B/C those six layers are fixed by the h/c character of the four inner layers: 16 windows. For each window we close it into a
# periodic stacking (six layers, or seven if the ends clash), walk it exactly with the census engine (which re-checks its distance
# bound on every stretch), and record the pieces of the three sites of the central gap at every stop and on every stretch.
# The union over the 16 windows is the complete catalogue. Output ../catalogue.json, ../catalogue.txt.
import json, itertools, sys
from fractions import Fraction as Fr
import census
from networks import NETS
from stackings import net_for
def word_for(hc):                 # hc: 4 letters h/c for layers k−1..k+2 → a 6-letter A/B/C word for layers k−2..k+3
    w = ['A', 'B']
    for t in hc:
        prev, cur = w[-2], w[-1]
        nxt = prev if t == 'h' else ({'A', 'B', 'C'} - {prev, cur}).pop()
        w.append(nxt)
    if w[-1] == w[0]: w.append(sorted({'A', 'B', 'C'} - {w[-1]})[0])   # ends clash: one more layer closes the cycle
    return ''.join(w)
if __name__ == '__main__':
    cat, rows = {}, []
    for hc in itertools.product('hc', repeat=4):
        hc = ''.join(hc); word = word_for(hc); key = 'cat_' + hc
        NETS[key] = net_for(word); census.NETS[key] = NETS[key]
        C = census.Census(key); d = C.walk(); fails = [c for c in C.checks if c[0] != 'PASS']
        central = {3 * 2, 3 * 2 + 1, 3 * 2 + 2}    # the three sites of gap k = 2 (layers 2→3 of the word: window layers k, k+1)
        seen = []
        for rec, kind in [(s, 'stop') for s in d['stops']] + [(iv, 'stretch') for iv in d['intervals']]:
            where = rec['lam'] if kind == 'stop' else f"({rec['lo']}, {rec['hi']})"
            for x in rec['sites']:
                if x['i'] not in central or x.get('vanished'): continue
                sig = f"{x['kind']} | {x['corners']} corners | faces {sorted(x['face_sizes'])} | bonds {x['bonds']}"
                seen.append((kind, where, sig)); cat.setdefault(sig, set()).add(f"{kind} {where} [{hc}]")
        rows.append(f"== window {hc} (word {word}): {len(d['stops'])} stops, {len(C.checks) - len(fails)} PASS, {len(fails)} FAIL")
        print(rows[-1], flush=True)
    out = {sig: sorted(v) for sig, v in cat.items()}
    json.dump(out, open('../catalogue.json', 'w'), indent=1)
    with open('../catalogue.txt', 'w') as fh:
        fh.write('\n'.join(rows) + '\n\nDISTINCT PIECES (central-gap sites over all 16 windows):\n')
        for sig in sorted(out, key=lambda s: (s.split('|')[0], int(s.split('|')[1].split()[0]))):
            fh.write(f"{sig}\n    seen at: {'; '.join(sorted({w.split(' [')[0] for w in out[sig]}))}\n")
    print(f'{len(out)} distinct pieces')
