// From parallelohedra.spec.ts: Parallelohedra in its four sections, with the credits in the details:
// Zometool (DICTO's leaning prism), the Bain stretch (the regular-hexagon ED), the Regular 9 (a new
// member).
import { open, assert } from './lib.mjs';
const open4 = async (h) => { await h.page.tap('.dicto-dim-content [data-family="PARALLELOHEDRA"]'); await h.wait(800); };
const credit = async (h, section, id, kind, text) => {
  await h.page.tap(`[data-section="${section}"] [data-action="tool:polyShape:${id}"]`); await h.wait(800);
  assert.match(await h.page.textContent(`[data-credit="${kind}"]`), text);
  await h.page.tap('.dim-wizard-back'); await h.wait(500);
};
export default [
  { name: "Fedorov's five, the variants, Kaleidohedra verified and the Regular 9, with their credits", async run(b) {
    const h = await open(b, { wizard: true });
    await open4(h);
    const counts = await h.page.evaluate(() => Object.fromEntries([...document.querySelectorAll('.poly-section')].map((s) => [s.dataset.section, s.querySelectorAll('[data-action]').length])));
    const { KALEIDOHEDRA_VERIFIED } = await import('../../../src/krp-core/src/polyhedra/families.js');
    assert.deepEqual(counts, { fedorov: 5, variants: 6, kaleidohedra: KALEIDOHEDRA_VERIFIED.length, regularNine: 9 });
    await credit(h, 'variants', 'DICTO_LEANING_HEX_PRISM', 'zome', /Zometool/);
    await credit(h, 'kaleidohedra', 'REGULAR_HEX_ED', 'bain', /Bain/);
    await credit(h, 'regularNine', 'RHOMBOHEDRON_60', 'regular-nine', /Regular 9/);
    h.noErrors(); await h.close();
  } },
];
