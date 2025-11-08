#How to use:
#`python3 change_pixelsize_in_mdoc_bulk.py pixel_size *.mdoc`

#!/usr/bin/env python3
import sys
import os
import re

if len(sys.argv) < 3:
    print("Usage: python change_pixelsize_in_mdoc.py <new_pixel_size> *.mdoc")
    sys.exit(1)

newpix = sys.argv[1]
files = sys.argv[2:]

# Match only numeric pixel spacing, not filenames
pattern = re.compile(r"^PixelSpacing\s*=\s*[\d.+-eE]+")

for inp in files:
    outp = inp + ".tmp"
    with open(inp) as f, open(outp, "w") as g:
        for line in f:
            if pattern.match(line.strip()):
                line = f"PixelSpacing = {newpix}\n"
            g.write(line)
    os.replace(outp, inp)
    print(f"Updated {inp}")

    
