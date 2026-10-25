#!/bin/bash
# Prior art: download Hales's three arXiv papers into the reference library inbox (dicto-big-brother), extract text, and ask the local
# 120b whether they contain anything like the rule of halves (hole cells of mixed stackings built from halves of fcc/hcp pieces).
set -u; mkdir -p ~/kres-tmp/priorart && cd ~/kres-tmp/priorart
for id in 9811071 9811073 9811077; do [ -s hales-$id.pdf ] || curl -sL -m 120 -o hales-$id.pdf "https://arxiv.org/pdf/math/$id"; pdftotext -layout hales-$id.pdf hales-$id.txt 2>/dev/null; done
python3 - <<'P'
import re
ks = re.compile(r'(hexagonal close|face-centered|stacking|octahedr|decomposition star|Delaunay star|hcp|fcc)', re.I)
out = []
for id in ('9811071', '9811073', '9811077'):
    t = open(f'hales-{id}.txt', errors='ignore').read(); paras = [p for p in re.split(r'\n\s*\n', t) if ks.search(p)]
    out.append(f'=== arXiv math/{id}: {len(t)} chars, {len(paras)} relevant paragraphs\n' + '\n---\n'.join(paras[:40]))
open('../dg.txt', 'w').write("QUESTION FOR THIS READ: Do these excerpts from Hales's Kepler-conjecture papers contain any statement that, in close packings with arbitrary stacking (not only fcc and hcp), the cells (Voronoi, Delaunay, hybrid or power cells) of the octahedral or tetrahedral holes are built from halves of the fcc and hcp cells, or any rule that a hole's cell depends only on the h/c type of the neighbouring layers? Quote any such passage exactly; otherwise say clearly that there is none, and list what these papers DO say about fcc, hcp and other stackings.\n\n" + '\n\n'.join(out))
P
bash ~/kres-tmp/read120.sh; cp ~/kres-tmp/read120.out.md ~/kres-tmp/priorart/hales-read120.md
