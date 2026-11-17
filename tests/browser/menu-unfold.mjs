// The world menu by the books (DICTO 2026-11-17) folds each book and each world's pieces: a test that goes straight to one entry
// opens its book (and its world, for a piece) first, with the menu's own fold buttons, so the entry is on screen to tap.
export const unfold = (page, action) => page.evaluate((a) => {
  const el = document.querySelector(`.bm [data-action="${a}"]`);
  for (let n = el; n; n = n.parentElement) if (n.matches?.('.bm-list[hidden], .bm-pieces[hidden]')) n.previousElementSibling.click();
}, action);
