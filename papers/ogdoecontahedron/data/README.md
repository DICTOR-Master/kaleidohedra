DICTO · dictospheres.com

# The DICTO Ogdoecontahedron: data and scripts (DICTO DOI: 10.5281/zenodo.23404688)

Copies of the study files behind the paper. The full studies, with their history, are in https://github.com/DICTOR-Master/kaleidohedra on branch research.

- **The solid** (studies/2026-10-16-polar-dharma):
  - `polar.py` computes the exact polar of every station, including the Hecatodihedron stage. It uses `exact.py` (from studies/2026-10-15-icosa-star-hollow) and reads `dharma_cycle.json`.
  - Its output is in `polar-step1.txt` and `reversed-chain.json` (floats).
  - Figure 1 comes from `hstar_render.py`, `hstar-render.json` and `render_hstar.html`.
- **Flip test** (studies/2026-10-16-flip-test): `flip.py` → `flip-dharma.txt`.
- **Face arrangement and catalogue scan** (studies/2026-10-16-ocd-pyrochlore): `ocd_dl0d.py` → `ocd-dl0d.txt`, and `ocd_catalogue_scan.py` → `ocd-catalogue.txt` and `ocd-catalogue-names.txt`.
- **Packings** (studies/2026-10-16-ocd-pyrochlore): `network.py` → `network.txt` (diamond network, pyrochlore joints, bcc density, all exact), and `densest.py` → `densest.txt` (lattice local search, float).
- **Quasicrystal check** (studies/2026-10-16-ogdoecontahedron-bridge, commit 3fd407f): `bridge.py` → `bridge.txt`, described in `bridge-README.md`. It uses `geomcheck.py` (studies/_lib).
- **Computed for the paper:** the face distances, the edge distances (no midsphere), the dihedral angles and the central-symmetry check are recorded in the polar-dharma study README, under "Further properties of the Ogdoecontahedron".

The scripts were written for the repository layout. Paths inside them refer to the study folders.
