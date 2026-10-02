# /// script
# dependencies = ["numpy", "matplotlib"]
# ///
"""Worst-axis |m| and |c| vs defect distance, both DEFECT_FILLs."""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

D = "/n17data/cdaley/tmp/fig922/"
rows = json.load(open(D + "bias_scan.json")) + json.load(open(D + "bias_scan_big.json"))
INK, INK2, GRID, FAIL = "#0b0b0b", "#52514e", "#e4e3df", "#f6e3dc"
SERIES = [  # (kind, hlr, label, colour, linestyle)
    ("column", 0.5, "bad column", "#2a78d6", "-"),
    ("bleed", 0.5, "3-px bleed", "#eb6834", "-"),
    ("pixel", 0.5, "single pixel", "#1baf7a", "-"),
    ("bleed", 0.7, "3-px bleed, 0.7″ galaxy, 0.9″ PSF", "#eb6834", (0, (3, 2))),
]
FILLS = [("noise", "DEFECT_FILL = noise", 10, "EPOCH_CENTRAL_DEFECT_RADIUS = 10"),
         ("interpolate", "DEFECT_FILL = interpolate", 7,
          "EPOCH_INTERPOLATED_DEFECT_RADIUS = 7")]
plt.rcParams.update({"font.size": 10, "axes.edgecolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2,
                     "axes.labelcolor": INK})
fig, axs = plt.subplots(2, 2, figsize=(10, 6.4), dpi=150, sharex=True,
                        sharey="row", gridspec_kw=dict(hspace=0.12, wspace=0.06))
for j, (fill, title, radius, rlabel) in enumerate(FILLS):
    for i, (q, bound, ylabel) in enumerate([
            ("m", 1.0, "worst |m|  [%]"), ("c", 5e-4, "worst |c|")]):
        ax = axs[i, j]
        ax.axhspan(bound, 1e3, color=FAIL, zorder=0, lw=0)
        ax.axhline(bound, color=INK2, lw=0.8, zorder=1)
        ax.axvline(radius, color=INK, ls=":", lw=1.2, zorder=1)
        for kind, hlr, label, col, ls in SERIES:
            sel = sorted((r for r in rows if r["kind"] == kind
                          and r["fill"] == fill and r.get("hlr", 0.5) == hlr),
                         key=lambda r: r["d"])
            d = [r["d"] for r in sel]
            v = [max(abs(x) for x in r[q]) * (100 if q == "m" else 1)
                 for r in sel]
            ax.plot(d, v, color=col, ls=ls, lw=2, marker="o", ms=4,
                    label=label, zorder=3)
        ax.set_yscale("log")
        ax.set_ylim((5e-3, 200) if q == "m" else (1e-6, 0.3))
        ax.grid(axis="y", color=GRID, lw=0.6, which="major")
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
        if j == 0:
            ax.set_ylabel(ylabel)
        if i == 0:
            ax.set_title(title, color=INK, fontsize=11, loc="left")
            ax.text(radius + 0.2, 100, rlabel.split(" = ")[1] + " px veto",
                    color=INK, fontsize=9, va="top")
        ax.text(16.4, bound * 1.25,
                "|m| > 1%" if q == "m" else "|c| > 5e-4",
                color="#a8462a", fontsize=8.5, ha="right", va="bottom")
fig.supxlabel("distance of the defect's nearest pixel from the object centre  [px]",
              fontsize=10, color=INK, y=0.035)
h, l = axs[0, 0].get_legend_handles_labels()
fig.legend(h, l, frameon=False, fontsize=9.5, ncol=4, loc="lower center",
           bbox_to_anchor=(0.5, -0.03))
fig.text(0.5, 0.955, "Shear bias from one defect, 0.5″ galaxy through a 0.7″ PSF "
         "(dashed: 0.7″ galaxy, 0.9″ PSF); worst of axes 1, 2",
         ha="center", color=INK2, fontsize=9.5)
fig.savefig(D + "922_bias_vs_distance.png", bbox_inches="tight")
