#!/bin/bash
# usage: check.sh TAG thm1 thm2 ... : full build, axioms, sorry count, lines -> logs/build-TAG.log (FINAL ok only if clean)
cd ~/lean/alexandrov && export PATH=$HOME/.elan/bin:$PATH
tag=$1; shift
{ echo "import Alexandrov"; for t in "$@"; do echo "#print axioms Alexandrov.$t"; done; } > /tmp/ax-alexandrov.lean
log=logs/build-$tag.log
{ date; timeout 250 lake build 2>&1 | tail -2; timeout 100 lake env lean /tmp/ax-alexandrov.lean; echo "sorry/admit/axiom hits:"; grep -nE "\bsorry\b|\badmit\b|^axiom" Alexandrov/*.lean Alexandrov.lean | wc -l; wc -l Alexandrov/*.lean Alexandrov.lean | tail -1; } > $log 2>&1
grep -q "Build completed successfully" $log && ! grep -q "sorryAx\|warning\|error" $log && ! grep -vq "propext, Classical.choice, Quot.sound\]\|^[^']" <(grep "depends on axioms" $log) && echo "FINAL ok" >> $log
cat $log
