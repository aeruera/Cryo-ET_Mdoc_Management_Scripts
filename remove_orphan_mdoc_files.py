#Author: Alice-Roza Eruera 01/08/2025
#Delete mdocs from any subdirectories which do not have corresponding tilt-series
#For use in tidying raw data where there are orphaned mdoc files

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
