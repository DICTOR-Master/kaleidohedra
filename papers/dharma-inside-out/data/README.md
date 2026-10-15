DICTO · dictospheres.com

# Inverted Shells: data and scripts (DICTO DOI: 10.5281/zenodo.23405029)

These are copies of the study files behind the paper. The full studies, with their history, are at https://github.com/DICTOR-Master/kaleidohedra on the research branch, in studies/2026-10-16-polar-dharma, studies/2026-10-16-flip-test and studies/_lib. The study README, copied here as `study-README.md`, describes every step.

- **The reversed chain:** `polar.py`, which uses `exact.py` and reads `dharma_cycle.json`. Output: `polar-step1.txt` and `reversed-chain.json`.
- **One piece per layer:** `polar_pieces.py` (which uses `geomcheck.py`) → `polar-step2.txt` and `polar-pieces.json`. Then `polar_exact.py` → `polar-exact.txt`.
- **The tight nest:** `polar_tight.py` → `polar-tight*.txt`. Then `polar_exact.py tight` → `polar-tight-exact.txt`.
- **The stars:** `polar_stars.py` → `polar-stars*.txt`. The exact fit and pieces of the great stellated dodecahedron: `polar_gsd_exact.py` and `polar_gsd_pieces.py` → `polar-gsd-*.txt`. Hafner's tetrahedra: `polar_hafner_exact.py` → `polar-hafner-exact.txt`.
- **The inner gap:**
  - `polar_heca_gap.py` → `polar-heca-gap.txt`;
  - `polar_round.py` → `polar-round.txt`;
  - `polar_dual_pair.py` → `polar-dual-pair.txt`;
  - `polar_pair.py tid|rid`, then `polar_exact.py tid|rid` → `polar-pair*.txt`.
- **Golden frame:** `polar_golden_rect.py` → `polar-golden-rect.txt`.
- **Core:** `polar_turns.py` and `turns_nested.py`.
- **Flip test:** `flip.py` → `flip-dharma.txt`.
- **Checks:** `python3 test_geomcheck.py`.
- **Renders:** the `render_*.html` pages with the `shoot_*.mjs` scripts, plus `pieces_gallery.py`. The `*-render.json` files are their inputs.

The scripts were written for the repository layout, so the paths inside them refer to the study folders. Outputs are float unless a file says exact.
