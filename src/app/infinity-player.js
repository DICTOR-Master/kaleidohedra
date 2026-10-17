// The ∞ player (DICTO 2026-10-17: "Double Vision then becomes a player for any build"): ◀ Wrap and ▶ Unwrap as plain VHS triangles in
// the two rings of an ∞, a light running round the ∞ while the film plays (backwards for Wrap), and a VHS pause beside it that resumes
// the way it was going. Tapping the running direction pauses too. Shared by the worlds that have a film (first: Vajrayana); the look is
// Dual Vision's. The world keeps its own film state and calls render(); the player only draws and reports taps.
//   createInfinityPlayer({ onDir(d), onPause(), words(L) -> { wrap, unwrap, pause } }) -> { el, render({ on, dir }, L) }
let styled = false;
const CSS = `
.inf-row{display:flex;justify-content:center;align-items:center;gap:14px}
.inf{position:relative;flex:0 0 184px;width:184px;height:83px;color:#d8cfb8}
.inf-line{position:absolute;inset:0;width:100%;height:100%;fill:none;stroke:#e8c060;stroke-width:3;opacity:.6;pointer-events:none}
.inf .inf-lobe{position:absolute!important;top:12px;margin:0!important;min-width:0!important;width:60px;height:60px;border-radius:50%!important;padding:0!important;display:grid;place-items:center;background:transparent!important;border:2px solid transparent!important;color:#d8cfb8!important;cursor:pointer;touch-action:manipulation}
.inf .inf-lobe[data-inf=wrap]{left:21px;right:auto}
.inf .inf-lobe[data-inf=unwrap]{right:21px;left:auto}
.inf-lobe svg{width:24px;height:24px;fill:currentColor;stroke:currentColor;stroke-width:1.5;stroke-linejoin:round}
.inf .inf-lobe.active{color:#e8c060!important}
.inf .inf-lobe.active svg{filter:drop-shadow(0 0 6px #e8c060)}
.inf-pause{width:46px;height:46px;border-radius:10px;padding:0;display:grid;place-items:center}
.inf-pause svg{width:20px;height:20px;fill:currentColor}
.inf-pause.active{color:#e8c060;border-color:#e8c060}
.inf-run{stroke:#ffe08a;stroke-width:4.5;stroke-linecap:round;stroke-dasharray:16 84;opacity:0;filter:drop-shadow(0 0 4px #e8c060)}
.inf.run .inf-line{opacity:1}
.inf.run .inf-run{opacity:1;animation:inf-run 2.2s linear infinite}
.inf.run.rev .inf-run{animation-direction:reverse}
@keyframes inf-run{from{stroke-dashoffset:0}to{stroke-dashoffset:-100}}`;
const PATH = 'M100 45C126 9 186 9 186 45S126 81 100 45 14 9 14 45 74 81 100 45Z';

export function createInfinityPlayer({ onDir, onPause, words }) {
  if (!styled) { const s = document.createElement('style'); s.textContent = CSS; document.head.appendChild(s); styled = true; }
  const el = document.createElement('div');
  el.className = 'w4d-row inf-row';
  el.innerHTML = `<div class="inf"><svg class="inf-line" viewBox="0 0 200 90" aria-hidden="true"><path d="${PATH}"/><path class="inf-run" pathLength="100" d="${PATH}"/></svg>`
    + ['wrap', 'unwrap'].map((d) => `<button type="button" class="inf-lobe" data-inf="${d}"><svg viewBox="0 0 20 20" aria-hidden="true">${d === 'unwrap' ? '<path d="M6 3l11 7-11 7z"/>' : '<path d="M14 3L3 10l11 7z"/>'}</svg></button>`).join('')
    + '</div><button type="button" class="inf-pause" data-inf-pause><svg viewBox="0 0 20 20" aria-hidden="true"><rect x="4" y="3" width="4" height="14" rx="1"/><rect x="12" y="3" width="4" height="14" rx="1"/></svg></button>';
  el.querySelectorAll('[data-inf]').forEach((b) => b.addEventListener('click', () => onDir(b.dataset.inf === 'unwrap' ? 1 : -1)));
  el.querySelector('[data-inf-pause]').addEventListener('click', () => onPause());
  return {
    el,
    render({ on, dir }, L) {
      const w = words(L);
      el.querySelectorAll('[data-inf]').forEach((b) => { const d = b.dataset.inf === 'unwrap' ? 1 : -1, t = w[b.dataset.inf]; b.title = t; b.setAttribute('aria-label', t); b.classList.toggle('active', on && dir === d); });
      const pb = el.querySelector('[data-inf-pause]'); pb.hidden = !on; pb.title = w.pause; pb.setAttribute('aria-label', w.pause); pb.classList.toggle('active', on && dir === 0);
      const inf = el.querySelector('.inf'); inf.classList.toggle('run', on && dir !== 0); inf.classList.toggle('rev', dir < 0);
    },
  };
}
