# /// script
# dependencies = ["numpy", "matplotlib"]
# ///
"""Objects lost vs central-veto radius, sims tile 233.293 (veto_cost outputs)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "/n17data/cdaley/scratch/dr6seg/veto_cost/out/sims_233.293_{}.npz"
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
ARMS = [("b_old", "neighbour pixels counted as defects", "#eb6834"),
        ("d_border", "this PR: neighbours never counted", "#2a78d6")]

plt.rcParams.update({"font.size": 11, "axes.edgecolor": INK2,
                     "axes.labelcolor": INK, "xtick.color": INK2,
                     "ytick.color": INK2})
fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=150)
for v, label, col in ARMS:
    z = np.load(D.format(v), allow_pickle=True)
    cf = [str(c) for c in z["configs"]]
    rs, pct, nlost = [], [], []
    for cfg in cf:
        fill, r = cfg.split(":")
        if fill != "noise":
            continue
        a = z["res"][:, cf.index(cfg)]
        ok = a[:, 0] >= 0
        lost = ok & (a[:, 0] > 0) & (a[:, 3] == 0)
        rs.append(int(r)); pct.append(100 * lost.sum() / ok.sum())
        nlost.append(lost.sum())
    ax.plot(rs, pct, "-o", color=col, lw=2, ms=7, mec="white", mew=1.5,
            label=label, zorder=3)
    ax.annotate(f"{pct[-1]:.2f}% ({nlost[-1]:,})" if pct[-1] < 1
                else f"{pct[-1]:.0f}% ({nlost[-1]:,})",
                (rs[-1], pct[-1]), xytext=(-8, 8 if pct[-1] < 1 else -4),
                textcoords="offset points", ha="right",
                va="bottom" if pct[-1] < 1 else "top", color=INK, fontsize=10)
ax.axvline(10, color=INK2, ls=":", lw=1)
ax.text(9.85, 33, "default\nradius", ha="right", va="top", color=INK2,
        fontsize=9)
ax.set_xlabel("central-veto radius  EPOCH_CENTRAL_DEFECT_RADIUS  [px]")
ax.set_ylabel("objects losing every epoch  [%]")
ax.set_xticks([0, 1, 3, 5, 10])
ax.set_ylim(-1, 35)
ax.grid(axis="y", color=GRID, lw=0.8)
ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(frameon=False, loc="upper left", fontsize=10)
ax.set_title("Simulated tile 233.293, 21,851 objects, noise fill",
             color=INK, fontsize=11, loc="left")
fig.tight_layout()
fig.savefig("/n17data/cdaley/tmp/fig922/922_object_loss.png")
