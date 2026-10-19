#!/usr/bin/env python3
"""
png_to_mat.py - Converts predicted PNG images to .mat format readable by edge_eval_python.

Reads grayscale PNG -> normalizes to [0,1] float32 -> saves as .mat (key="result").

Usage:
    # RCF (black lines on white background, requires inversion)
    python png_to_mat.py --png_dir ./RCF --out_dir ./RCF_mat --invert

    # Others (white lines on black background, no inversion required)
    python png_to_mat.py --png_dir ./PRED_DIR --out_dir ./OUT_DIR
"""

import os
import sys
import glob
import argparse
import numpy as np
from PIL import Image

try:
    import scipy.io as sio
except ImportError:
    print("ERROR: scipy is not installed. Please run: pip install scipy")
    sys.exit(1)


def convert(png_dir, out_dir, key="result", invert=False):
    png_files = sorted(glob.glob(os.path.join(png_dir, "*.png")))
    if not png_files:
        print(f"[ERROR] No .png files found in {png_dir}")
        return

    os.makedirs(out_dir, exist_ok=True)

    for png_path in png_files:
        name = os.path.basename(png_path)
        stem = os.path.splitext(name)[0]
        im = np.array(Image.open(png_path).convert("L"), dtype=np.float32) / 255.0
        if invert:
            im = 1.0 - im  # White background/black lines -> Black background/white lines (high value = edge)
        out_path = os.path.join(out_dir, f"{stem}.mat")
        sio.savemat(out_path, {key: im}, do_compression=True)

    print(f"Done: {len(png_files)} .mat files -> {out_dir}/")


def main():
    parser = argparse.ArgumentParser(description="Convert PNG prediction maps to .mat format")
    parser.add_argument("--png_dir", type=str, required=True)
    parser.add_argument("--out_dir", type=str, required=True)
    parser.add_argument("--key", type=str, default="result")
    parser.add_argument("--invert", action="store_true",
                        help="Invert colors: white background/black lines -> black background/white lines")
    args = parser.parse_args()
    convert(args.png_dir, args.out_dir, args.key, args.invert)


if __name__ == "__main__":
    main()