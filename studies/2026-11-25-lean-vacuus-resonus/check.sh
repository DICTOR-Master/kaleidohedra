#!/bin/bash
# usage: check.sh TAG MODULE thm1 thm2 ... : build MODULE, print axioms, count sorry -> logs/build-TAG.log (FINAL ok only if clean)
cd ~/lean/vacuus-resonus && export PATH=$HOME/.elan/bin:$PATH
tag=$1; mod=$2; shift 2
{ echo "import $mod"; for t in "$@"; do echo "#print axioms VacuusResonus.$t"; done; } > /tmp/ax-vacres-$tag.lean
log=logs/build-$tag.log
{ date; timeout 280 lake build $mod 2>&1 | grep -v "^✔\|^⣿\|^info: " | tail -80; timeout 120 lake env lean /tmp/ax-vacres-$tag.lean; echo "sorry/admit/axiom/native_decide hits:"; grep -nE "\bsorry\b|\badmit\b|^axiom|native_decide" VacuusResonus/*.lean | wc -l; } > $log 2>&1
grep -q "Build completed successfully" $log && ! grep -q "sorryAx\|warning\|error" $log && ! grep "depends on axioms" $log | grep -vq "\[propext, Classical.choice, Quot.sound\]" && grep -q "hits:" $log && [ "$(tail -1 $log)" = 0 ] && echo "FINAL ok" >> $log
cat $log
