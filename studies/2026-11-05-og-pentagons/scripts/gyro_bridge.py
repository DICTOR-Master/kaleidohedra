exec(open("gyro_kit2.py").read().split("print(\"PER-CELL")[0])
# octet corner pieces (exact octet configuration around the origin), turned/translated to an upper twin-layer octahedron
src = open("octet_kit3.py").read().split("cones = []")[0]
g = {}; exec(src, g)
ps = [p for p in g["rest"].decompose() if abs(p.volume() - 0.07826) < 1e-4]; cyc = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)
six = [b.transform(np.c_[np.linalg.matrix_power(cyc, k), np.zeros(3)].tolist()) for b in ps for k in range(3)]
c = R*np.array([0., 1, 1]); O = hull(OCT + c); rest = O - U_all
P = [p for p in rest.decompose() if abs(p.volume() - 0.25255) < 1e-4][0]
cs = [s_.translate(c.tolist()) for s_ in six]; inP = [s_ for s_ in cs if abs((s_ ^ P).volume() - s_.volume()) < 1e-7]
print("octet corner pieces lying inside the 0.25255 piece:", len(inP))
extra = P - m3.Manifold.batch_boolean(inP, m3.OpType.Add); bits = [b for b in extra.decompose() if b.volume() > 1e-9]
print("extra bits:", [round(b.volume(), 6) for b in bits])
for b in bits:
    P_ = np.array(b.to_mesh().vert_properties)[:, :3]; cen = P_.mean(0)
    grown = b.translate((-cen).tolist()).scale([1.02]*3).translate(cen.tolist())
    print("  bit", round(b.volume(), 6), "face contact with corner pieces:", [round((grown ^ s_).volume(), 7) for s_ in inP])
print("FINAL ok")
