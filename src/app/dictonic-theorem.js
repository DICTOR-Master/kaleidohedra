// DICTONIC's theorem, shown with its evidence (DICTO 2026-10-25: "a presentation of a geometric theorem", not a demonstration):
// (1) the statement on a card, a tap opens why it holds and where it is proved; (2) a live chart of the exact bond sizes along
// the slider, the key points marked and a marker riding with the slider; (3) the bonds of each piece; (4) for the Delian bond,
// the switch at the octet drawn in the dual picture: one rhombus trading its long diagonal (oct–oct) for its short one (tet–tet).
// Exact formulas: study 2026-10-25-bond-relay (371 checks), app units (golden L = φ, Delian octet edge 1). Words: i18n dictonic.thm.*.
import { t } from './i18n.js';
import { mountTheoremSheet, switchPicture } from './theorem-sheet.js';

const PHI = (1 + Math.sqrt(5)) / 2, P2 = PHI * PHI, S3 = Math.sqrt(3);
/** Exact bond areas (one shared face of each kind) at the slider value. */
export const BOND_AREAS = {
  golden: (x) => (x === Infinity
    ? { bb: P2 / 2, ss: 0, bs: (S3 / 8) * P2 }
    : { bb: (P2 * x * x) / (2 * (1 + x) ** 2), ss: P2 / (2 * (1 + x) ** 2), bs: ((S3 / 8) * P2 * (x * x + 4 * x + 1)) / (1 + x) ** 2 }),
  delian: (tt) => ({
    oo: tt < 1 / 3 ? (Math.SQRT2 / 4) * (1 - 9 * tt * tt) : 0,
    ot: tt <= 0 || tt >= 1 ? 0 : tt <= 1 / 3 ? ((9 * S3) / 4) * tt * tt : ((9 * S3) / 16) * (1 - tt) ** 2,
    tt: tt > 1 / 3 ? ((3 * tt - 1) * (5 - 3 * tt)) / 8 : 0,
  }),
};
const CURVES = { golden: [['bb', '#ffc857'], ['ss', '#7fd3ff'], ['bs', '#ff8a5c']], delian: [['oo', '#9d8cff'], ['ot', '#ff8a5c'], ['tt', '#ffc857']] };
const MARKS = { golden: ['kelvin', 'tau'], delian: ['octet', 'bond'] };
/** Bonds of each piece (study: coordination numbers), as words. */
function countLine(kind, v, L) {
  if (kind === 'golden') return t(v === 0 ? 'dictonic.thm.count.golden.zero' : v === Infinity ? 'dictonic.thm.count.golden.inf' : 'dictonic.thm.count.golden', L);
  const o = v === 0 ? 12 : v < 1 / 3 ? 20 : v < 1 ? 8 : null, k = v === 0 ? null : v <= 1 / 3 ? 4 : v < 1 ? 10 : 6;
  return t('dictonic.thm.count.delian', L, { o: o ?? '—', t: k ?? '—' });
}

// The sheet itself is the shared theorem sheet (theorem-sheet.js); DICTONIC gives it its two loops as data.
const tk = (key) => (L) => t(key, L);
const NETWORKS = Object.fromEntries(Object.keys(CURVES).map((kind) => [kind, {
  areas: BOND_AREAS[kind], curves: CURVES[kind], marks: MARKS[kind], statement: tk(`dictonic.thm.${kind}`), detail: tk('dictonic.thm.detail'),
  chart: tk('dictonic.thm.chart'), bond: (key, L) => t(`dictonic.thm.bond.${key}`, L), mark: (k, L) => t(`dictonic.thm.mark.${k}`, L), count: (v, L) => countLine(kind, v, L),
  // (4) the switch, Delian only: before the octet the rhombus's long diagonal (oct–oct) is a bond, after it the short one (tet–tet);
  // oct sites at the ends of the long diagonal (length √2), tet sites at the short one (length 1)
  flip: kind !== 'delian' ? null : {
    svg: (v) => switchPicture({ a: 38, b: 38 / Math.SQRT2, cols: ['#9d8cff', '#ffc857'], before: v < 1 / 3 && v > 0, after: v > 1 / 3 && v < 1 }),
    now: (v, paused) => !!paused || Math.abs(v - 1 / 3) < 1e-9, label: tk('dictonic.thm.flip'),
  },
}]));
const WORDS = { more: tk('dictonic.thm.more'), less: tk('dictonic.thm.less'), almanac: tk('dictonic.thm.almanac'), title: tk('dictonic.thm.almanac.title'), entry: tk('dictonic.thm.almanac.entry') };

export function mountTheorem(panel, { stopsOf, valueAt, openAction = () => {} }) {
  return mountTheoremSheet(panel, { networks: NETWORKS, words: WORDS, entryAction: 'openAlmanac:dicto:dictonic', stopsOf, valueAt, openAction });
}
