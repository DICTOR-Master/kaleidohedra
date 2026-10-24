// DICTONIC's theorem, shown with its evidence (DICTO 2026-10-25: "a presentation of a geometric theorem", not a demonstration):
// (1) the statement on a card, a tap opens why it holds and where it is proved; (2) a live chart of the exact bond sizes along
// the slider, the key points marked and a marker riding with the slider; (3) the bonds of each piece; (4) for the Delian bond,
// the switch at the octet drawn in the dual picture: one rhombus trading its long diagonal (oct–oct) for its short one (tet–tet).
// Exact formulas: study 2026-10-25-bond-relay (371 checks), app units (golden L = φ, Delian octet edge 1). Words: i18n dictonic.thm.*.
import { t } from './i18n.js';

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

export function mountTheorem(panel, { stopsOf, valueAt }) {
  const box = document.createElement('div');
  box.className = 'w4d-row ch-theorem';
  box.innerHTML = `<div class="thm-card"><p class="thm-statement"></p><button type="button" class="thm-more"></button><p class="thm-detail" hidden></p></div>
    <button type="button" class="thm-evidence-toggle"></button>
    <div class="thm-evidence"><div class="thm-chart"><div class="thm-chart-title"></div><svg viewBox="0 0 320 120" preserveAspectRatio="none" role="img"></svg><div class="thm-legend"></div></div>
    <div class="thm-count" aria-live="polite"></div>
    <div class="thm-flip"><svg viewBox="0 0 120 80"></svg><span class="thm-flip-label"></span></div></div>`;
  const caption = panel.querySelector('.ch-param-caption');
  caption.after(box);
  const more = box.querySelector('.thm-more'), detail = box.querySelector('.thm-detail');
  more.addEventListener('click', () => { detail.hidden = !detail.hidden; box.querySelector('.thm-card').classList.toggle('open', !detail.hidden); update(last); });
  box.querySelector('.thm-statement').addEventListener('click', () => box.querySelector('.thm-card').classList.toggle('open'));
  const svg = box.querySelector('.thm-chart svg'), flip = box.querySelector('.thm-flip');
  // the evidence (chart, bonds per piece, the switch) stands open where the controls are a side column (TV, wide screens) and folds
  // behind a button on upright screens, where it would cover the picture (DICTO's TV/iPad tests, 2026-10-25)
  const evidence = box.querySelector('.thm-evidence'), evToggle = box.querySelector('.thm-evidence-toggle');
  evidence.hidden = !matchMedia('(min-width: 900px) and (max-height: 900px) and (min-aspect-ratio: 4/3)').matches;
  evToggle.addEventListener('click', () => { evidence.hidden = !evidence.hidden; update(last); });
  let last = null, drawnFor = null;
  const W = 320, H = 120, PAD = 6;
  function chart(kind, L) {
    const stops = stopsOf(kind), N = 200, ys = [];
    for (let i = 0; i <= N; i++) ys.push(BOND_AREAS[kind](valueAt(kind, (i * 1000) / N)));
    const top = Math.max(...ys.flatMap((a) => Object.values(a))) * 1.08;
    const X = (u) => PAD + ((W - 2 * PAD) * u) / 1000, Y = (a) => H - PAD - ((H - 2 * PAD) * a) / top;
    const paths = CURVES[kind].map(([key, col]) => `<polyline fill="none" stroke="${col}" stroke-width="2.4" vector-effect="non-scaling-stroke" points="${ys.map((a, i) => `${X((i * 1000) / N).toFixed(1)},${Y(a[key]).toFixed(1)}`).join(' ')}"/>`).join('');
    const marks = MARKS[kind].map((k) => stops.find((s) => s.key === k || (k === 'octet' && s.key === 'octet') || (k === 'bond' && s.key === 'bond'))).filter(Boolean)
      .map((s) => `<line x1="${X(s.u)}" x2="${X(s.u)}" y1="${PAD}" y2="${H - PAD}" stroke="#ffffff55" stroke-dasharray="3 3" vector-effect="non-scaling-stroke"/>`).join('');
    svg.innerHTML = `${marks}${paths}<line class="thm-marker" y1="${PAD}" y2="${H - PAD}" stroke="#fff" stroke-width="2" vector-effect="non-scaling-stroke"/>`;
    box.querySelector('.thm-legend').innerHTML = CURVES[kind].map(([key, col]) => `<span><i style="background:${col}"></i>${t(`dictonic.thm.bond.${key}`, L)}</span>`).join('')
      + `<span class="thm-marks">${MARKS[kind].map((k) => t(`dictonic.thm.mark.${k}`, L)).join(' · ')}</span>`;
    drawnFor = `${kind}.${L}`;
  }
  function update(s) {
    last = s;
    if (!s) return;
    const { kind, u, v, L, paused } = s, on = kind in CURVES;
    box.hidden = !on;
    if (!on) return;
    box.querySelector('.thm-statement').textContent = t(`dictonic.thm.${kind}`, L);
    more.textContent = t(detail.hidden ? 'dictonic.thm.more' : 'dictonic.thm.less', L);
    detail.textContent = t('dictonic.thm.detail', L);
    evToggle.textContent = t(evidence.hidden ? 'dictonic.thm.evidence.show' : 'dictonic.thm.evidence.hide', L);
    box.querySelector('.thm-chart-title').textContent = t('dictonic.thm.chart', L);
    if (drawnFor !== `${kind}.${L}`) chart(kind, L);
    const m = svg.querySelector('.thm-marker'), x = PAD + ((W - 2 * PAD) * u) / 1000;
    m.setAttribute('x1', x); m.setAttribute('x2', x);
    box.querySelector('.thm-count').textContent = countLine(kind, v, L);
    // (4) the switch, Delian only: before the octet the rhombus's long diagonal (oct–oct) is a bond, after it the short one (tet–tet)
    flip.hidden = kind !== 'delian';
    if (kind === 'delian') {
      const before = v < 1 / 3 && v > 0, after = v > 1 / 3 && v < 1;
      // rhombus of the dual: oct sites at the ends of the long diagonal (length √2), tet sites at the short one (length 1)
      const cx = 60, cy = 40, a = 38, b = a / Math.SQRT2;
      flip.querySelector('svg').innerHTML = `<polygon points="${cx - a},${cy} ${cx},${cy - b} ${cx + a},${cy} ${cx},${cy + b}" fill="none" stroke="#9fa8c0" stroke-width="1.5"/>
        <line x1="${cx - a}" y1="${cy}" x2="${cx + a}" y2="${cy}" stroke="#9d8cff" stroke-width="${before ? 5 : 1.2}" ${before ? '' : 'stroke-dasharray="3 3"'}/>
        <line x1="${cx}" y1="${cy - b}" x2="${cx}" y2="${cy + b}" stroke="#ffc857" stroke-width="${after ? 5 : 1.2}" ${after ? '' : 'stroke-dasharray="3 3"'}/>
        ${[[cx - a, cy, '#9d8cff'], [cx + a, cy, '#9d8cff'], [cx, cy - b, '#ffc857'], [cx, cy + b, '#ffc857']].map(([px, py, c]) => `<circle cx="${px}" cy="${py}" r="5" fill="${c}"/>`).join('')}`;
      flip.classList.toggle('now', !!paused || Math.abs(v - 1 / 3) < 1e-9);
      flip.querySelector('.thm-flip-label').textContent = t('dictonic.thm.flip', L);
    }
  }
  return { update };
}
