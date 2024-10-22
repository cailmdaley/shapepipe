### sqlite_get_ccd_names.py

# Extract names of single-exposure single-HDU (CCD) names
# from sqlite PSF interpolation information file.



import sys
import glob
from tqdm import tqdm

from sqlitedict import SqliteDict


def get_ccds_from_file(fname):
    """Return set of CCD names from sqlite file.
    """

    # Open sqlite file
    psf_vign_cat = SqliteDict(fname)
    
    # Initialise set of CCD names
    ccds = set()

    # Lazy iteration (do not store list in variable).
    # Keys in postage stamp file are object (galaxy) IDs for which
    # the PSF postage stamp is used elsehere,
    for obj_ID in tqdm(psf_vign_cat.keys(), desc=f"Processing {fname}"):

        # If vignet is not empty, add all used CCDs (=keys) to name set
        if psf_vign_cat[obj_ID] != "empty":
            ccds.update(psf_vign_cat[obj_ID].keys())

    return set(ccds)


def get_all_ccds(filenames):
    """Return set of CCD names from list of sqlite files.
    """

    all_ccds = set()
    for fname in tqdm(filenames, desc="Overall progress"):
        all_ccds.update(get_ccds_from_file(fname))
    return all_ccds


def main(argv):

    filenames = glob.glob("tile_runs/077.32?/output/run_sp_tile_PsViSmVi_202*/psfex_interp_runner/output/galaxy_psf-???-???.sqlite")

    print(len(filenames))

    all_ccds = get_all_ccds(filenames)
    print(all_ccds)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
    

