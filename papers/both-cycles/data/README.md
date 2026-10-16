DICTO · dictospheres.com

# Double Vision – Both Cycles in One Space: data and scripts (DICTO DOI: 10.5281/zenodo.23407107)

These are copies of the study files behind the paper. The full studies, with their history, are at https://github.com/DICTOR-Master/kaleidohedra on the research branch, in studies/2026-10-16-interlock, studies/2026-10-16-polar-dharma and studies/_lib. The study README, copied here as `study-README.md`, describes every step.

- **Both chains in one frame:** `polar.py` (with `exact.py`, reading `dharma_cycle.json`; its reversed chain is in `polar-step1.txt`), then `chains.py` → `orig-chain.json`, `flip-ends-chain.json`.
- **The interlock, float:** `interlock.py` (ends; an argument for the middle setting) → `interlock-ends.json`, `interlock-middle.json` and their `.txt` summaries; the cone-cut pieces of each cycle are in `orig-pieces.*` and `flip-ends-pieces.*`.
- **The interlock, exact:** `interlock_exact.py` (with `geomcheck.py`) → `interlock-ends-exact.txt`, `interlock-middle-exact.txt`: exact corners, remainder 0 in every piece and layer, kinds by volume and by orbit under the full icosahedral group.
- **Tables 1–3:** `interlock_kinds.py` → `interlock-kinds.txt`.
- **The middle-setting icosahedron is 3·I (exact):** `middle_icosa_3I.py` → `middle-icosa-3I.txt`.
- **Figures:** `interlock_kinds_render.py` and `p4_render_data.py` → `interlock-kinds-render-*.json`, `p4-render-*.json`; `p4_xray_data.py` → `p4-xray-*.json`; `render_p4.html` (hero, slice, peel, kit, locators) shot by `shoot_p4.mjs` and `shoot_p4_slice.mjs`; `p4_compose.py` composes Figures 1–5. `p4_figures.py`, `render_p4_xray.html` and `shoot_p4_xray.mjs` draw the earlier flat and glass diagrams kept in the study record.
- **Checks:** `python3 test_geomcheck.py`.

The scripts were written for the repository layout, so the paths inside them refer to the study folders. Outputs are float unless a file says exact. Figures are drawn from float corners of exact pieces.
