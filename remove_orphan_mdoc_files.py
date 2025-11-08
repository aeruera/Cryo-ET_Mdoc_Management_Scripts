"""
Author: Alice-Roza Eruera 01/08/2025

This script was written because we were processing a dataset where all the mdocs had been provided to us
but only some of the frame series were provided. We therefore had a folder with a mixture of orphaned mdocs
and mdocs associated with raw data. WarpTools will crash if you provide it with any orphaned mdocs. In this case, we 
had many that were mixed in. This script will search the mdoc folder and the frame series folder and remove any 
orphaned mdocs. 

It was written for use with an .eer dataset but it should work for any format.

TO USE: First, replace the two paths on lines 20 and 21. Then run the script in the terminal 
using `python3 remove_orphan_mdoc_files.py`.  

"""

import os
from pathlib import Path

# Set paths. Replace the paths with your own paths. 
eer_dir = Path("./testing_mdoc_script/")
mdoc_dir = Path("./testing_mdoc_script/")

# Collect base prefixes (before first underscore, or full stem if no underscore)
eer_prefixes = set()
for f in eer_dir.glob("*.eer"):
    stem = f.stem.split("_")[0]  # keep only part before first "_"
    eer_prefixes.add(stem)

mdoc_files = list(mdoc_dir.glob("*.mdoc"))

deleted = []

# Compare mdoc and tilt-series file names. If same, keep. If orphaned, delete.
for mdoc in mdoc_files:
    mdoc_prefix = mdoc.stem.split("_")[0]
    if mdoc_prefix not in eer_prefixes:
        print(f"Deleting: {mdoc}")
        mdoc.unlink() 
        deleted.append(mdoc.name)

print(f"\nDeleted {len(deleted)} extra mdoc files.")
