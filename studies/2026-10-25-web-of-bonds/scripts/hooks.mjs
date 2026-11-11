export async function resolve(spec, ctx, next) {
  if (spec === 'three' || spec.startsWith('three/')) return next(spec, { ...ctx, parentURL: 'file://~/kaleidohedra/package.json' });
  return next(spec, ctx);
}
