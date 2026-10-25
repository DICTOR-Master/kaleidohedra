#!/bin/sh
# paper.src.html -> paper.html (study commit $1; DOI given as $2, else "reserved on publication"), then print on dicto-big-brother in
# ~/kres-tmp/relay-census (node_modules -> ~/kaleidohedra-check/node_modules, as for #52).
# Appendix C (__WALKTABLES__) is generated here from the study's data/raw/tables.md, so the walk tables are never retyped.
#   sh build.sh <study commit> [DOI] [pdf name] [version]
set -e
cd "$(dirname "$0")"
python3 - "$1" "${2:-}" <<'P'
import sys, re, html
NAMES = {"square": "square lattice + centres", "honeycomb": "honeycomb + hexagon centres", "kagome": "kagome + hexagon centres",
         "bcc": "CsCl (bcc two-kind; golden-loop sites)", "delian": "fluorite (fcc + all tetrahedral holes; Delian-loop sites)",
         "nacl": "rock salt NaCl", "zincblende": "zinc blende ZnS", "hcpholes": "hcp holes (octahedral + tetrahedral holes of ideal hcp)",
         "a15": "A15 Cr₃Si", "c15": "C15 Laves MgCu₂"}
md = open('../../studies/2026-10-25-relay-census/data/raw/tables.md').read()
out = []
for block in md.strip().split('\n**')[0:]:
    block = block.strip().lstrip('*')
    if not block: continue
    head, _, rest = block.partition('\n')
    key = head.split('**')[0].strip()
    lamdef = head.split('; λ = ')[1].split(';')[0] if '; λ = ' in head else ''
    rows = [r for r in rest.strip().split('\n') if r.startswith('|')]
    hdr = [c.strip() for c in rows[0].strip('|').split('|')]
    body = [[c.strip() for c in r.strip('|').split('|')] for r in rows[2:]]
    fix = lambda s: re.sub(r'(?<![A-Za-z])-(?=[0-9(])', '−', html.escape(s)).replace('-', '–')
    t = [f'<tr><th colspan="{len(hdr)}" style="padding-top:6pt">{html.escape(NAMES[key])} · λ = {html.escape(lamdef).replace("w_", "w<sub>").replace(" - ", "</sub> − ")}</sub></th></tr>']
    t.append('<tr>' + ''.join(f'<td class="h">{fix(h)}</td>' for h in hdr) + '</tr>')
    for r in body:
        t.append('<tr>' + ''.join(f'<td class="n">{fix(c)}</td>' for c in r) + '</tr>')
    out.append('<table class="walk">' + '\n'.join(t) + '</table>')
s = open('paper.src.html').read().replace('__WALKTABLES__', '\n'.join(out))
doi = ('DICTO DOI: ' + sys.argv[2]) if sys.argv[2] else 'DICTO DOI: reserved on publication'
s = s.replace('__DOI__', doi).replace('__COMMIT__', sys.argv[1])
open('paper.html', 'w').write(s)
P
rsync -a --delete --exclude pg ./ ${PRINT_NODE:-dicto-big-brother}:kres-tmp/relay-census/2026-10-25-relay-census/
rsync -a ../paper.css ../dicto-logo.png ../print.mjs ${PRINT_NODE:-dicto-big-brother}:kres-tmp/relay-census/
ssh ${PRINT_NODE:-dicto-big-brother} "cd ~/kres-tmp/relay-census && ln -sfn ~/kaleidohedra-check/node_modules node_modules && nice -n 10 node print.mjs 2026-10-25-relay-census ${3:-relay-census-draft.pdf} 'Bond hand-over census (working title)' '${2:-reserved}' ${4:-1}"
rsync -a ${PRINT_NODE:-dicto-big-brother}:kres-tmp/relay-census/2026-10-25-relay-census/${3:-relay-census-draft.pdf} ./
