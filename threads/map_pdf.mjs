import { chromium } from 'playwright';
const b = await chromium.launch(); const p = await b.newPage();
await p.goto('file:///tmp/thr/MAP.html'); await p.pdf({ path: '/tmp/thr/THREADS-MAP.pdf', format: 'A4', margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' } });
await b.close(); console.log('ok');
