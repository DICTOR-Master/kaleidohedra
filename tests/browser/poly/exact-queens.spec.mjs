// DICTO 2026-10-29: the exact builds beside RCP. The 600-cell's card keeps both RCP builds and adds "White Queen: exact build", the
// 120-cell's keeps its RCP build and adds "Red Queen: exact build"; each opens the queens' world at the core of the Shells view; a tap
// on the picture adds the next shell; RCP view redraws the shells in the RCP build's perspective; the other polytopes have no such
// button.
import { open, assert } from './lib.mjs';
const card = async (h, id) => {
  await h.page.tap('[data-dim="4D"]'); await h.wait(500);
  await h.page.tap('.dicto-dim-content [data-family="POLYTOPES_4D"]'); await h.wait(700);
  await h.page.tap(`[data-action="tool:polyShape:${id}"]`); await h.wait(700);
};
const wq = (h) => h.page.evaluate(() => window.__whiteQueenProbe());
export default [
  { name: 'the 600-cell and 120-cell cards open the exact builds, RCP kept', async run(b) {
    for (const [id, queen, rcp, total, second] of [['POLYTOPE_600_CELL', 'white', ['600-cell', '600-cell (vertex-first)'], 15, 20], ['POLYTOPE_120_CELL', 'red', ['120-cell'], 9, 12]]) {
      const h = await open(b, { wizard: true });
      await card(h, id);
      assert.deepEqual(await h.page.evaluate(() => [...document.querySelectorAll('.poly-detail-build')].map((x) => x.dataset.target)), rcp, `${id}: RCP builds kept`);
      await h.page.tap('.poly-detail-exact'); await h.wait(2500);
      if (await h.page.locator('#leave-dialog:not([hidden])').count()) { await h.page.tap('#leave-dialog [data-choice="keep"]'); await h.wait(1500); }
      let st = await wq(h);
      assert.deepEqual([st.queen, st.mode, st.shells, st.total, st.whole], [queen, 'shells', 1, total, false], `${id}: the core`);
      // a tap on the picture adds the next shell
      const c = await (await h.page.$('canvas')).boundingBox();
      await h.tap({ x: c.x + c.width / 2, y: c.y + c.height * 0.4 }); await h.wait(800);
      st = await wq(h); assert.equal(st.shells, 2, `${id}: a tap adds shell 2`); assert.equal(st.newest.pieces, second);
      await h.page.tap('#worldwhiteQueen-panel [data-wq-rcp]'); await h.wait(1000);
      st = await wq(h); assert.equal(st.rcp, true, `${id}: RCP view`);
      await h.page.screenshot({ path: `/tmp/pv-exact-${queen}-rcp.png` });
      await h.page.tap('#worldwhiteQueen-panel [data-wq-rcp]'); await h.wait(500);
      h.noErrors(); await h.close();
    }
  } },
  { name: 'the other polytopes have no exact-build button', async run(b) {
    const h = await open(b, { wizard: true });
    await card(h, 'POLYTOPE_24_CELL');
    assert.equal(await h.page.$('.poly-detail-exact'), null);
    h.noErrors(); await h.close();
  } },
];
