#!/usr/bin/env python3
"""
convert_gt_to_mat.py - Convert GroundTruths/*.png to BSDS500 format .mat files.

Each GroundTruths/*.png is a boundary annotation for a single image, generating a .mat file 
of the same name. The 'groundTruth' variable contains the annotation itself as a single annotator.

The annotation maps are automatically thinned using bwmorph_thin (morphological thinning) 
during conversion to ensure the labels are a single pixel wide.
"""

import os
import sys
import glob
import argparse
import numpy as np
from PIL import Image

# Import bwmorph_thin (the same function used for evaluating prediction maps to ensure consistency)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "edge_eval_python", "impl"))
from bwmorph_thin import bwmorph_thin

try:
    import scipy.io as sio
except ImportError:
    print("ERROR: scipy is not installed. Please run: pip install scipy")
    sys.exit(1)


def load_boundary(png_path):
    """Load PNG boundary map, apply binarization and bwmorph_thin, return (H, W) boolean array."""
    im = Image.open(png_path).convert("L")
    binary = np.array(im) > 128
    thinned = bwmorph_thin(binary)
    return thinned


def convert_all(gt_dir, out_dir):
    png_files = sorted(glob.glob(os.path.join(gt_dir, "*.png")))
    os.makedirs(out_dir, exist_ok=True)

    print(f"Found {len(png_files)} ground truth PNG files")
    print("Applying bwmorph_thin to each label...")
    print()

    dt = np.dtype([("Segmentation", "O"), ("Boundaries", "O")])
    for png_path in png_files:
        name = os.path.basename(png_path)
        stem = os.path.splitext(name)[0]
        bnd = load_boundary(png_path)

        # groundTruth array with shape (1, 1)
        groundTruth = np.empty((1, 1), dtype=dt)
        groundTruth[0, 0] = (bnd, bnd)

        sio.savemat(
            os.path.join(out_dir, f"{stem}.mat"),
            {"groundTruth": groundTruth},
            do_compression=True,
        )

    print(f"Done: {len(png_files)} .mat files -> {out_dir}/")
    print("[Note] All labels have been thinned to single-pixel width via bwmorph_thin.")


def main():
    parser = argparse.ArgumentParser(
        description="Convert GroundTruths PNG boundary maps to BSDS format .mat files (automatically thinned)"
    )
    parser.add_argument("--gt_dir", type=str, required=True)
    parser.add_argument("--out_dir", type=str, default=None)
    args = parser.parse_args()

    if args.out_dir is None:
        if args.gt_dir in ("GroundTruths", "./GroundTruths"):
            args.out_dir = "GroundTruths_mat"
        else:
            args.out_dir = os.path.join(os.path.dirname(args.gt_dir.rstrip("/")), "GroundTruths_mat")

    convert_all(args.gt_dir, args.out_dir)


if __name__ == "__main__":
    main()