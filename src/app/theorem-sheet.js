// A theorem shown with its evidence (DICTO 2026-10-25: "a presentation of a geometric theorem", not a demonstration), for any world
// built on the layered-world engine (world-chains.js) with one big slider: (1) the statement on a card, a tap opens why it holds;
// (2) a live chart of the exact bond sizes along the slider, the key points marked and a marker riding with the slider; (3) the bonds
// of each piece; (4) where there is a switch, the switch drawn in the dual. (2)-(4) live in the 📖 Almanac sheet, opened from the
// panel, so the panel keeps only the statement and the controls; the sheet links to the world's entry in the app's Almanac.
// Used by DICTONIC (dictonic-theorem.js) and The Global Web of Bonds (world-global-web.js); each passes its networks as data:
//   networks[kind] = { areas(v) → { key: size }, curves: [[key, colour]], marks: [stop keys], statement(L), detail(L), chart(L),
//     bond(key, L), mark(key, L), count(v, L), flip: null | { svg(v) → markup, now(v, paused), label(L) } }
//   words = { more(L), less(L), almanac(L), title(L), entry(L) }, entryAction: what the sheet's entry button opens.
// The sheet is in the page only while it is open (one sheet at a time, whichever world shows it).

export function mountTheoremSheet(panel, { networks, words, entryAction, stopsOf, valueAt, openAction = () => {} }) {
  const box = document.createElement('div');
  box.className = 'w4d-row ch-theorem';
  box.innerHTML = `<div class="thm-card"><p class="thm-statement"></p><button type="button" class="thm-more"></button><p class="thm-detail" hidden></p></div>
    <button type="button" class="thm-almanac-open"></button>`;
  const sheet = document.createElement('div');
  sheet.className = 'thm-almanac';
  sheet.hidden = true;
  sheet.innerHTML = `<div class="thm-alm-head"><span class="thm-alm-title"></span><button type="button" class="thm-alm-close" aria-label="Close">✕</button></div>
    <button type="button" class="thm-alm-entry"></button>
    <div class="thm-evidence"><div class="thm-chart"><div class="thm-chart-title"></div><svg viewBox="0 0 320 120" preserveAspectRatio="none" role="img"></svg><div class="thm-legend"></div></div>
    <div class="thm-count" aria-live="polite"></div>
    <div class="thm-flip"><svg viewBox="0 0 120 80"></svg><span class="thm-flip-label"></span></div></div>`;
  const show = (on) => { sheet.hidden = !on; if (on && !sheet.isConnected) document.body.appendChild(sheet); else if (!on) sheet.remove(); };
  const caption = panel.querySelector('.ch-param-caption');
  caption.after(box);
  const more = box.querySelector('.thm-more'), detail = box.querySelector('.thm-detail');
  more.addEventListener('click', () => { detail.hidden = !detail.hidden; box.querySelector('.thm-card').classList.toggle('open', !detail.hidden); update(last); });
  box.querySelector('.thm-statement').addEventListener('click', () => box.querySelector('.thm-card').classList.toggle('open'));
  const svg = sheet.querySelector('.thm-chart svg'), flip = sheet.querySelector('.thm-flip');
  box.querySelector('.thm-almanac-open').addEventListener('click', () => { show(sheet.hidden); update(last); });
  sheet.querySelector('.thm-alm-close').addEventListener('click', () => { show(false); update(last); });
  // the whole entry (words, data) in the app's Almanac: one name, one place
  sheet.querySelector('.thm-alm-entry').addEventListener('click', () => { show(false); openAction(entryAction); });
  // the sheet closes with the world (its panel hidden)
  new MutationObserver(() => { if (!panel.classList.contains('visible')) show(false); }).observe(panel, { attributes: true, attributeFilter: ['class'] });
  let last = null, drawnFor = null;
  const W = 320, H = 120, PAD = 6;
  function chart(kind, L) {
    const net = networks[kind], stops = stopsOf(kind), N = 200, ys = [];
    for (let i = 0; i <= N; i++) ys.push(net.areas(valueAt(kind, (i * 1000) / N)));
    const top = Math.max(...ys.flatMap((a) => Object.values(a))) * 1.08;
    const X = (u) => PAD + ((W - 2 * PAD) * u) / 1000, Y = (a) => H - PAD - ((H - 2 * PAD) * a) / top;
    const paths = net.curves.map(([key, col]) => `<polyline fill="none" stroke="${col}" stroke-width="2.4" vector-effect="non-scaling-stroke" points="${ys.map((a, i) => `${X((i * 1000) / N).toFixed(1)},${Y(a[key]).toFixed(1)}`).join(' ')}"/>`).join('');
    const marks = net.marks.map((k) => stops.find((s) => s.key === k)).filter(Boolean)
      .map((s) => `<line x1="${X(s.u)}" x2="${X(s.u)}" y1="${PAD}" y2="${H - PAD}" stroke="#ffffff55" stroke-dasharray="3 3" vector-effect="non-scaling-stroke"/>`).join('');
    svg.innerHTML = `${marks}${paths}<line class="thm-marker" y1="${PAD}" y2="${H - PAD}" stroke="#fff" stroke-width="2" vector-effect="non-scaling-stroke"/>`;
    sheet.querySelector('.thm-legend').innerHTML = net.curves.map(([key, col]) => `<span><i style="background:${col}"></i>${net.bond(key, L)}</span>`).join('')
      + `<span class="thm-marks">${net.marks.map((k) => net.mark(k, L)).join(' · ')}</span>`;
    drawnFor = `${kind}.${L}`;
  }
  function update(s) {
    last = s;
    if (!s) return;
    const { kind, u, v, L, paused } = s, net = networks[kind];
    box.hidden = !net;
    if (!net) { show(false); return; }
    box.querySelector('.thm-statement').textContent = net.statement(L);
    more.textContent = detail.hidden ? words.more(L) : words.less(L);
    detail.textContent = net.detail(L);
    box.querySelector('.thm-almanac-open').textContent = `📖 ${words.almanac(L)}`;
    sheet.querySelector('.thm-alm-title').textContent = words.title(L);
    sheet.querySelector('.thm-alm-entry').textContent = words.entry(L);
    sheet.querySelector('.thm-chart-title').textContent = net.chart(L);
    if (drawnFor !== `${kind}.${L}`) chart(kind, L);
    const m = svg.querySelector('.thm-marker'), x = PAD + ((W - 2 * PAD) * u) / 1000;
    m.setAttribute('x1', x); m.setAttribute('x2', x);
    sheet.querySelector('.thm-count').textContent = net.count(v, L);
    flip.hidden = !net.flip;
    if (net.flip) {
      flip.querySelector('svg').innerHTML = net.flip.svg(v);
      flip.classList.toggle('now', net.flip.now(v, paused));
      flip.querySelector('.thm-flip-label').textContent = net.flip.label(L);
    }
  }
  return { update };
}

/** The switch in the dual (a quadrilateral, its two like diagonals): the horizontal one is a bond before the switch, the vertical one
 *  after it; the bond alive is drawn thick, the other dashed. a, b: the half-diagonals; cols: [horizontal, vertical]. */
export function switchPicture({ a, b, cols: [ch, cv], before, after }) {
  const cx = 60, cy = 40;
  return `<polygon points="${cx - a},${cy} ${cx},${cy - b} ${cx + a},${cy} ${cx},${cy + b}" fill="none" stroke="#9fa8c0" stroke-width="1.5"/>
        <line x1="${cx - a}" y1="${cy}" x2="${cx + a}" y2="${cy}" stroke="${ch}" stroke-width="${before ? 5 : 1.2}" ${before ? '' : 'stroke-dasharray="3 3"'}/>
        <line x1="${cx}" y1="${cy - b}" x2="${cx}" y2="${cy + b}" stroke="${cv}" stroke-width="${after ? 5 : 1.2}" ${after ? '' : 'stroke-dasharray="3 3"'}/>
        ${[[cx - a, cy, ch], [cx + a, cy, ch], [cx, cy - b, cv], [cx, cy + b, cv]].map(([px, py, c]) => `<circle cx="${px}" cy="${py}" r="5" fill="${c}"/>`).join('')}`;
}
