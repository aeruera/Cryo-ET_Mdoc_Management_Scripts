# -*- coding: utf-8 -*-

"""

Created on Wed Sep  3 11:02:49 2025



@author: alice

"""

# Fix mdoc file so that the DateTime column is in 4-digit year format 

# Make sure all values with decimals are 2-digit decimal placeholders 



import re

from pathlib import Path



# Input and output files

input_file = Path(r"/nfs/hms/Sliz/aeruera/mdoc_conversion/converted.mdoc")

output_file = Path(r"/nfs/hms/Sliz/aeruera/mdoc_conversion/converted_padded.mdoc")



def pad_decimals(text: str, digits=2) -> str:

    """Pad numbers with decimals to a fixed number of digits (leave integers as-is)."""

    number_pattern = re.compile(r"-?\d+(\.\d+)?")



    def fmt(match):

        val = match.group(0)

        if "." in val:

            decimals = len(val.split(".")[1])

            if decimals < digits:

                return f"{float(val):.{digits}f}"

            else:

                return val  # already has enough decimals

        else:

            return val  # integer, leave unchanged



    return number_pattern.sub(fmt, text)



def fix_datetime_years(text: str) -> str:

    """Convert 2-digit years in DateTime fields to 4-digit years (assumes 2000s)."""

    date_pattern = re.compile(r"(DateTime\s*=\s*\d{2}-[A-Za-z]{3}-)(\d{2})(\s+\d{2}:\d{2}:\d{2})")

    return date_pattern.sub(lambda m: f"{m.group(1)}20{m.group(2)}{m.group(3)}", text)



if __name__ == "__main__":

    # Read input file

    with open(input_file, "r") as f:

        text = f.read()



    # Apply both transformations

    text = fix_datetime_years(text)

    text = pad_decimals(text, digits=2)



    # Write to output file

    with open(output_file, "w") as f:

        f.write(text)



    print("All DateTime 2-digit years converted and decimals padded.")


