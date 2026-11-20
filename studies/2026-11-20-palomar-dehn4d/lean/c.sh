#!/bin/bash
# usage: c.sh File [lines]  (compile one file of DehnHadwiger/ on the compute host, write its olean)
f=$1
cd "${WORKSPACE:?set WORKSPACE to the Lean project folder}" && export PATH=$HOME/.elan/bin:$PATH && /usr/bin/time -f "%e s %M KB" timeout 270 lake env lean -o .lake/build/lib/lean/DehnHadwiger/$f.olean DehnHadwiger/$f.lean 2>&1 | head -${2:-60}
