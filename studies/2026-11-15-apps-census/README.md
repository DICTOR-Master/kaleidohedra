# Apps census and The Five Orders of Space (15 Nov 2026)

**Conclusion (15 Nov 2026): proposal, for DICTO's read.** Every world and door of the joined app (Kaleidohedra, Rhombiverse, Polyhedraverse doors; DICTO wizard; dictospheres.com) is mapped to its home book and ring. One pick: inside the gold DICTO block, list the 37 entries under the five rings in book order (today's order kept inside each book), with a ring jump row and a "new" mark; move Golden Breathing Pyrochlore and Golden Bodhi Pyrochlore Networks from the two classical lattice blocks into the gold block (Book One); everything else stays. Nothing in any app, the site or a repository was changed.

DICTO, 15 November 2026: "maybe we need a census of all apps and whether they need to be reordered in line with The Five Orders of Space headings".

- `data/census.json`: the census (worlds, papers, home book, other books; other doors).
- `scripts/make_html.py <dimension-wizard.js>`: reads the current gold-block order from the wizard code, checks every DICTO world has exactly one census row, writes `paper/paper.html`; FINAL ok/FAIL.
- `build.sh <dimension-wizard.js>`: html, figcheck and print.mjs on the compute host; PDF `paper/DRAFT-apps-five-orders-census.pdf`.

Run of 15 Nov 2026 (Kaleidohedra master 24ddb349): 33 gold worlds in the code + 2 DICTO lattices + 2 lattices moved in = 37 rows; FINAL ok.

Built 16 Nov 2026 (DICTO: "apps proposal start work"; Kaleidohedra branch five-orders-gold, not yet deployed): the wizard now holds the order itself (`FIVE_RINGS`, `DICTO_SHELF` in `src/app/dimension-wizard.js`). On such code `make_html.py` checks it against the census instead of rewriting `paper/paper.html` (the proposal as read): every row once on the shelf under its census book, in the order of Table 1, the two pyrochlore worlds in DICTO_WORK, Golamandalas (no book yet) after the rings. Run: 36 on the shelf + 1 no book yet = 37 entries, 37 census rows; FINAL ok (master 24ddb349 still gives FINAL ok in the old mode, paper.html unchanged).

LEADS: Golamandalas (#103) needs a book; Targets and Shells have no paper; site "In the book" labels predate Books Two, Seven and Eight; site shelf order (Quanta, HexOct first) differs from series order (DICTO's call).
