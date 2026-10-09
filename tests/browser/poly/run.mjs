// Runs Polyhedraverse's browser tests (every *.spec.mjs here; ONLY=name runs those whose file or
// title contains it). Each spec exports [{ name, run(browser) }]. Serve the app first (as the smoke
// test does); BASE_URL picks the address.
import { chromium } from 'playwright';
import { readdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const only = process.env.ONLY;
const files = readdirSync(here).filter((f) => f.endsWith('.spec.mjs')).sort();
const browser = await chromium.launch();
let passed = 0, failed = 0;
const t0 = Date.now();
for (const f of files) {
  const tests = (await import(path.join(here, f))).default;
  for (const test of tests) {
    if (only && !f.includes(only) && !test.name.includes(only)) continue;
    const t = Date.now();
    try {
      await Promise.race([test.run(browser), new Promise((_, no) => setTimeout(() => no(new Error('timed out after 120 s')), 120000))]);
      passed++;
      console.log(`ok   ${f.replace('.spec.mjs', '')}: ${test.name} (${((Date.now() - t) / 1000).toFixed(1)} s)`);
    } catch (e) {
      failed++;
      console.log(`FAIL ${f.replace('.spec.mjs', '')}: ${test.name}\n     ${String(e.message ?? e).split('\n').slice(0, 4).join('\n     ')}`);
    }
  }
}
await browser.close();
console.log(`${passed} passed, ${failed} failed (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
process.exit(failed ? 1 : 0);
