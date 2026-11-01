#!/bin/bash
# Typeset the Star Cores book draft on dicto-big-brother: papers/book-star-cores is synced to ~/kres-tmp/star-cores-book/typeset/papers,
# then ../print.mjs (A4, footer with the DICTO mark line) prints paper.html to DRAFT-star-cores-book.pdf; page images for checking.
T=~/kres-tmp/star-cores-book/typeset; cd $T/papers || exit 1
[ -e $T/node_modules ] || ln -s ~/kaleidohedra-check/node_modules $T/node_modules
node print.mjs book-star-cores DRAFT-star-cores-book.pdf "Star Cores · DRAFT for reading" "none yet" "0 (draft)" && pdfinfo book-star-cores/DRAFT-star-cores-book.pdf | grep Pages
