export async function resolve(spec, ctx, next) {
  if (spec === 'three' || spec.startsWith('three/')) return next(spec, { ...ctx, parentURL: 'file:///home/dicto/kaleidohedra/package.json' });
  return next(spec, ctx);
}
