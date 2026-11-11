#!/bin/bash
# Typeset the Star Cores book draft on compute-host: papers/book-star-cores is synced to ~/work/star-cores-book/typeset/papers,
# then ../print.mjs (A4, footer with the DICTO mark line) prints paper.html to dicto-star-cores.pdf (version 1; DRAFT-star-cores-book.pdf for the drafts); page images for checking.
T=~/work/star-cores-book/typeset; cd $T/papers || exit 1
[ -e $T/node_modules ] || ln -s ~/kaleidohedra-check/node_modules $T/node_modules
node print.mjs book-star-cores dicto-star-cores.pdf "Star Cores" "10.5281/zenodo.23867732" 1 && pdfinfo book-star-cores/dicto-star-cores.pdf | grep Pages
