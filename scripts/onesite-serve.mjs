// Local stand-in for Vercel's router, for testing one site, four doors: serves dist-onesite/.vercel/output/static and applies
// config.json's routes (host conditions, headers with continue, filesystem, rewrites) the way the Build Output API describes.
//   node scripts/onesite-serve.mjs [port]     then browse with each host mapped to 127.0.0.1 (Host header decides the door)
import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.join(path.dirname(path.dirname(fileURLToPath(import.meta.url))), 'dist-onesite', '.vercel', 'output');
const { routes } = JSON.parse(await readFile(path.join(root, 'config.json'), 'utf8'));
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.txt': 'text/plain', '.xml': 'application/xml', '.md': 'text/markdown', '.webp': 'image/webp', '.glb': 'model/gltf-binary' };
const isFile = async (p) => { try { return (await stat(p)).isFile(); } catch { return false; } };
http.createServer(async (req, res) => {
  const host = (req.headers.host || '').split(':')[0]; let [pathname] = req.url.split('?'); pathname = decodeURIComponent(pathname);
  const hdrs = {}; let served = null, phase = 'pre';
  const fsPath = (p) => path.join(root, 'static', p.replace(/\?.*$/, ''));
  for (const r of routes) {
    if (r.handle === 'filesystem') { phase = 'post'; if (await isFile(fsPath(pathname)) && pathname !== '/') { served = pathname; break; } continue; }
    if (r.has && !r.has.every((h) => h.type === 'host' && h.value === host)) continue;
    const m = pathname.match(new RegExp(r.src)); if (!m) continue;
    if (r.headers) Object.assign(hdrs, r.headers);
    if (r.dest) { served = r.dest.replace(/\$(\d)/g, (_, i) => m[+i]); break; }
    if (!r.continue) break;
  }
  served = served || pathname;
  const f = fsPath(served);
  if (!(await isFile(f))) { res.writeHead(404, hdrs); return res.end('404 ' + served); }
  res.writeHead(200, { ...hdrs, 'Content-Type': TYPES[path.extname(f)] || 'application/octet-stream', 'X-Served': served });
  res.end(await readFile(f));
}).listen(+(process.argv[2] || 8090), () => console.log('one-site test server on', process.argv[2] || 8090));
