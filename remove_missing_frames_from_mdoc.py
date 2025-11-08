#Usage: python3 remove_missing_frames_from_mdocs.py

"""
Remove blocks from mdoc if the referenced .eer file is missing.
Requires that the mdoc subframepath collumn points to the correct location.
Creates a .mdoc.bak file which is a copy of the original mdoc. 
New mdoc has correct name with erased blocks.
"""

#!/usr/bin/env python3
import os
import shutil
import glob

EER_FOLDER = "/nfs/hms/Sliz/aeruera/workshop/lisicki_data/PFIByeastTomos_MPIdortmund/frames"
MDOC_FILES = glob.glob("/nfs/hms/Sliz/aeruera/workshop/lisicki_data/PFIByeastTomos_MPIdortmund/mdoc/*.mdoc")

def clean_mdoc(mdoc_path, eer_folder):
    with open(mdoc_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    header = []
    blocks = []
    current_block = []
    in_block = False

    for line in lines:
        if line.lstrip().lower().startswith("[zvalue"):
            if current_block:
                blocks.append(current_block)
            current_block = [line]
            in_block = True
        else:
            if not in_block:
                header.append(line)
            else:
                current_block.append(line)
    if current_block:
        blocks.append(current_block)

    kept_blocks = []
    removed_count = 0

    for block in blocks:
        keep = True
        for i, line in enumerate(block):
            if line.lstrip().startswith("SubFramePath"):
                ref_path = line.split("=",1)[1].strip().strip('"').strip("'")
                filename = os.path.basename(ref_path)
                file_path = os.path.join(eer_folder, filename)
                if not os.path.exists(file_path):
                    keep = False
                    print(f"[REMOVE] {filename} missing")
        if keep:
            kept_blocks.append(block)
        else:
            removed_count += 1

    # Rename the backup copy of the original mdoc file
    backup = mdoc_path + ".bak"
    shutil.copy2(mdoc_path, backup)

    # move backup into orig_mdocs subdirectory
    orig_dir = os.path.join(os.path.dirname(backup), "orig_mdocs")
    os.makedirs(orig_dir, exist_ok=True)
    shutil.move(backup, os.path.join(orig_dir, os.path.basename(backup)))

    # write cleaned file
    with open(mdoc_path, 'w', encoding='utf-8') as f:
        f.writelines(header)
        for block in kept_blocks:
            f.writelines(block)

    print(f"✅ Cleaned {mdoc_path}: kept {len(kept_blocks)}, removed {removed_count}, backup: {backup}")

for mdoc in MDOC_FILES:
    if not os.path.isfile(mdoc):
        print(f"[WARN] mdoc not found: {mdoc}")
        continue
    clean_mdoc(mdoc, EER_FOLDER)
