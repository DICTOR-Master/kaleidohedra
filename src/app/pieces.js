// The pieces the Almanac lists, and their icons (moved here from the retired wheel's config,
// DICTO 2026-10-08: the wheels are gone; the DICTO wizard is the one place pieces are chosen).
// Faces keep their old slot keys only as stable ids.

// === 2. VISUAL SYSTEM (validated, user-approved) =======================
// Single wire color across the whole RD -- matches the existing `home`
// classDef stroke from the flow chart, so it's consistent with graphics
// already established elsewhere in the project, not a new invented
// color. Spare/reserved faces differ only by dash pattern, never color.
export const SKELETON_COLOR = "#4DD0E1";

// Piece (added 2026-08-28, replacing the separate piece-cluster-3d.js
// widget -- see WHEEL_BUILD's own comment above for the full reasoning).
// Originally exactly 6 real piece tiers filled the 6 available
// non-reserved, non-universal slots (4 equator + 3 bottom) with no
// SPARE or duplicate needed. 2026-08-29: Cuboctahedron Build (a real,
// separate persistent-World system, same shape as BCC Build -- see
// core/cubocta-build.js) needed a 7th seat and this wheel was already
// completely full, so "Lenses" was dropped from the shared universal
// ring entirely (direct instruction: "lenses are amply catered for now
// so can come off universal ring" -- X-Ray/Lenses is already reachable
// via the corner HUD wheel and the Lab panel). That freed top|sy1sz1.
//
// 2026-08-29 SAME-DAY FIX, real bug caught live: top|sy1sz1 (along with
// equator|sx1sy1 and top|sx1sz1) is one of only THREE faces visible/
// clickable at every wheel's default opening rotation (confirmed live:
// every other face sits at opacity 0 / pointer-events:none until the
// player rotates) -- true structurally for every wheel, which is
// exactly why this slot always held the low-consequence universal
// "Lenses" before. Putting Cuboctahedron Build there instead meant an
// early, un-rotated tap near the top of a freshly-opened Piece wheel
// silently switched the whole app into a different BUILD MODE (not
// just a different piece-type selection) -- every subsequent World
// click then routed to Cuboctahedron Build instead of the intended
// piece placement, which is what actually broke Material/Cube/
// Disphenoid taps ("dispenses cuboctahedra"/"cube placement
// interfering"/"disphenoid wont place" were all downstream symptoms of
// the SAME accidental mode-switch, not three separate bugs). Fixed by
// swapping Cuboctahedron and Material's positions: Material (a
// terminal, non-mode-switching action, closes cleanly back to the
// normal Add flow) now sits at the always-visible top|sy1sz1 -- an
// improvement on the original "close together" request, since it's
// reachable with zero rotation -- and Cuboctahedron Build (a real mode
// switch, same category as BCC Build) moved to bottom|sx-1sz-1,
// requiring a deliberate rotation first, same as BCC Build's own
// placement on Home (bottom|sx-1sz-1 there too, since 2026-09-02).
export const WHEEL_PIECE = {
  id: "piece",
  faces: {
    // RD's own true original face was a direct "tool:pieceType:rd"
    // terminal through 2026-09-05 -- changed to a doorway into its own
    // sub-wheel (WHEEL_RD_FAMILY below), direct user decision 2026-09-06,
    // made right at the moment two new RD-derived pieces (Hemi RD,
    // Hourglass, ported from Rhombis) needed a home: WHEEL_PIECE itself
    // was found to be completely full (all 12 slots -- 8 real + the 4
    // universal-ring ones every wheel structurally can't touch -- already
    // spoken for), so cramming new top-level piece types in here would
    // have meant evicting something real. A sub-wheel gives the RD family
    // room to grow (this user: "I have some more ideas for piece
    // variety") without reopening WHEEL_PIECE's own already-settled layout.
    "equator|sx1sy1":   { kind: "dept", label: "RD Family", action: "navigateTo:rdFamily", desc: "RD and its real derived pieces -- Hemi RD, Hourglass, and more." },
    "equator|sx1sy-1":  { kind: "dept", label: "Cube", action: "tool:pieceType:cube", desc: "A bare block, no pyramids -- build up from here with the Pyramid tier." },
    "equator|sx-1sy1":  { kind: "dept", label: "Pyramid", action: "tool:pieceType:pyramid", desc: "Add or remove one pyramid on an already-placed cell." },
    "equator|sx-1sy-1": { kind: "dept", label: "TO", action: "tool:pieceType:to", desc: "Truncated Octahedron -- the BCC lattice's own real space-filling cell." },
    "bottom|sy1sz-1":   { kind: "dept", label: "Flattened Octahedron", action: "tool:pieceType:ioct", desc: "BCC interstitial lattice: places the 4-disphenoid bundle a flattened octahedron combines into." },
    "bottom|sx1sz-1":   { kind: "dept", label: "Disphenoid", action: "tool:pieceType:idis", desc: "BCC interstitial lattice: one tetragonal disphenoid at a time." },
    // Cuboctahedron Build: not a "tool:pieceType:*" terminal like its
    // siblings -- it's its own click-to-place/grow mode (like BCC Build
    // on WHEEL_RHOMBISIS), so it uses the matching "tool:cuboctaBuild"
    // action instead. Deliberately NOT on the always-visible top ring --
    // see this wheel's own header comment above. Label shortened to "CO"
    // 2026-08-29, direct instruction ("just say CO like RD does") --
    // matches this wheel's own existing abbreviation convention (RD,
    // TO), the full word still appears in desc below and the detail
    // panel that opens on selection.
    "bottom|sx-1sz-1":  { kind: "dept", label: "CO", action: "tool:cuboctaBuild",
      desc: "Cuboctahedron -- place cells on the RD lattice's dual, vertex-pointed cuboctahedra, alongside your normal World (Rhombeometry only)." },
    // Material lived here 2026-08-29 through 2026-08-31 (direct request
    // to pick shape and Material "close together"), then was removed --
    // direct follow-up feedback: a real color swatch among this wheel's
    // own monochrome marks was a genuine visual outlier, and picking any
    // Piece face now opens the material-swatch overlay directly instead
    // (see the tool:pieceType:* handler in render.js), so a dedicated
    // face here was redundant besides. Material's still reachable at
    // WHEEL_BUILD's own equator and the bottom-left HUD color icon,
    // unchanged. This freed the always-visible top|sy1sz1 slot (see this
    // wheel's own header comment) for the Cuboctahedron gap-fill
    // Octahedron -- a genuinely new piece, kept distinct from the old
    // "Octahedron Site" 4-disphenoid bundle above rather than replacing
    // it, direct user decision 2026-08-31.
    "top|sy1sz1":       { kind: "dept", label: "Octahedron", action: "tool:pieceType:octahedron",
      desc: "Fills the gap between cuboctahedra face to face -- click near a Cuboctahedron's own corner." },
  }
};

// RD family: reached via WHEEL_PIECE's own "RD" face (navigateTo:rdFamily,
// see that face's own header comment for why this exists as a sub-wheel
// rather than more WHEEL_PIECE faces). Hemi RD/Hourglass/the two cluster
// stamps below all ported from Rhombis 2026-09-06 (src/rhombis/stages.js's
// Hourglass/Hourglass Chain stages and Multi-Cell's hubcap-cluster idea,
// krp-core/src/core/lattice.js's hemisphereSplit -- see core/hemisphere-build.js for
// the real store/key/cluster-group scheme).
//
// Real same-day bug, direct report: this wheel's first draft only
// declared 3 of its 12 addressable faces, leaving top|sy1sz1 undeclared --
// one of only 3 faces visible at a fresh wheel's default opening rotation
// (equator|sx1sy1, top|sx1sz1, top|sy1sz1, same fact every OTHER wheel's
// own header comment already documents), so this wheel broke the
// established "never open onto a mostly-blank wheel" rule every sibling
// wheel deliberately upholds by filling that exact slot with real
// content. Fixed by giving the cluster-stamp pieces (hemi3/hemi4,
// added the same session once the earlier "12-cluster" idea was dropped
// as redundant with 'to' -- see core/hemisphere-build.js's own header)
// real homes, one of them AT top|sy1sz1 specifically. Two more clusters
// (hemiTri Triangle Cluster, hemiRing Triangle Ring) filled the remaining
// bottom-ring slots later the same session. The 1 remaining slot is
// explicit SPARE (not just left undeclared) -- this user flagged "more
// ideas for piece variety" the same session this wheel was created, so
// real room is kept for future RD-derived pieces, just never as an
// accidentally-blank face again.
// Trimmed 2026-09-22, direct instruction ("remove some RD pieces, just
// keeping RD-Hemi and RD-Hourglass"): the 4 cluster stamps (Corner/Band/
// Triangle Cluster, Triangle Ring) are cut from this wheel -- their
// underlying core/hemisphere-build.js math and core/build.js click
// handling are untouched, just no longer reachable via this face or the
// Piece picker (archived-in-place, per this repo's own "archive, don't
// delete" convention, not removed from the codebase).
export const WHEEL_RD_FAMILY = {
  id: "rdFamily",
  faces: {
    "equator|sx1sy1":   { kind: "dept", label: "RD", action: "tool:pieceType:rd", desc: "A full block -- cube plus all 6 pyramids." },
    "equator|sx1sy-1":  { kind: "dept", label: "Hemi RD", action: "tool:pieceType:halfrd",
      desc: "One real hemisphereSplit() half of an RD -- click an existing face to add the neighbor's near half." },
    "equator|sx-1sy1":  { kind: "dept", label: "Hourglass", action: "tool:pieceType:hourglass",
      desc: "Two matching hemisphere halves bridging a cell and its neighbor -- click an existing face to add one across that boundary." },
    // Not strictly "RD family" (Elongated Dodecahedron/Hex Prism are 2
    // of the OTHER real parallelohedra, unrelated to RD's own
    // decomposition) -- placed here anyway, direct pragmatic call:
    // WHEEL_PIECE itself has zero spare slots (see its own header
    // comment -- "completely full" already before these 3 existed), and
    // this sub-wheel is the only one with real room. RD Quarter IS a
    // genuine RD-family piece (one of RD's own 4 real rhombohedra).
    "equator|sx-1sy-1": { kind: "dept", label: "RD Quarter", action: "tool:pieceType:rdquarter",
      desc: "One of RD's own 4 real rhombohedra (Fedorov's zonotope decomposition) -- tap an RD near a corner to fill it in; tap a quarter's face to place its mirror image there." },
    // "ED", not the full name -- direct instruction 2026-09-23, matching
    // this wheel's own existing abbreviation convention (RD, TO, CO):
    // "Elongated Dodecahedron" was the one long label left on this
    // wheel, long enough to visually crowd/overlap its neighboring
    // faces' own label area.
    "top|sy1sz1":       { kind: "dept", label: "ED", action: "tool:pieceType:elongdodeca",
      desc: "Elongated Dodecahedron -- the 4th of the real \"5\" parallelohedra -- its own lattice, same FCC positions, anisotropic scale." },
    "bottom|sy1sz-1":   { kind: "dept", label: "Hex Prism", action: "tool:pieceType:hexprism",
      desc: "The 5th real parallelohedron -- its own separate hexagonal lattice." },
    // Rhombohedra (free lattice): direct follow-up, same session as RD
    // Quarter -- "need placement of rhombohedra not limited to fill
    // existing RDs, rhombohedra should be able to fulfil their own
    // geometry free connecting in all directions... call them
    // rhombohedra too." Genuinely the SAME real shape as one of RD
    // Quarter's own 4 congruent orientations (geometry-extensions/
    // rhombohedra-lattice.js reuses rdQuarterPieces(s)[0] directly),
    // just growing freely through open space via its own 6 real face
    // directions instead of only appearing pre-packed inside an
    // already-solid RD -- see that file's own header for why RD
    // Quarter itself can't be freely placed/removed once bootstrapped
    // into an already-solid cell (its own volume becomes fully
    // enclosed, unclickable from outside).
    "bottom|sx1sz-1":   { kind: "dept", label: "Rhombohedra", action: "tool:pieceType:rhombohedra",
      desc: "The same real rhombohedron as RD Quarter, but its own free-standing lattice -- click an existing face to add the next one, in any of 6 real directions." },
    // Pyrochlore (3D Kagome) -- direct request 2026-09-24, placed in
    // this wheel's one remaining spare slot (direct decision). Not RD-
    // family either, but registered to the RD world's own FCC frame:
    // one up-tetrahedron inside every RD, truncated-tetrahedron voids in
    // its real holes -- see krp-core/src/geometry-extensions/pyrochlore-lattice.js.
    "bottom|sx-1sz-1":  { kind: "dept", label: "Pyrochlore", action: "tool:pieceType:pyrochlore",
      desc: "Pyrochlore (3D Kagome) -- place truncated tetrahedra; the corner-sharing tetrahedra between them appear on their own." },
  }
};

// Icon System (RHOMBIVERSE_SPEC_ICON_SYSTEM.md): only actions the spec's
// section 4 table (or the live cross-walk's Cyborg resolution) actually
// resolves get a real mark -- every other face keeps its existing plain
// text label exactly as today. Deliberately NOT a guess-to-fill-every-
// face table: the spec explicitly says not to guess silently, and
// several real actions (tool:material, tool:repeat, tool:generateBody,
// and the department-nav faces themselves) have no resolved row.
//
// Lives here (rhombic-wheel-3d-core.js), not rhombic-wheel-3d.js, even
// though it's only ever consumed there for real icon rendering -- moved
// 2026-09-09 so almanac-data.js (a plain data/logic module with zero
// npm dependencies, covered by the pure `node --test tests/unit/` suite
// per tests/README.md) can reuse this same action -> mark mapping
// instead of re-declaring a second copy that could drift out of sync.
// rhombic-wheel-3d.js imports `three` for its own rendering, so ANY
// import from that file (even of a plain object like this one) drags a
// browser-only dependency into that pure-Node test environment, which
// this pure "core" file (already home to WHEEL_PIECE/WHEEL_RD_FAMILY,
// zero imports of its own) never has that problem -- real failure hit
// and fixed while wiring almanac-data.js's Stage 0, not a hypothetical.
// See docs/RHOMBIVERSE_SPEC_ALMANAC.md section 4.
export const ACTION_TO_MARK = {
  // Universal Add/Remove + Piece picker (direct instruction 2026-08-26,
  // retiring the earlier separate Rhombi-/Pyramid-/Cube- model/sculpt
  // marks). 'tool:symmetry' reuses the existing `symmetryMirror` modifier
  // mark below (a real match for what that panel actually does) rather
  // than the old generic "-" now spoken for by 'tool:remove'.
  // Piece: the doorway face (WHEEL_BUILD's own "Piece") shows the
  // clustered-shapes mark as a preview of what's inside, same pattern
  // as navigateTo:build/alter below; each of the 6 real tiers inside
  // WHEEL_PIECE gets its own real shape mark instead (added 2026-08-28,
  // replacing the old bare 'tool:pieceType' -- that action string no
  // longer exists on its own now that Piece is a real wheel, not a
  // picker overlay).
  'navigateTo:piece': 'pieceType',
  // RD's own doorway face reuses its own family's primary mark as a
  // preview of what's inside, same convention as navigateTo:build/alter
  // below.
  'navigateTo:rdFamily': 'pieceRD',
  'tool:pieceType:rd': 'pieceRD',
  // Real 3D-profile marks, added 2026-09-06 -- see wheel-icons.js's own
  // pieceHalfRD/pieceHourglass/pieceHemi3/pieceHemi4 header for the full
  // derivation (real orthographic silhouettes, not hand-drawn).
  'tool:pieceType:halfrd': 'pieceHalfRD',
  'tool:pieceType:hourglass': 'pieceHourglass',
  'tool:pieceType:hemi3': 'pieceHemi3',
  'tool:pieceType:hemi4': 'pieceHemi4',
  'tool:pieceType:hemiTri': 'pieceHemiTri',
  'tool:pieceType:hemiRing': 'pieceHemiRing',
  'tool:pieceType:cube': 'pieceCube',
  'tool:pieceType:pyramid': 'piecePyramid',
  'tool:pieceType:to': 'pieceTO',
  'tool:pieceType:ioct': 'pieceOctaSite',
  'tool:pieceType:octahedron': 'pieceOctahedron',
  'tool:pieceType:idis': 'pieceDisphenoid',
  // Same real gap as PIECE_MARK_KEY's own (render.js) -- every piece
  // added this session was missing here too, leaving these wheel faces
  // with no icon at all (the `markKey && MARKS[markKey]` fallback in
  // rhombic-wheel-3d.js/almanac.js is empty-string, not pieceRD, so this
  // specific gap read as "blank," not "wrong," but still a real gap).
  'tool:pieceType:elongdodeca': 'pieceElongDodeca',
  'tool:pieceType:hexprism': 'pieceHexPrism',
  'tool:pieceType:dictofcc': 'pieceDictoFcc',
  'tool:pieceType:dictohex': 'pieceDictoHex',
  'tool:pieceType:dictoblock': 'pieceRhombohedron',
  'tool:pieceType:rdquarter': 'pieceRDQuarter',
  'tool:pieceType:rhombohedra': 'pieceRhombohedron',
  'tool:pieceType:pyrochlore': 'piecePyrochlore',
  'tool:pieceType:tesseract': 'pieceTesseract',
  'tool:pieceType:cell24': 'piece24Cell',
  'tool:pieceType:cell16': 'piece16Cell',
  'tool:pieceType:a4trunc': 'pieceTrunc5Cell',
  'tool:pieceType:a4bitrunc': 'pieceBitrunc5Cell',
  'tool:pieceType:a4cell5': 'piece5Cell',
  // 2D lattice tier: one entry per lattice-2d.js's own LATTICE_PRIMITIVES
  // (Phase 6: primitive id alone -- angle is a live, in-scene toggle now,
  // not part of the piece-type value at all; see render.js's own
  // lattice2dSeedCell header for the full incident that drove this),
  // spelled out by hand rather than generated -- this file's own header
  // is explicit that it stays at "zero imports of its own" (a real prior
  // failure importing into a file in this same wheel-config layer, see
  // that header), so these ids are kept in sync with lattice-2d.js by
  // hand instead.
  'tool:pieceType:lattice2d:parallelogram': 'piece2dParallelogram',
  'tool:pieceType:lattice2d:triangle': 'piece2dTriangle',
  'tool:pieceType:lattice2d:hexagon': 'piece2dHexagon',
  openAlmanac: 'almanac',
  // 2026-08-26 second pass -- see wheel-icons.js for full design notes
  // on each of these (not in the spec's own table, resolved here).
  'tool:color': 'color',
  // Build's department-nav face reuses its own wheel's primary tool
  // icon -- the face is a doorway into that wheel, so Add doubles as a
  // preview of what's inside. Alter used to do the same with Dig, but
  // got its own real mark (a 6-arrow recycling symbol) 2026-09-02 --
  // direct request, see wheel-icons.js's MARKS.alter for the full
  // design-review history.
  // Universal ring (every wheel): Home.
  navigateHome: 'home',
  // Cuboctahedron Build (Piece, 2026-08-29): reuses the same pinwheel
  // mark Lattice Quick-View already uses for this shape.
  'tool:cuboctaBuild': 'cuboctahedron',
};
