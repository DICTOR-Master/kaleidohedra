import { idStar } from '/home/dicto/kaleidohedra/src/krp-core/src/geometry-extensions/id-star.js';
const s = idStar(); console.log(JSON.stringify(s, (k, v) => (typeof v === 'number' ? +v.toFixed(12) : v)).slice(0, 300));
import fs from 'fs'; fs.writeFileSync('/tmp/claude-1000/-home-dicto-Downloads-pet-bottle-rhombiverse/1096c3a3-2779-41fc-a53e-3ed930c8f843/scratchpad/star.json', JSON.stringify(s));
