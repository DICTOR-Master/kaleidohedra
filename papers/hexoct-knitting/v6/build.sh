#!/bin/sh
# #83 Version 6 DRAFT: four parts printed on the print host with the house pipeline (figcheck, then print.mjs), joined in order
# front, Part 1, Part 2, Part 4 (crochet). Usage: sh build.sh
set -e
cd "$(dirname "$0")"
D=k83-v6; H=compute-host-2; T='Knitting vs Crocheting Crystals'; DOI=10.5281/zenodo.23848271
rsync -a --delete --exclude '*.pdf' --exclude build.sh ./ $H:kaleidohedra-papers/$D/
rsync -a ../../paper.css ../../dicto-logo.png ../../print.mjs ../../figcheck.mjs ../../edgecheck.py ../../edgecheck-allow.txt $H:kaleidohedra-papers/
ssh $H "cd ~/kaleidohedra-papers && python3 edgecheck.py $D/crochet/figs/*.png && for p in front part1 part2 crochet; do node figcheck.mjs $D/\$p && node print.mjs $D/\$p DRAFT-k83-\$p.pdf '$T' $DOI 6 || exit 1; done && python3 -c 'import pypdf,sys; w=pypdf.PdfWriter(); [w.append(f) for f in sys.argv[2:]]; w.write(sys.argv[1])' $D/DRAFT-83-v6-knitting-vs-crocheting.pdf $D/front/DRAFT-k83-front.pdf $D/part1/DRAFT-k83-part1.pdf $D/part2/DRAFT-k83-part2.pdf $D/crochet/DRAFT-k83-crochet.pdf"
rsync -a $H:kaleidohedra-papers/$D/DRAFT-83-v6-knitting-vs-crocheting.pdf ./
cp DRAFT-83-v6-knitting-vs-crocheting.pdf ~/Documents/papers-to-read/
