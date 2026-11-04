exec(open("octet_kit3.py").read().split("cones = []")[0])
ps = [p for p in rest.decompose() if abs(p.volume() - 0.07826) < 1e-5]; a, b = ps
cyc = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)
for k in range(1, 3):
    Mk = np.linalg.matrix_power(cyc, k); img = a.transform(np.c_[Mk, np.zeros(3)].tolist())
    print(f"z-corner piece turned by the 3-fold axis ({k}): lies in the leftover:", round((img ^ rest).volume(), 6), "of", round(img.volume(), 6))
print("+z vs -z corner piece by rotation:", same_shape(a, b, "rotation"), "by reflection:", same_shape(a, b, "reflection"))
print("corner piece achiral (= own mirror by rotation)?", same_shape(a, a.mirror([1, 0, 0]), "rotation"))
print("FINAL ok")
