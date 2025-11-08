"""
Author: Alice Eruera, SBGrid Consortium

This script was written when a tomography software (which shall remain nameless) would crash
upon import because the subframes were not located at the absolute path provided under 
the Subframepath column of the mdocs. You can use this script to change the subframe path 
by providing it with the new path on your local machine. 

Usage: `python3 replace_subframepath_in_mdoc.py $input_file_name.mdoc $output_file_name.mdoc /path/to/frames`

"""

import os, sys

inp, outp, newdir = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/\\")
with open(inp) as f, open(outp, "w") as g:
    for line in f:
        if line.startswith("SubFramePath"):
            fname = os.path.basename(line.split("=",1)[1].strip().replace("\\","/"))
            line = f"SubFramePath = {newdir}/{fname}\n"
        g.write(line)

