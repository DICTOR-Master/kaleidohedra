# Slices of the wave fields (wave_image.py output): the solid, and the field at the network's own wavelength (a/2) and at a/4.
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = np.load("wave-fields.npz"); S, a, N = D["S"], float(D["a"]), int(D["N"])
fig, axs = plt.subplots(2, 3, figsize=(13, 9), facecolor="white")
for row, (z, lab) in enumerate(((0, "slice through a cut OG centre (z = 0)"), (N//8, "slice a quarter-step up (z = a/8)"))):
    sl = (slice(None), slice(None), z)
    axs[row, 0].imshow(S[sl].T, origin="lower", cmap="Greys", extent=(0, a, 0, a)); axs[row, 0].set_title("solid (black) and gaps (white)\n" + lab, fontsize=9)
    for col, key, nm in ((1, "long", "network wavelength a/2"), (2, "medium", "half that, a/4")):
        F = D[key][sl]; im = axs[row, col].imshow(F.T, origin="lower", cmap="magma", extent=(0, a, 0, a))
        axs[row, col].contour(np.linspace(0, a, N), np.linspace(0, a, N), S[sl].T, levels=[0.5], colors="#4dd0e1", linewidths=0.8)
        axs[row, col].set_title(f"spherical waves, {nm}\ndark = cancelling; cyan = edges of the solid", fontsize=9)
for ax in axs.ravel(): ax.set_xticks([]); ax.set_yticks([])
fig.suptitle("Spherical-wave imaging of the cut-OG pyrochlore network: at the network's own wavelength the dark half lies wholly in the gaps", fontsize=11)
fig.text(0.5, 0.01, "DICTO · dictospheres.com · 5 Nov 2026", ha="center", fontsize=8, color="#555")
plt.savefig("wave-slices.png", dpi=120, bbox_inches="tight"); print("FINAL ok")
