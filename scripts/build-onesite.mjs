// One site, four doors (DICTO 2026-10-28/29: one Vercel project instead of four, easy to mirror on a second host).
// Builds the three app doors with the usual per-door build (scripts/build.mjs, SITE=...), keeps ONE copy of everything they
// share (checked byte for byte: the build fails if a shared file differs between doors), and puts each door's own pages
// (index, guide, legal, robots, sitemap, search verification) in its own folder; dictospheres.com goes in whole.
//   dist-onesite/.vercel/output/   Vercel Build Output API v3: static/ + config.json (host routing and per-host headers)
//   dist-onesite/.vercel/output/static/_worker.js + _headers: the same routing for Cloudflare Pages (advanced mode)
// Nothing at the root of static/ may share a name with a door page: on Vercel, files are served before the host rewrites.
//   DICTOSPHERES_DIR: the dictospheres.com files (default ../dictospheres; on Vercel a shallow clone of the public repo).
import { execFileSync } from 'node:child_process';
import { cp, mkdir, readdir, readFile, rm, writeFile, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const out = path.join(root, 'dist-onesite', '.vercel', 'output');
const stat_ = path.join(out, 'static');
const tmp = path.join(root, 'dist-onesite', 'doors');

// host -> door folder; the apps' door pages, and the pretty paths they answer to
export const DOORS = {
  'kaleidohedra.dictospheres.com': '_k',
  'rhombiverse.dictospheres.com': '_r',
  'polyhedraverse.dictospheres.com': '_p',
  // test addresses of the one-site Vercel project, to check every door before (and after) the real addresses point here
  'dicto-onesite-k.vercel.app': '_k',
  'dicto-onesite-r.vercel.app': '_r',
  'dicto-onesite-p.vercel.app': '_p',
};
const APP = { _k: 'kaleidohedra', _r: 'rhombiverse', _p: 'polyhedraverse' };
const HOME = ['dictospheres.com', 'www.dictospheres.com', 'dicto-onesite.vercel.app'];
const DOOR_FILES = ['index.html', 'guide.html', 'legal.html', 'robots.txt', 'sitemap.xml', 'googlec4db6e568a2c28ac.html'];
const PRETTY = { '/guide': '/guide.html', '/terms': '/legal.html?doc=terms', '/privacy': '/legal.html?doc=privacy', '/security': '/legal.html?doc=security' };

async function files(dir, base = dir) {
  const r = [];
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) r.push(...(await files(f, base))); else r.push(path.relative(base, f));
  }
  return r;
}
const hash = async (f) => createHash('sha256').update(await readFile(f)).digest('hex');

async function main() {
  await rm(path.join(root, 'dist-onesite'), { recursive: true, force: true });
  await mkdir(stat_, { recursive: true });
  // 1. the three app doors, each with the usual build
  for (const [dir, site] of Object.entries(APP)) {
    execFileSync('node', ['scripts/build.mjs'], { cwd: root, env: { ...process.env, SITE: site }, stdio: 'inherit' });
    await cp(path.join(root, 'dist'), path.join(tmp, dir), { recursive: true });
  }
  // 2. shared files once (identical in every door), door pages in their folders
  const lists = {};
  for (const dir of Object.keys(APP)) lists[dir] = (await files(path.join(tmp, dir))).sort();
  const shared = lists._k.filter((f) => !DOOR_FILES.includes(f));
  for (const dir of ['_r', '_p']) {
    const s = lists[dir].filter((f) => !DOOR_FILES.includes(f));
    if (s.join('\n') !== shared.join('\n')) throw new Error(`door ${dir}: shared file list differs from _k`);
  }
  for (const f of shared) {
    const h = await hash(path.join(tmp, '_k', f));
    for (const dir of ['_r', '_p']) if ((await hash(path.join(tmp, dir, f))) !== h) throw new Error(`shared file differs between doors: ${f}`);
    await mkdir(path.dirname(path.join(stat_, f)), { recursive: true });
    await cp(path.join(tmp, '_k', f), path.join(stat_, f));
  }
  for (const dir of Object.keys(APP)) {
    for (const f of DOOR_FILES) if (existsSync(path.join(tmp, dir, f))) {
      await mkdir(path.join(stat_, dir), { recursive: true });
      await cp(path.join(tmp, dir, f), path.join(stat_, dir, f));
    }
  }
  // 3. dictospheres.com, whole, in _d
  let dsDir = process.env.DICTOSPHERES_DIR || path.join(root, '..', 'dictospheres');
  if (!existsSync(dsDir)) {
    dsDir = path.join(root, 'dist-onesite', 'dictospheres-src');
    execFileSync('git', ['clone', '--depth', '1', 'https://github.com/DICTOR-Master/dictospheres.git', dsDir], { stdio: 'inherit' });
  }
  for (const f of await files(dsDir)) {
    if (f.startsWith('.git') || f === 'vercel.json' || /^[A-Z][A-Z0-9-]*\.md$/.test(f)) continue;   // repo files, not site files
    await mkdir(path.dirname(path.join(stat_, '_d', f)), { recursive: true });
    await cp(path.join(dsDir, f), path.join(stat_, '_d', f));
  }
  // 4. no root file may shadow a door page
  const top = await readdir(stat_);
  const clash = top.filter((f) => DOOR_FILES.includes(f) || existsSync(path.join(stat_, '_d', f)));
  if (clash.length) throw new Error('root files shadow door pages: ' + clash.join(', '));

  // 5. Vercel routing (Build Output API v3) and headers
  const vj = JSON.parse(await readFile(path.join(root, 'vercel.json'), 'utf8'));
  const appHeaders = Object.fromEntries(vj.headers[0].headers.map((h) => [h.key, h.value]));
  // dictospheres.com has its own policy (vercel.json rules 2 and 3, DICTO 2026-10-31): the app's would block the tetrapod heap's
  // three.js, fonts, Supabase and weather.
  const homeHeaders = Object.fromEntries(vj.headers[1].headers.map((h) => [h.key, h.value]));
  const host = (h) => [{ type: 'host', value: h }];
  const routes = [];
  for (const h of Object.keys(DOORS)) routes.push({ src: '/(.*)', has: host(h), headers: appHeaders, continue: true });
  for (const h of HOME) routes.push({ src: '/(.*)', has: host(h), headers: homeHeaders, continue: true });
  for (const [h, dir] of Object.entries(DOORS)) {
    routes.push({ src: '^/$', has: host(h), dest: `/${dir}/index.html` });
    for (const [p, d] of Object.entries(PRETTY)) routes.push({ src: `^${p}$`, has: host(h), dest: `/${dir}${d}` });
  }
  for (const h of HOME) routes.push({ src: '^/$', has: host(h), dest: '/_d/index.html' });
  routes.push({ handle: 'filesystem' });
  for (const [h, dir] of Object.entries(DOORS)) routes.push({ src: `^/(${DOOR_FILES.map((f) => f.replace('.', '\\.')).join('|')})$`, has: host(h), dest: `/${dir}/$1` });
  for (const h of HOME) routes.push({ src: '^/(.*)$', has: host(h), dest: '/_d/$1' });
  await writeFile(path.join(out, 'config.json'), JSON.stringify({ version: 3, routes }, null, 1));

  // 6. Cloudflare Pages: the same routing as a worker, and the headers
  const worker = `// Cloudflare Pages (advanced mode): host routing for one site, four doors; generated by scripts/build-onesite.mjs.
const DOORS = ${JSON.stringify(DOORS)};
const HOME = ${JSON.stringify(HOME)};
const DOOR_FILES = ${JSON.stringify(DOOR_FILES)};
const PRETTY = ${JSON.stringify(PRETTY)};
const APP_HEADERS = ${JSON.stringify(appHeaders)};
const HOME_HEADERS = ${JSON.stringify(homeHeaders)};
export function route(hostname, pathname, search) {
  const dir = DOORS[hostname];
  if (dir) {
    if (pathname === '/') return '/' + dir + '/index.html' + search;
    if (PRETTY[pathname]) { const [p, q] = PRETTY[pathname].split('?'); return '/' + dir + p + (q ? '?' + q : search); }
    if (DOOR_FILES.includes(pathname.slice(1))) return '/' + dir + pathname + search;
    return pathname + search;
  }
  if (HOME.includes(hostname) || hostname.endsWith('.pages.dev')) return '/_d' + (pathname === '/' ? '/index.html' : pathname) + search;
  return pathname + search;
}
export default {
  async fetch(request, env) {
    const u = new URL(request.url);
    const target = route(u.hostname, u.pathname, u.search);
    // Pages serves clean URLs (x.html -> /x, index.html -> /), so ask for those, not the .html names
    const clean = target.replace(/\\/index\\.html(?=\\?|$)/, '/').replace(/\\.html(?=\\?|$)/, '');
    let res = await env.ASSETS.fetch(new Request(new URL(clean, u.origin), request));
    if (res.status === 404 && !DOORS[u.hostname] && target.startsWith('/_d/')) res = await env.ASSETS.fetch(request);
    res = new Response(res.body, res);
    for (const [k, v] of Object.entries(DOORS[u.hostname] ? APP_HEADERS : HOME_HEADERS)) res.headers.set(k, v);
    return res;
  },
};
`;
  await writeFile(path.join(stat_, '_worker.js'), worker);
  await rm(tmp, { recursive: true, force: true });
  await rm(path.join(root, 'dist'), { recursive: true, force: true });
  const n = (await files(stat_)).length;
  const size = (await Promise.all((await files(stat_)).map(async (f) => (await stat(path.join(stat_, f))).size))).reduce((a, b) => a + b, 0);
  console.log(`One site: ${n} files, ${(size / 1e6).toFixed(1)} MB (shared ${shared.length}, doors ${Object.keys(APP).length}, home in _d); ${routes.length} routes`);
}
main().catch((e) => { console.error(e); process.exit(1); });
