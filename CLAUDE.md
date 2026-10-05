# CLAUDE.md

Guidance for Claude Code (and other agents) working in this repository.
It describes the app as it is now. For how it got here, use `git log`;
nothing in this file is history.

## What this project is

Kaleidohedra is the third sibling of
[Rhombiverse](https://github.com/DICTOR-Master/rhombiverse) and
[Polyhedraverse](https://github.com/DICTOR-Master/polyhedraverse):
lattices you can shear and slide continuously, where every piece of
geometry moves with the lattice as one slider moves it along an exact
space-filling path (see `PLAN.md`), rather than Rhombiverse's one piece
at a time on a fixed lattice. Chosen states ("population members") are
exported to the two sibling apps — as a lattice world in Rhombiverse, as
pieces in Polyhedraverse.

It grew from shapes DICTO found in Zometool — a golden leaning hexagonal
prism and a skewed rhombic dodecahedron that tiles as a sheared FCC (see
`DISCOVERIES.md` and Polyhedraverse's
`docs/dicto-zometool-discoveries.md`) — and goes on from there, no
longer tied to Zometool.

GitHub: https://github.com/DICTOR-Master/kaleidohedra (`gh` is authenticated).

The 3D engine (`index.html`, `src/`, `data/`) is forked from
Rhombiverse's own code (FCC world, lattice view, saving), so building
stays exactly as in Rhombiverse while Kaleidohedra's own controls (the
shear slider, "towards…" picker, Export of population members) are
layered on top. See `PLAN.md`'s "Build order" for what stage that is at
— until noted otherwise there, titles, meta tags and in-app copy on the
forked engine files still describe Rhombiverse and haven't been
rebranded yet; don't assume they describe Kaleidohedra-specific
behavior.

## Scope guardrails

Same discipline as Rhombiverse — pure, deterministic geometry. Do not
add, even partially, without an explicit decision from the user:

- simulation of any kind: physics, gravity, growth, evolution, anything
  that changes over elapsed time rather than on user action;
- game systems: mining, inventory, trade, claims, avatars, walking;
- shared or networked state: multiplayer, sync, accounts, backends, AI calls;
- bulk-building tools (fill, dig, smooth, shells, repeat, sculpt). One
  piece at a time is the design.

`scripts/stale-terms.json` lists the retired vocabulary. `npm run
verify:copy` (in CI) fails if any of it reaches user-visible text.

UI rule: hide controls that don't apply; don't grey them out.

## Layout

See README.md for the top-level files. Kaleidohedra's own work:
`DISCOVERIES.md` (findings and how each is verified), `TARGETS.md` +
`geometry-targets.json` (the 160-cell target list, from `discover.py` /
`discover_run.py`), `enumerate.py` + `targets.json` (the earlier,
smaller list), `PLAN.md` (the current design), `assets/brand/` (the
logo). The forked engine: `index.html` (the app), `src/render.js`
(scene, render loop, most UI wiring), `src/core/` (lattice math,
placement/removal input in `build.js`, world state, persistence),
`src/app/` (wheels, Wizard, 4D and 5D/6D worlds, Almanac, settings,
i18n, welcome, guide, language picker), `src/geometry-extensions/`
(every lattice beyond FCC), `data/` (starter world, changelog),
`docs/guide*.md` (the user guide) — all inherited from Rhombiverse, not
yet diverged for Kaleidohedra's own slider/export model.

## Running and checking

- **Dev:** no build step. `python3 -m http.server 8000` in the repo root;
  plain ES modules with an import map, Three.js from a CDN.
- **Production:** Vercel runs `npm run build` (`scripts/build.mjs`):
  esbuild minifies each file in place into `dist/` (no bundling, same
  module graph) and copies the static files listed there. A new
  top-level static file must be added to that list.
- **Unit tests:** `node --test tests/unit/` (CI uses Node 20; on Node 22
  pass the files, `node --test tests/unit/*.test.mjs`).
- **Browser smoke test:** `tests/browser/smoke.mjs` against a served
  copy, raw source and `dist/` both, in CI.
- **Checks:** `npm run verify:i18n | verify:rhombis-i18n | verify:copy |
  verify:lattice-2d | verify:pyrochlore | verify:rhombohedra | verify:4d |
  verify:quasicrystal | verify:catalogue | verify:kaleido | verify:shells |
  verify:kaleidoscope | verify:trajectory | verify:construction |
  verify:nets | verify:packing | verify:dicto-fcc`.
- **Browser automation:** run Playwright on `dicto-node` (192.168.0.7,
  SSH), not the dev Pi. Sync first, with `--delete` for tests. Headless
  Chromium there can starve timers, so hold simulated long-presses 1.5 s+.
- After every push, check CI (`gh run list -L 1`) and fix a red run.

## Conventions that matter

- **The world is data.** Each lattice has its own JSON store, keyed
  `"x,y,z"`. FCC cells are integer `(x, y, z)` with `x + y + z` even;
  the 12 neighbour offsets are the `(±1, ±1, 0)` permutations
  (`src/core/lattice.js`). Other lattices use their own frames
  (see each `geometry-extensions/*.js` header).
- **Every store change goes through `persist()`** (render.js). That is
  what records undo history (per dimension, ↶ bottom right). A new store
  must also be registered in `registerHistoryStores()`, which makes it
  part of undo and of Export/Import World (a `world-bundle` of every
  registered store).
- **i18n:** 7 languages (`src/app/i18n.js`, `LANG_ORDER`). Tag static
  text with `data-i18n` / `data-i18n-html` / `data-i18n-title` so
  `applyTranslations()` re-translates it live on a language change; call
  `t(key, lang)` for dynamic text. Every key needs all 7 languages
  (`verify:i18n`). Language is one setting (`updateSettings({ language })`),
  shared by Settings and the 🌐 picker (`src/app/language-picker.js`).
- **What's New** (`data/changelog.json`): user-facing features only,
  newest first, added in the same push. No entries for fixes to things
  that should already have worked.
- **Touch first.** Every interaction must work by touch on iPhone/iPad.
  Long-press is 500 ms (`build.js`), with a guard against the click that
  iOS synthesizes afterwards. Mouse-only tests don't prove touch works.
- **Every geometric claim is checked numerically**, not by eye — see
  `scripts/verify-kaleido.mjs` and the `DISCOVERIES.md` table of which
  script backs which finding.
- **Removing a feature means deleting it**: code, UI, strings, tests,
  docs. Git history is the archive. Don't leave comments that narrate
  what used to be there.
- **Design law** (`docs/KALEIDOHEDRA_PRINCIPLES.md`): prefer real,
  established geometry over anything invented, and the simplest version
  that works.
