// The world menu by the books (DICTO 2026-11-17, "build it": the apps were still a jumble). Every DICTO world once, under its home
// book, the books in series order (The Five Orders of Space, Books One to Eleven; a book with no world of its own is not listed);
// inside a book, paper order. After the books: one shelf of others' lattices and tilings, by their regular names and discoverers,
// then the studies and tools. The same order through every door. Pure data (no DOM), so the unit tests read it as the menu does.
// Book titles and world names are names, so they stay as written in every language.

// Each world: key = the world's key in the wizard's lists (K_WORLDS / LATTICES_3D) or one of EXTRA_WORLDS below; papers = its papers.
export const BOOKS = [
  { id: 'One', title: 'Quanta of Space I and II', cover: 'quanta', worlds: [['dodeca', '#13, #14'], ['breathing', '#20'], ['bodhiPyro', '#30, #31, #36'], ['ocdStella', '#31a'], ['octetTruss', '#37, #37a, #40'], ['icosa', '']] },
  { id: 'Two', title: 'Space-Fillers and Lattice Moves', cover: 'space-fillers', worlds: [['stellaJewel', '#17, #18, #41'], ['thirteens', '#19, #25, #26'], ['sunstar', '#42'], ['octet', '#48'], ['octetBuild', ''], ['dictofcc', ''], ['dictohex', '']] },
  { id: 'Three', title: 'DICTONIC Bonds', cover: 'dictonic-bonds', worlds: [['dictonic', '#51, #52'], ['globalWeb', '#53'], ['bloom', '#59']] },
  { id: 'Four', title: 'The Golden Cycle', cover: 'golden-cycle', worlds: [['chains', '#22, #23, #24'], ['cycles', '#27, #28'], ['kpFilm', '#27'], ['theaetetus', '#29'], ['doubleVision', '#32, #33'], ['vajrayana', '#34, #34a, #35, #35a, #35b'], ['up', '#38, #38a, #39'], ['upFilm', '#38']] },
  { id: 'Five', title: 'Star Cores', cover: 'star-cores', worlds: [['starCores', '#79, #80, #81']] },
  { id: 'Six', title: 'HexOct', cover: 'hexoct', worlds: [['stackings', '#57, #58, #66, #68, #70–#74'], ['hexoct', '#75, #83'], ['hexoctKit', '#86']] },
  { id: 'Seven', title: 'The Permutohedron Paradigm', cover: 'permutohedron-paradigm', worlds: [['bitrunc', '#76, #104, #107'], ['perm4', '#105']] },
  { id: 'Eight', title: 'The Platonic Solids', cover: 'platonic-solids', worlds: [['roofFold', '#8'], ['aristotle', '#44, #77, #92'], ['reuleaux', '#45'], ['platonicMix', '#47, #106']] },
  { id: 'Nine', title: 'The Golden Ladder', cover: 'golden-ladder', worlds: [] },
  { id: 'Ten', title: 'Alicia in Wonderland', cover: 'alicia', worlds: [['whiteQueen', '#63, #65, #76'], ['queensWalls', '#107, #109, #110']] },
  { id: 'Eleven', title: 'A Brief Geometry of Space', cover: null, worlds: [] },
];

// Worlds reached from inside other worlds or pages until now, listed in their books too: label, action, and the app they open in
// (null = the door's own, as DICTO's worlds do).
export const EXTRA_WORLDS = {
  upFilm: { label: 'Universal PiTet film', action: 'tool:upFilmWorld', app: 'kaleidohedra' },
  kpFilm: { label: 'Kepler–Poinsot–UP film', action: 'tool:kpFilmWorld', app: 'kaleidohedra' },
  hexoctKit: { label: 'HexOct kit', action: 'tool:hexoctKit', app: 'polyhedraverse' },
  // DICTO's leaning hexagonal prism, a piece of Rhombiverse's hexagonal lattice, always opened there.
  dictohex: { label: 'DICTO Hex Prism', action: 'tool:pieceType:dictohex', app: 'rhombiverse', tip: 'wiz.3d.hexDicto' },
};

// Others' lattices and tilings: name (with discoverer and year where known) and the lattice or world it opens (`lat`: a LATTICES_3D
// key, its pieces listed under it; `world`: a K_WORLDS key; `dim`: a dimension screen).
export const OTHERS_SHELF = [
  { id: 'fcc', name: 'FCC (face-centred cubic)', lat: 'fcc' },
  { id: 'bcc', name: 'BCC (body-centred cubic)', lat: 'bcc' },
  { id: 'bccGaps', name: 'BCC interstitial', lat: 'bccGaps' },
  { id: 'rdDual', name: 'RD dual: cuboctahedra and octahedra', lat: 'rdDual' },
  { id: 'ed', name: 'Elongated dodecahedra (Fedorov, 1885)', lat: 'ed' },
  { id: 'hex', name: 'Hexagonal prisms', lat: 'hex' },
  { id: 'rhombohedral', name: 'Rhombohedral', lat: 'rhombohedral' },
  { id: 'hcp', name: 'HCP: trapezo-rhombic dodecahedra', lat: 'hcp' },
  { id: 'gyro', name: 'Gyrated octet', lat: 'gyro' },
  { id: 'triprism', name: 'Triangular prisms', lat: 'triprism' },
  { id: 'pyrochlore', name: 'Pyrochlore', lat: 'pyrochlore' },
  { id: 'golden', name: 'Golden rhombohedra: 3D Penrose tiling (Ammann, 1976; Kramer, 1982)', world: 'golden' },
  { id: 'gperm', name: 'Generalized permutohedra (Postnikov, 2009)', world: 'gperm' },
  { id: 'polytopes', name: 'Polytopes in 4D, 5D, 6D', dims: ['4D', '5D', '6D'] },
];

// Studies and tools: `world` a K_WORLDS key; `family` the 1D/2D families (by id) with their dimension; `open` a page of the app;
// `href` a page of its own beside the app (in every door; DICTO 2026-11-21: Amber cells and Aequi first, new work at the top).
export const TOOLS_SHELF = [
  { id: 'amber', href: '/amber/', label: 'wiz.books.amber', sub: 'wiz.books.amberSub', glyph: '⬢', thumb: 'amber' },
  { id: 'aequi', href: '/aequi/', label: 'wiz.books.aequi', sub: 'wiz.books.aequiSub', glyph: '⚀', thumb: 'aequi' },
  { id: 'studies', world: 'studies' },
  { id: 'targets', world: 'targets' },
  { id: 'shells', world: 'shells' },
  { id: 'construct', name: 'Construct', dim: '1D', families: ['construct', 'constructKagome', 'constructRd'] },
  { id: 'kaleido', name: 'Kaleidoscope', dim: '2D', families: ['kaleido'] },
  { id: 'nets', name: 'Nets', dim: '2D', families: ['nets'] },
  { id: 'signal', name: 'Signal', dim: '1D', families: ['signal'] },
  { id: 'mandala', world: 'mandala' },
  { id: 'almanac', open: 'almanac' },
  { id: 'guide', open: 'guide' },
];

// Every world key of the books, in menu order.
export const bookWorldKeys = () => BOOKS.flatMap((b) => b.worlds.map(([k]) => k));

// A world's paper list as numbers: '#57, #58, #70–#74' -> ['57', '58', '70', '71', '72', '73', '74'] (for its paper chips).
export function paperNumbers(s) {
  const out = [];
  for (const part of String(s ?? '').split(',')) {
    const m = part.trim().match(/^#(\d+)([a-z]?)(?:\s*[–-]\s*#?(\d+))?$/);
    if (!m) continue;
    if (m[3]) for (let i = Number(m[1]); i <= Number(m[3]); i++) out.push(String(i));
    else out.push(m[1] + m[2]);
  }
  return out;
}
