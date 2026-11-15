#!/bin/sh
# #83 Version 6: front, Part 1, Part 2, Part 4 (crochet) and the Appendix (crochet pattern, core templates at 1:1),
# each printed on the print host with the house pipeline (edge guard, figcheck, print.mjs), then joined in order. Usage: sh build.sh
set -e
cd "$(dirname "$0")"
D=k83-v6; H=compute-host-2; T='Knitting vs Crocheting Crystals'; DOI=10.5281/zenodo.23848271; OUT=dicto-hexoct-knitting-v6.pdf
rsync -a --delete --exclude '*.pdf' --exclude '*.json' --exclude build.sh ./ $H:kaleidohedra-papers/$D/
rsync -a ../../paper.css ../../dicto-logo.png ../../print.mjs ../../figcheck.mjs ../../edgecheck.py ../../edgecheck-allow.txt $H:kaleidohedra-papers/
ssh $H "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/crochet/figs/*.png $D/appendix/fig/*.png && for p in front part1 part2 crochet appendix; do node figcheck.mjs $D/\$p && node print.mjs $D/\$p k83-\$p.pdf '$T' $DOI 6 || exit 1; done && python3 -c 'import pypdf,sys; w=pypdf.PdfWriter(); [w.append(f) for f in sys.argv[2:]]; w.write(sys.argv[1])' $D/$OUT $D/front/k83-front.pdf $D/part1/k83-part1.pdf $D/part2/k83-part2.pdf $D/crochet/k83-crochet.pdf $D/appendix/k83-appendix.pdf"
rsync -a $H:kaleidohedra-papers/$D/$OUT ./
