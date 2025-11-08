#Usage: python3 replace_subframepath_in_mdoc.py $file.mdoc $output_file.mdoc /path/to/frames 

import os, sys

inp, outp, newdir = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/\\")
with open(inp) as f, open(outp, "w") as g:
    for line in f:
        if line.startswith("SubFramePath"):
            fname = os.path.basename(line.split("=",1)[1].strip().replace("\\","/"))
            line = f"SubFramePath = {newdir}/{fname}\n"
        g.write(line)

