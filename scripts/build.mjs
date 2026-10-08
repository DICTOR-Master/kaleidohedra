// Production-only build: minifies src/**/*.js in place (same file
// structure, same relative imports, NO bundling across files) and copies
// every other static asset the client actually loads. Local dev is
// completely untouched by this -- README.md's "Running locally" section
// still means `python3 -m http.server` directly against the repo root,
// zero tooling required, exactly as before. This script only runs at
// Vercel build time (see vercel.json's buildCommand), producing `dist/`
// as the deployed static output.
//
// Why minify-only, not bundle: a real per-file measurement (2026-08-24,
// on the actual Pi500 this app is played on) found 51%+ of src/'s JS
// bytes were comments/blank lines (this codebase's own very heavily-
// commented style) -- esbuild's minifier alone cut real measured bytes
// 669,897 -> 178,482 (73.4%), zero errors, with the exact same module
// graph untouched. Bundling would add real risk (dynamic import() paths,
// the many files/call-sites throughout this codebase) for a much smaller
// additional win, since HTTP/2 already parallelizes the separate
// requests -- not worth it for what the actual profiled bottleneck was.
import { build } from 'esbuild';
import { mkdir, cp, readdir, rm, readFile, writeFile } from 'node:fs/promises';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const dist = path.join(root, 'dist');

async function findJsFiles(dir) {
  const entries = await readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...(await findJsFiles(full)));
    else if (entry.name.endsWith('.js')) files.push(full);
  }
  return files;
}

async function main() {
  await rm(dist, { recursive: true, force: true });
  await mkdir(dist, { recursive: true });

  // One code, two front doors (KRP): SITE picks which app this build is (Vercel sets it per project;
  // default Kaleidohedra, this repo's own). Each site's head, guide, changelog and icons are in
  // site/<site>/; everything else is shared.
  const SITE_ID = process.env.SITE || 'kaleidohedra';
  const { SITES } = await import(pathToFileURL(path.join(root, 'src/app/site.js')).href);
  const site = SITES[SITE_ID];
  if (!site) throw new Error(`unknown SITE '${SITE_ID}' (one of ${Object.keys(SITES).join(', ')})`);
  const staticEntries = ['index.html', 'rhombis.html', 'guide.html', 'legal.html', `site/${SITE_ID}`, 'favicon.svg', 'assets', 'data', 'TERMS.md', 'PRIVACY.md', 'SECURITY.md'];
  if (SITE_ID === 'rhombiverse') staticEntries.push('googlec4db6e568a2c28ac.html'); // its search-console verification
  for (const entry of staticEntries) {
    await cp(path.join(root, entry), path.join(dist, entry), { recursive: true });
  }

  // Each page's site head (between its <!-- site head --> markers) and data-site; the wordmark.
  const siteFile = (f) => readFile(path.join(root, 'site', SITE_ID, f), 'utf8');
  const swapHead = (html, head) => {
    const a = html.indexOf('<!-- site head'), b = html.indexOf('<!-- /site head -->');
    if (a < 0 || b < 0) throw new Error('site head markers not found');
    return html.slice(0, a) + head.trimEnd() + '\n  ' + html.slice(b + '<!-- /site head -->'.length).trimStart().replace(/^/, '');
  };
  const page = async (file, headFile, more = (h) => h) => {
    const p = path.join(dist, file);
    let html = await readFile(p, 'utf8');
    html = more(swapHead(html, await siteFile(headFile)).replace('data-site="kaleidohedra"', `data-site="${SITE_ID}"`));
    await writeFile(p, html);
  };
  const [w1, w2] = site.wordmark;
  await page('index.html', 'head.html', (h) => h.replace(/<div id="hud-wordmark">.*?<\/div>/, `<div id="hud-wordmark">${w1}<span>${w2}</span></div>`));
  await page('guide.html', 'guide-head.html');
  await page('legal.html', 'icons.html', (h) => h.replace(/<title>[^<]*<\/title>/, `<title>${site.name}</title>`));

  // Search engines: the English guide pre-rendered into guide.html (the page's script still swaps
  // in the reader's language), plus robots.txt and a sitemap dated with this build.
  const { renderMarkdown } = await import(pathToFileURL(path.join(root, 'src/app/markdown.js')).href);
  const guidePath = path.join(dist, 'guide.html');
  const guideHtml = await readFile(guidePath, 'utf8');
  const guideBody = renderMarkdown(await siteFile('guide.md'));
  if (!guideHtml.includes('<main class="md-guide">Loading…</main>')) throw new Error('guide.html: <main> placeholder not found');
  await writeFile(guidePath, guideHtml.replace('<main class="md-guide">Loading…</main>', `<main class="md-guide" data-prerendered="en">${guideBody}</main>`));
  const URL_ = site.url;
  const today = new Date().toISOString().slice(0, 10);
  await writeFile(path.join(dist, 'robots.txt'), `User-agent: *\nAllow: /\n\nSitemap: ${URL_}/sitemap.xml\n`);
  const pages = ['/', '/guide', ...['ja', 'es', 'fr', 'ko', 'zh', 'ru'].map((l) => `/guide?lang=${l}`), ...(SITE_ID === 'rhombiverse' ? ['/rhombis.html'] : []), '/terms', '/privacy'];
  await writeFile(path.join(dist, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${pages.map((u) => `  <url><loc>${URL_}${u.replace('&', '&amp;')}</loc><lastmod>${today}</lastmod></url>`).join('\n')}\n</urlset>\n`);

  const jsFiles = await findJsFiles(path.join(root, 'src'));
  await build({
    entryPoints: jsFiles,
    outbase: path.join(root, 'src'),
    outdir: path.join(dist, 'src'),
    minify: true,
    format: 'esm',
    bundle: false,
    logLevel: 'info',
  });

  // tokens.css is the one stylesheet outside <style> blocks: copied with the sources.
  await cp(path.join(root, 'src/app/tokens.css'), path.join(dist, 'src/app/tokens.css'));
  console.log(`Built ${site.name}: ${jsFiles.length} JS files into dist/src/, plus static assets, into dist/.`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
