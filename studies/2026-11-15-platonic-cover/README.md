# Series front cover for The Platonic Solids (15 Nov 2026) - DICTO · dictospheres.com

DICTO, 15 Nov 2026: a new cover "matching protocols" (the house style of his other book covers). Not yet in the book: the current
white cover (book-platonic/front.html, cover/cover-skins.png) stays until DICTO chooses.

- Image: the five Platonic solids as stones in their element colours, each in its gold setting of #106 Table 1 / Chapter 10
  Table 10.2, so that stone + setting is exactly the dodecahedron of edge 1: D bare; I in 6 Admiral Caps + 8 caps; C in Euclid's
  6 roofs; T (edge phi sqrt2) in 4 corner tetrahedra + 6 roofs; O (edge phi^2/sqrt2) in 8 caps. All five at one scale (each fills
  the same cell). The front half of each setting (pieces whose centre lies in front of the cell's centre) is left off so the stone
  shows. Layout 2 over 3 in D·I·C·T·O order: the largest equal size that fits (cell box 740 px against about 430 in a row of five).
- One gold for every setting piece: the series gold deepened a little (204, 152, 44) so the yellow octahedron stays distinct;
  gold edges dark, stone edges light (as Chapter 10's figures).
- Lettering as the series: the series line of front.html above the title (as Golden Cycle and Star Cores); subtitle shortened to
  one line: "Inside the Five, Filling Space & Where They Live" (front.html: "Inside the five, the five filling space, and where
  the five live", too long for one line at the series size).
- Exact checks first (scripts/cover.py, 27 X PASS): cell volume (15 + 7 sqrt5)/4; for each jewel stone + setting = cell by exact
  volume, gold share = Table 10.2, stone edge, every corner inside the cell, piece counts.

Files: scripts/cover.py (pieces from studies/2026-11-14-platonic-hybrid golden.py / hybrid.py through
studies/2026-11-15-filigree/scripts/jewels_lib.py; painting, layout and lettering after studies/2026-11-15-paradigm-cover);
scripts/ledtext.py (copy, plus the middle dot and the kanji of the series line); platonic-cover-front-series.png (2400 x 3394);
platonic-dicto-mark-back.png (back mark, as Space-Fillers and Paradigm). Run on the compute host through the job gate
(pilots platcover-pilot, platcover-pilot2; final platcover, FINAL ok).
