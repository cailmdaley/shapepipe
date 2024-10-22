import sys
import numpy as np

from tqdm import tqdm


def main(argv):

    job = 32

    n_patch = 7
    patches = [f'P{x}' for x in np.arange(n_patch) + 1]

    missing = set()

    # Loop over patches
    for patch in tqdm(patches, desc="Loop over patches"):

    # Read in files from summary output with missing CCDs.
    # Create and update CCD name set.
        fname = f"{patch}/summary/missing_job_{job}_all.txt"
        with open(fname) as f:
            lines = f.readlines()
        for line in lines:
            missing.update([line.rstrip("\n")])

    print(missing)

    # Read in exposure name files.
    # Create and update CCD name set.

    # Combine above to create used CCD name set.


if __name__ == "__main__":
    sys.exit(main(sys.argv))
