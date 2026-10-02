"""m and c vs defect distance for both DEFECT_FILLs, via tests/helpers/defect_response.

Run from the shapepipe worktree root inside the container:
  PYTHONPATH=src:. python bias_scan.py out.json NPROC
"""
import json
import sys
from multiprocessing import Pool

import numpy as np

from tests.helpers.defect_response import defect_response

N, C = 51, 25
import os

KINDS = tuple(os.environ.get("KINDS", "column,bleed,pixel").split(","))
FILLS = tuple(os.environ.get("FILLS", "noise,interpolate").split(","))
DISTS = range(int(os.environ.get("DMIN", 3)), int(os.environ.get("DMAX", 15)))
HLR = float(os.environ.get("HLR", 0.5))
PSF = float(os.environ.get("PSF", 0.7))


def geometry(kind, d):
    bad = np.zeros((N, N), dtype=bool)
    if kind == "pixel":
        bad[C, C + d] = True
    elif kind == "column":
        bad[:, C + d] = True
    elif kind == "bleed":
        bad[:, C + d:C + d + 3] = True
    return bad


def one(args):
    kind, fill, d = args
    try:
        r = defect_response(geometry(kind, d), hlr=HLR, psf=PSF,
                            seeds=range(6),
                            options={"defect_fill": fill})
        return dict(kind=kind, fill=fill, d=d, hlr=HLR, psf=PSF, m=r["m"], m_err=r["m_err"],
                    c=r["c"].tolist() if hasattr(r["c"], "tolist") else r["c"],
                    c_err=r["c_err"])
    except Exception as e:  # noqa: BLE001
        return dict(kind=kind, fill=fill, d=d, error=repr(e))


if __name__ == "__main__":
    jobs = [(k, f, d) for k in KINDS for f in FILLS for d in DISTS]
    with Pool(int(sys.argv[2])) as p:
        out = p.map(one, jobs, chunksize=1)
    json.dump(out, open(sys.argv[1], "w"), indent=1)
