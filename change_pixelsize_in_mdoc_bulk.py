#!/usr/bin/env python3
"""
Author: Alice-Roza Eruera, SBGrid Consortium 

Some mdoc files have the incorrect pixel size recorded in them. This 
sometimes happens when the nominal pixel size was printed to the mdoc
prior to microscope calibration. In cases where it's important to have 
the calibrated pixel size recorded in the mdoc, you need to change the pixel
size everywhere. 

#How to use: `python3 change_pixelsize_in_mdoc_bulk.py pixel_size *.mdoc`

""

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

    
