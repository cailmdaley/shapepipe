"""One synthetic epoch through prepare_ngmix_weights under three settings.

Run from the shapepipe worktree root inside the container:
  PYTHONPATH=src python stamp_demo.py out.npz
"""
import sys

import numpy as np

from shapepipe.modules.ngmix_package.ngmix import (
    OFF_TILE_FLAG,
    prepare_ngmix_weights,
)

N, C = 51, 25
rng = np.random.RandomState(4)
yy, xx = np.indices((N, N))


def blob(r0, c0, sigma, flux, q=1.0, theta=0.0):
    dy, dx = yy - r0, xx - c0
    ct, st = np.cos(theta), np.sin(theta)
    u, v = ct * dx + st * dy, -st * dx + ct * dy
    r = np.sqrt(u ** 2 + (v / q) ** 2)
    return flux * np.exp(-r / sigma) / (2 * np.pi * sigma ** 2 * q)


rms = 1.0
target = blob(C, C, 2.2, 3000, q=0.7, theta=0.5)
nbr = blob(C - 10, C - 11, 2.0, 4000, q=0.8, theta=-0.3)
gal = target + nbr + rng.normal(0, rms, (N, N))

# Segmentation: each pixel above 2 sigma joins the brighter profile there.
above = (target + nbr) > 2 * rms
seg = np.where(above, np.where(target >= nbr, 1, 2), 0).astype(np.int32)
neighbour = seg == 2              # the tile VIGNET's -1e30 neighbour markers

flag = np.zeros((N, N), np.int32)
flag[:, C + 12] = 1               # bad column, 12 px right of centre
flag[C + 9, C - 9] = 1            # hot pixel, 12.7 px from centre
flag[N - 5:, :] = OFF_TILE_FLAG   # off-tile band at the stamp's lower edge
gal[:, C + 12] = 400.0
gal[C + 9, C - 9] = 400.0
weight = np.ones((N, N))
bkg_rms = np.full((N, N), rms)

out = dict(gal=gal, seg=seg, neighbour=neighbour, flag=flag)
for name, kw in {
    "noisefill_noise": dict(blend_handling="noisefill", defect_fill="noise"),
    "uberseg_noise": dict(blend_handling="uberseg", defect_fill="noise",
                          seg=seg, object_number=1),
    "noisefill_interpolate": dict(blend_handling="noisefill",
                                  defect_fill="interpolate"),
}.items():
    img, w, _ = prepare_ngmix_weights(
        gal, weight, flag, np.random.RandomState(1), bkg_rms=bkg_rms,
        neighbour=neighbour, **kw,
    )
    out[name + "_img"], out[name + "_w"] = img, w
np.savez(sys.argv[1], **out)
print({k: v.shape for k, v in out.items()})
