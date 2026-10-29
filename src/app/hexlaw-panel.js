// The Hexagonality Law panel (DICTO 2026-10-29, "all recommended": decisions 1A–5A, k-research
// studies/2026-10-30-hexagonality-law-panel). A "Law" button in the Stackings world opens a chart in the world's panel, above
// the layer chips: one paper of
// the law at a time (#66, #68, #70–#74, the same charts as the site cards), a measured or computed quantity against h, the share of
// hexagonal layers, with the law's straight line and a dot for each real stacking. Tapping a dot that names a stacking builds it in
// the world; the stacking built in the world (flipped layers included) is the gold marker on each line at its own h. ?law=68 opens
// the world with #68's chart showing (the site cards' "View in app"). Data: hexlaw-data.js, unchanged from the papers' studies.
import { t } from './i18n.js';
import { LAW_CHARTS } from './hexlaw-data.js';
import { layerTypes } from './stackings-geometry.js';

export const LAW_PAPERS = [...new Set(LAW_CHARTS.map((c) => c.paper))];
const COLOURS = ['#6fa3e0', '#d07fb0', '#7fae7a', '#a990d8', '#e07a6a', '#4fa3a5', '#b0b0b0'];
const GOLD = '#d4af37', INK = '#e8e4d8', MUTED = '#9a9a9a';
const W = 440, H = 210, M = { l: 44, r: 62, t: 12, b: 30 };
const lineAt = (ln, x) => ln[0][1] + ((x - ln[0][0]) * (ln[1][1] - ln[0][1])) / (ln[1][0] - ln[0][0]);
const fmt = (v) => (Math.abs(v) >= 100 ? v.toFixed(0) : Math.abs(v) >= 10 ? v.toFixed(1) : Math.abs(v) >= 1 ? v.toFixed(2) : v.toFixed(3)).replace('-', '−');

/** The share of hexagonal layers of a word, as [h count, layers], in lowest terms. */
const gcd = (a, b) => (b ? gcd(b, a % b) : a);
export const hexShare = (word) => { const ty = layerTypes(word), n = ty.filter((x) => x === 'h').length, g = gcd(n, ty.length) || 1; return [n / g, ty.length / g]; };

/** The y range of a chart: its points and lines, a little padded. */
function yRange(c) {
  const ys = c.series.flatMap((s) => [...s.points.map((p) => p.y), ...(s.line ? s.line.map((q) => q[1]) : [])]);
  let lo = Math.min(...ys), hi = Math.max(...ys); const pad = (hi - lo || 1) * 0.08; lo -= pad; hi += pad;
  return [lo, hi];
}
const ticks = (lo, hi) => { const step = 10 ** Math.floor(Math.log10((hi - lo) / 3)), k = [1, 2, 5].find((m) => (hi - lo) / (m * step) <= 5) ?? 10; const s = k * step, out = []; for (let v = Math.ceil(lo / s) * s; v <= hi + 1e-9; v += s) out.push(+v.toFixed(10)); return out; };

/** One chart as SVG markup; `own` = [h count, layers] of the world's stacking (marker on each line), or null. */
export function chartSvg(c, own, L) {
  const xmax = c.xmax ?? 1, [lo, hi] = yRange(c);
  const X = (x) => M.l + ((W - M.l - M.r) * x) / xmax, Y = (y) => H - M.b - ((H - M.t - M.b) * (y - lo)) / (hi - lo);
  const parts = [`<rect x="0" y="0" width="${W}" height="${H}" fill="none"/>`];
  for (const v of ticks(lo, hi)) parts.push(`<line x1="${M.l}" x2="${W - M.r}" y1="${Y(v)}" y2="${Y(v)}" stroke="#2a2d33" stroke-width="1"/><text x="${M.l - 5}" y="${Y(v) + 3.5}" text-anchor="end" font-size="10" fill="${MUTED}">${fmt(v)}</text>`);
  const xt = c.x === 'P' ? [0, 10, 20, 30] : [0, 0.25, 0.5, 0.75, 1];
  for (const v of xt) parts.push(`<text x="${X(v)}" y="${H - M.b + 14}" text-anchor="middle" font-size="10" fill="${MUTED}">${c.x === 'P' ? v : v === 0 || v === 1 ? v : v.toFixed(2)}</text>`);
  parts.push(`<line x1="${M.l}" x2="${W - M.r}" y1="${H - M.b}" y2="${H - M.b}" stroke="#555"/><text x="${(M.l + W - M.r) / 2}" y="${H - 3}" text-anchor="middle" font-size="10.5" fill="${INK}">${t(`law.x.${c.x}`, L)}</text>`);
  if (c.mark != null) parts.push(`<line x1="${X(c.mark)}" x2="${X(c.mark)}" y1="${M.t}" y2="${H - M.b}" stroke="${COLOURS[0]}" stroke-dasharray="2 3"/>`);
  if (c.x === 'h' && own) { const h = own[0] / own[1]; parts.push(`<line x1="${X(h)}" x2="${X(h)}" y1="${M.t}" y2="${H - M.b}" stroke="${GOLD}" stroke-dasharray="3 3" opacity="0.7"/>`); }
  c.series.forEach((s, i) => {
    const col = COLOURS[i % COLOURS.length];
    if (s.line) {
      const [[x0, y0], [x1, y1]] = s.line;
      if (s.until != null) {
        const yu = lineAt(s.line, s.until);
        parts.push(`<line x1="${X(x0)}" y1="${Y(y0)}" x2="${X(s.until)}" y2="${Y(yu)}" stroke="${col}" stroke-width="2"/><line x1="${X(s.until)}" y1="${Y(yu)}" x2="${X(x1)}" y2="${Y(y1)}" stroke="${col}" stroke-width="1.4" stroke-dasharray="5 4"/><circle cx="${X(s.until)}" cy="${Y(yu)}" r="3.5" fill="${col}"/>`);
      } else parts.push(`<line x1="${X(x0)}" y1="${Y(y0)}" x2="${X(x1)}" y2="${Y(y1)}" stroke="${s.joined ? INK : col}" stroke-width="${s.joined ? 1 : 2}"${s.joined ? ' stroke-dasharray="5 4"' : ''}/>`);
    }
    if (s.joined) parts.push(`<polyline fill="none" stroke="${col}" stroke-width="1.2" points="${s.points.map((p) => `${X(p.h)},${Y(p.y)}`).join(' ')}"/>`);
    const end = s.line && !s.joined ? s.line[1] : s.points.at(-1) ? [s.points.at(-1).h, s.points.at(-1).y] : null;
    if (end && c.series.length === 1) parts.push(`<text x="${X(end[0]) + 6}" y="${Y(end[1]) + 3.5}" font-size="10" fill="${INK}">${s.name}</text>`);
    s.points.forEach((p, j) => {
      const tag = `${LAW_CHARTS.indexOf(c)}.${i}.${j}`;
      parts.push(`<g class="law-dot${p.word ? ' law-build' : ''}" data-law-dot="${tag}" style="cursor:pointer"><circle cx="${X(p.h)}" cy="${Y(p.y)}" r="12" fill="transparent"/><circle cx="${X(p.h)}" cy="${Y(p.y)}" r="4.5" fill="${col}" stroke="#0b0d12" stroke-width="1.5"/></g>`);
    });
    if (c.x === 'h' && own && s.line && !s.joined) {
      const h = own[0] / own[1];
      if (h >= s.line[0][0] - 1e-9 && h <= s.line[1][0] + 1e-9) parts.push(`<circle class="law-own" cx="${X(h)}" cy="${Y(lineAt(s.line, h))}" r="6.5" fill="none" stroke="${GOLD}" stroke-width="2.5"/>`);
    }
  });
  const legend = c.series.length > 1 ? `<div class="law-legend" style="display:flex;flex-wrap:wrap;gap:4px 12px;justify-content:center;font-size:11px">${c.series.map((s, i) => `<span><span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:${COLOURS[i % COLOURS.length]};margin-right:4px"></span>${s.name}</span>`).join('')}</div>` : '';
  return `<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="${t(`law.${c.key}.title`, L)}" style="display:block">${parts.join('')}</svg>${legend}`;
}

/** The panel: a Law button inside `box` and the chart card above the stacking. `build(word)` builds a stacking in the world. */
export function mountLaw(box, panel, { word, build }) {
  const btn = document.createElement('button'); btn.type = 'button'; btn.className = 'stk-chip stk-law'; btn.dataset.stkLaw = '1';
  btn.style.borderColor = GOLD; box.prepend(btn);
  const card = document.createElement('div'); card.className = 'hexlaw-card'; card.hidden = true;
  // inside the world's panel, above the layer chips (a floating card covered the top bar and side buttons on a phone)
  if (!document.getElementById('hexlaw-style')) {
    const css = document.createElement('style'); css.id = 'hexlaw-style';
    // clear of the app's column of side buttons on a narrow screen
    css.textContent = '.hexlaw-card{font-family:system-ui,-apple-system,"Segoe UI",sans-serif}.hexlaw-card svg text{font-family:inherit}@media (max-width:700px){.hexlaw-card{width:calc(100% - 56px)!important;margin-left:0!important}}';
    document.head.append(css);
  }
  card.style.cssText = `width:100%;max-width:460px;margin:6px auto;background:rgba(11,13,18,0.94);border:1px solid #3a3d44;border-radius:10px;padding:8px 10px;color:${INK};font-size:12px;box-sizing:border-box;text-align:left`;
  card.innerHTML = `<div style="display:flex;align-items:center;gap:6px"><b class="law-head" style="flex:1"></b><button type="button" class="stk-chip" data-law-close aria-label="close">✕</button></div>
    <div class="w4d-row w4d-options law-papers" style="justify-content:center"></div><div class="law-charts"></div><div class="law-note" aria-live="polite" style="min-height:2.6em;margin-top:4px;color:#cfcabd;font-size:11.5px"></div>`;
  btn.after(card);
  const st = { open: false, paper: LAW_PAPERS[0], note: null, L: 'en' };
  const q = new URLSearchParams(globalThis.location?.search ?? '').get('law');
  if (q && LAW_PAPERS.includes(Number(q))) { st.open = true; st.paper = Number(q); }
  const paint = (L = st.L) => {
    st.L = L; btn.textContent = `${st.open ? '✓ ' : ''}${t('law.button', L)}`; btn.classList.toggle('active', st.open);
    card.hidden = !st.open || !panel.classList.contains('visible'); if (card.hidden) return;
    const own = hexShare(word());
    card.querySelector('.law-head').textContent = t('law.head', L);
    card.querySelector('.law-papers').innerHTML = LAW_PAPERS.map((p) => `<button type="button" data-law-paper="${p}" class="${p === st.paper ? 'active' : ''}">#${p}</button>`).join('');
    card.querySelector('.law-charts').innerHTML = LAW_CHARTS.filter((c) => c.paper === st.paper)
      .map((c) => `<div style="margin:4px 0 2px;font-weight:600">${c.label ? `${c.label} ` : ''}${t(`law.${c.key}.title`, L)}</div><div style="color:${MUTED};font-size:11px">${t(`law.${c.key}.y`, L)}</div>${chartSvg(c, own, L)}`).join('');
    const hasOwn = LAW_CHARTS.some((c) => c.paper === st.paper && c.x === 'h');
    card.querySelector('.law-note').textContent = st.note ?? (hasOwn ? `${t('law.own', L, { h: `${own[0]}/${own[1]}`, types: layerTypes(word()).join('') })} · ${t('law.tap', L)}` : t('law.noown', L));
  };
  btn.addEventListener('click', (e) => { e.stopPropagation(); st.open = !st.open; st.note = null; paint(); });
  card.addEventListener('click', (e) => {
    const close = e.target.closest('[data-law-close]'), pb = e.target.closest('[data-law-paper]'), dot = e.target.closest('[data-law-dot]');
    if (close) { st.open = false; paint(); return; }
    if (pb) { st.paper = Number(pb.dataset.lawPaper); st.note = null; paint(); return; }
    if (dot) {
      const [c, i, j] = dot.dataset.lawDot.split('.').map(Number), s = LAW_CHARTS[c].series[i], p = s.points[j];
      const said = `${s.name} · ${p.label}: ${fmt(p.y)}`;
      if (p.word && build(p.word)) { st.note = `${said} · ${t('law.built', st.L, { w: p.word })}`; paint(); }
      else { st.note = `${said}${p.word ? '' : ` · ${t('law.nobuild', st.L)}`}`; paint(); }
    }
  });
  new MutationObserver(() => paint()).observe(panel, { attributes: true, attributeFilter: ['class'] });
  return { update: (L) => paint(L), clearNote: () => { st.note = null; }, state: st };
}
