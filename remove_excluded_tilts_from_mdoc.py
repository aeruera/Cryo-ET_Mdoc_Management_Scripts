#!/usr/bin/env python3

"""
remove_excluded_tilts_from_mdoc.py

Remove full [ZValue] tilt blocks from SerialEM .mdoc files when their
SubFramePath filename matches a filename listed in an exclusion list.

This script DOES NOT overwrite the original .mdoc files. It writes cleaned
copies into a separate output directory.

Example:
    python remove_excluded_tilts_from_mdoc.py data/*.mdoc \
        --exclude exclude_list.txt \
        --out clean_mdocs

Example exclude_list.txt:
    data/HeLa_end_4hGTPP_139_170_42.0_Oct19.mrc
"""

import argparse
from pathlib import Path


def read_exclude_list(path):
    excluded = set()

    with open(path, "r") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            excluded.add(Path(line.replace("\\", "/")).name)

    return excluded


def split_mdoc(lines):
    header = []
    blocks = []
    current = None

    for line in lines:
        if line.startswith("[ZValue"):
            if current is not None:
                blocks.append(current)
            current = [line]
        elif current is None:
            header.append(line)
        else:
            current.append(line)

    if current is not None:
        blocks.append(current)

    return header, blocks


def get_subframe_name(block):
    for line in block:
        if line.strip().startswith("SubFramePath"):
            value = line.split("=", 1)[1].strip()
            return Path(value.replace("\\", "/")).name

    return None


def clean_mdoc(mdoc_path, excluded_names, outdir):
    lines = mdoc_path.read_text().splitlines()
    header, blocks = split_mdoc(lines)

    kept_blocks = []
    removed = []

    for block in blocks:
        subframe_name = get_subframe_name(block)

        if subframe_name in excluded_names:
            removed.append(subframe_name)
        else:
            kept_blocks.append(block)

    output_lines = list(header)

    for block in kept_blocks:
        output_lines.extend(block)

    outpath = outdir / mdoc_path.name

    if outpath.resolve() == mdoc_path.resolve():
        raise RuntimeError(f"Refusing to overwrite input file: {mdoc_path}")

    outpath.write_text("\n".join(output_lines) + "\n")

    return outpath, removed


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Remove [ZValue] tilt blocks from SerialEM .mdoc files when the "
            "SubFramePath filename matches an entry in an exclusion list. "
            "Original .mdoc files are never overwritten."
        )
    )

    parser.add_argument(
        "mdocs",
        nargs="+",
        help="Input .mdoc file(s), e.g. data/*.mdoc"
    )

    parser.add_argument(
        "--exclude",
        required=True,
        help=(
            "Text file containing frames to remove, one per line. Paths are OK; "
            "only the filename is matched."
        )
    )

    parser.add_argument(
        "--out",
        required=True,
        help="Output directory for cleaned .mdoc copies."
    )

    args = parser.parse_args()

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    excluded_names = read_exclude_list(args.exclude)

    if not excluded_names:
        raise RuntimeError("Exclude list is empty.")

    for mdoc in args.mdocs:
        mdoc_path = Path(mdoc)

        if not mdoc_path.exists():
            raise FileNotFoundError(f"Input file does not exist: {mdoc_path}")

        outpath, removed = clean_mdoc(mdoc_path, excluded_names, outdir)

        if removed:
            print(f"{mdoc_path} -> {outpath}")
            for name in removed:
                print(f"  removed: {name}")
        else:
            print(f"{mdoc_path} -> {outpath}")
            print("  removed: none")


if __name__ == "__main__":
    main()
