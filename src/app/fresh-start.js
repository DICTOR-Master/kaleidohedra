// A fresh start (DICTO's rule, app audit 2026-10-22): entering a world whose store holds a saved build asks first, "Continue where
// you left off" or "Start fresh" (render.js askFreshStart). These are its pure parts, kept apart so the unit tests can run them.

const LISTS = ['cells', 'pieces', 'tiles', 'nodes'];
/** A store's build, for comparing with its untouched state: without the names, dates and versions a store carries. */
export const buildOf = (json) => JSON.stringify(json, (k, v) => (['lastModified', 'createdAt', 'meta', 'worldName', 'version'].includes(k) ? undefined : v));
/** A lattice-style store whose piece lists are all empty holds nothing (no need to compare it). */
export const listsEmpty = (j) => !!j && LISTS.some((k) => k in j) && LISTS.every((k) => !(k in j) || Object.keys(j[k] ?? {}).length === 0);
/** Two worlds that show the same stores are one space (the 3D lattices share theirs): moving between them asks nothing. */
export const sameStores = (a, b) => !!a && !!b && a.length > 0 && a.length === b.length && a.every((k) => b.includes(k));
/** Entry routes that ask about replacing a build themselves (the Polyhedraverse kits and polytopes). */
export const asksItself = (action) => /^tool:(polyKit|polytope):/.test(action ?? '');
