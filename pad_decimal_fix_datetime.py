"""

Author: Alice-Roza Eruera, SBGrid 

The DateTime column in mdoc files is recorded in 2-digit year format 
prior to 2023 and 4-digit year format after 2023 (to my understanding, SerialEM
made this change in an update at that time). Some software has problems parsing 
the mdoc file if the dateutil format is still in the 2-digit year...

At that time, they also changed how many decimal places are used. 


TO USE: Replace the input_path and output_paths with the paths to your mdocs. 
Then, execute the script by running in the terminal: `python3 pad_decimal_fix_datetime.py` 

"""


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


