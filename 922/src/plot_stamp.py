# /// script
# dependencies = ["numpy", "matplotlib", "scipy"]
# ///
"""One epoch's stamp: pixel classes, and what ngmix sees under three settings."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle, Patch

z = np.load("/n17data/cdaley/tmp/fig922/stamp_demo.npz")
INK, INK2 = "#0b0b0b", "#52514e"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
N, C = 51, 25

def stretch(a):
    return np.arcsinh(a / 3.0)

vmin, vmax = stretch(-3), stretch(120)
plt.rcParams.update({"font.size": 10})
fig, axs = plt.subplots(2, 4, figsize=(11, 5.9), dpi=150,
                        gridspec_kw=dict(hspace=0.08, wspace=0.05))

def clean(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color(INK2); s.set_linewidth(0.6)

# Column 0: the exposure, and its pixel classes.
ax = axs[0, 0]
ax.imshow(stretch(z["gal"]), origin="lower", cmap="gray_r", vmin=vmin,
          vmax=vmax, interpolation="nearest")
ax.set_title("one epoch's stamp\n", color=INK, fontsize=11)
fig.text(0.62, 0.995, "what ngmix sees under  BLEND_HANDLING + DEFECT_FILL",
         ha="center", va="bottom", color=INK, fontsize=11)
ax.set_ylabel("image", color=INK, fontsize=11)
ax = axs[1, 0]
cls = np.zeros((N, N), int)
cls[z["neighbour"]] = 1
cls[(z["flag"] > 0) & (z["flag"] < 1024)] = 2
cls[z["flag"] == 1024] = 3
cls[z["seg"] == 1] = np.where(cls[z["seg"] == 1] == 0, 4, cls[z["seg"] == 1])
cmap = ListedColormap(["#f4f3ef", BLUE, ORANGE, AQUA, "#c3c2b7"])
ax.imshow(cls, origin="lower", cmap=cmap, vmin=-0.5, vmax=4.5,
          interpolation="nearest")
for r, ls, lab in ((10, "--", "10 px"), (7, ":", "7 px")):
    ax.add_patch(Circle((C, C), r, fill=False, ec=INK, ls=ls, lw=1.1))
ax.text(C, C + 10.8, "10 px", ha="center", va="bottom", fontsize=8, color=INK)
ax.text(C, C - 6.3, "7 px", ha="center", va="bottom", fontsize=8, color=INK)
ax.set_ylabel("pixel class / weight", color=INK, fontsize=11)
ax.legend(handles=[
    Patch(color="#c3c2b7", label="target footprint"),
    Patch(color=BLUE, label="neighbour (−1e30 in tile)"),
    Patch(color=ORANGE, label="defect (flag / weight / RMS)"),
    Patch(color=AQUA, label="off-tile (a defect)"),
], loc="upper center", bbox_to_anchor=(2.05, -0.03), ncol=4, frameon=False,
    fontsize=9.5, handlelength=1.2)

panels = [
    ("noisefill_noise", "noisefill + noise\n(the defaults)"),
    ("uberseg_noise", "uberseg + noise\n"),
    ("noisefill_interpolate", "noisefill + interpolate\n"),
]
for j, (key, title) in enumerate(panels, start=1):
    ax = axs[0, j]
    ax.imshow(stretch(z[key + "_img"]), origin="lower", cmap="gray_r",
              vmin=vmin, vmax=vmax, interpolation="nearest")
    ax.set_title(title, color=INK, fontsize=10)
    ax = axs[1, j]
    w = z[key + "_w"]
    ax.imshow(w > 0, origin="lower", cmap=ListedColormap(["#3a3a38", "#f4f3ef"]),
              vmin=0, vmax=1, interpolation="nearest")
for ax in axs.flat:
    clean(ax)
axs[1, 3].text(N - 1, 1, "dark = zero weight", ha="right", va="bottom",
               fontsize=8.5, color="white",
               bbox=dict(fc="#3a3a38", ec="none", pad=1.5))
fig.savefig("/n17data/cdaley/tmp/fig922/922_pixel_classes.png",
            bbox_inches="tight")
