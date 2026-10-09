# Tests

Two independent suites, matching the two harnesses described in
`.claude/skills/browser-test-harness/SKILL.md` (this is their permanent,
committed form; that skill's harnesses were always throwaway/local).

## Unit tests (`unit/`)

Pure math/logic (`src/lattice.js`, `src/worldstate.js`, `src/regions.js`)
— none of these import `three` or touch the DOM. Zero npm dependencies;
`src/package.json`'s `"type": "module"` is the only thing needed so plain
Node treats `src/*.js` as ESM (deliberately scoped to `src/`, not the
repo root, so it can never affect how Vercel detects/builds this
project — still zero build step for the app itself).

```
node --test tests/unit/
```

## Browser smoke test (`browser/`)

A real Playwright browser driving the actual app — the one thing the
unit tests can't cover (rendering, real clicks, DOM state). Needs the
app served locally first, exactly as this repo's own `README.md`
describes:

```
python3 -m http.server 8000 &
cd tests/browser && npm install && npx playwright install chromium
node smoke.mjs
```

Both run automatically on every push/PR via `.github/workflows/ci.yml`.

## Polyhedraverse's browser tests (`browser/poly/`)

The old Polyhedraverse site's 23 Playwright specs, ported to the joined app in step D6: one
`*.spec.mjs` per old spec, testing the same intent through the joined app's controls (tap attach,
More…, long-press, Undo, Settings, DICTO). They open the Polyhedraverse door on a phone-sized touch
screen with `?probe`, a read-only hook (render.js) that says where a piece's faces and corners are on
screen, so taps land on the real canvas; long-press is a real held touch.

```
python3 -m http.server 8000 &
cd tests/browser && node poly/run.mjs        # ONLY=<file or title part> runs some
```

CI runs them against the built Polyhedraverse door (`SITE=polyhedraverse`).

