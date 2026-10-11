// The 5D/6D catalogue file (data/catalogue-5d6d.json), fetched once (browser only). Its geometry lives in krp-core
// (quasicrystal-catalogue.js); loading the app's data file stays here.
let cataloguePromise = null;
export function loadCatalogue() {
  cataloguePromise ??= fetch('./data/catalogue-5d6d.json').then((r) => r.json()).catch(() => []);
  return cataloguePromise;
}
