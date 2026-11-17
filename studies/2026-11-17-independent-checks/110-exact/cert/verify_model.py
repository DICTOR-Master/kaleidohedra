#!/usr/bin/env python3
"""Control for the cover CNF: read a SAT solver's model (lines 'v ...') for make_cnf.py's CNF at a K where a cover exists,
and check directly against the instance that the chosen copies number at most K and cover all 720 pentagons. This shows
the encoding admits real covers (the UNSAT certificate at K - 1 is then about the right question).
Usage: verify_model.py instance.json FAMILY K solver_output.txt   (prints FINAL ok / FINAL FAIL)"""
import sys, json
inst, fam, K, outp = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
sets = json.load(open(inst))[fam]['sets']; n = len(sets)
txt = open(outp).read()
sat = any(l.strip() == 's SATISFIABLE' for l in txt.splitlines())
lits = [int(t) for l in txt.splitlines() if l.startswith('v ') for t in l[2:].split()]
chosen = [v for v in lits if 0 < v <= n]
covered = set().union(*(sets[c - 1] for c in chosen)) if chosen else set()
print(f'{fam} K={K}: solver SAT={sat}, {len(chosen)} copies chosen, {len(covered)} of 720 pentagons covered')
ok = sat and len(chosen) <= K and len(covered) == 720
print('FINAL ok' if ok else 'FINAL FAIL model is not a cover of size <= K')
