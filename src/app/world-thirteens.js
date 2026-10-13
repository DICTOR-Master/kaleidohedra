// The 13s (DICTO 2026-10-13, docs/PLAN-13.md): twelve around one, seven ways, each with its kits as views, on the shared
// layered-world engine (Pull apart, Top shell, Crystal). Data: src/app/thirteens-data.js, built and checked by
// scripts/build-thirteens-data.py. Words: i18n thirteens.*; DICTO's names stay untranslated.
import DATA from './thirteens-data.js';
import { createLayeredWorld } from './world-chains.js';

const KINDS = ['icosa13', 'dodeca13', 'bodhi', 'unity', 'dictoStar', 'deshi', 'rd13', 'hexed', 'to13'];
// Crystal: the twelve and their centre turn see-through, so what fills between them shows.
const GLASS = {
  icosa13: new Set(['ico', 'dodeca', 'j11']), dodeca13: new Set(['dodeca', 'centre']), bodhi: new Set(['copy']), unity: new Set(['j11']),
  dictoStar: new Set(['dodeca', 'centre']), deshi: new Set(['ico']), hexed: new Set(['hexByHex', 'hexByRhombus', 'hexByHexN', 'hexByRhombusN', 'hexCentreN']),
  to13: new Set(['toByHex', 'toBySquare', 'toByHexN', 'toBySquareN', 'toCentreN']), rd13: new Set(['rd', 'rdA', 'rdB', 'rdAN', 'rdBN', 'rdCentreN']),
};

export function createThirteensWorld({ scene, fitView }) {
  return createLayeredWorld({ scene, fitView, name: 'thirteens', data: DATA, kinds: KINDS, glassRoles: GLASS, prefix: 'thirteens',
    defaultParts: { icosa13: 'pieces', dodeca13: 'pieces', bodhi: 'seed', unity: 'open', dictoStar: 'star', deshi: 'deshi', rd13: 'plain', hexed: 'cluster', to13: 'cluster' }, centreGold: true });
}

/** Points whose convex hull previews a 13 in the DICTO menu (its first view). */
export function thirteensPreviewPoints(kind) {
  const views = DATA[kind]?.views;
  return views ? Object.values(views)[0].flatMap((p) => p[1]) : [];
}
