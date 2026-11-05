# Clean picture (DICTO 5 Nov 2026: "a dataless simplified version"): no titles, numbers or axes; solid beside its wave image, two slices.
import numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
D = np.load("wave-fields.npz"); S, a, N = D["S"], float(D["a"]), int(D["N"])
fig, axs = plt.subplots(2, 2, figsize=(8, 8), facecolor="#0b0b10"); plt.subplots_adjust(wspace=0.04, hspace=0.04)
for row, z in enumerate((0, N//8)):
    sl = (slice(None), slice(None), z)
    axs[row, 0].imshow(S[sl].T, origin="lower", cmap="copper")
    axs[row, 1].imshow(D["long"][sl].T, origin="lower", cmap="magma")
for ax in axs.ravel(): ax.axis("off")
fig.text(0.985, 0.01, "DICTO", ha="right", fontsize=8, color="#d9a521")
plt.savefig("wave-clean.png", dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor()); print("FINAL ok")
