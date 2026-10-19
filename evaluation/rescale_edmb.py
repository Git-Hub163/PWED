#!/usr/bin/env python3


import os
import sys
import argparse
import glob
import numpy as np
from PIL import Image

# Prefer cv2, fallback to PIL+NumPy if unavailable
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    import scipy.io as sio
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def load_gt_sizes(gt_dir):
    """Scan GroundTruths/*.png and return a {filename_without_ext: (w, h)} dictionary."""
    gt_sizes = {}
    for p in glob.glob(os.path.join(gt_dir, "*.png")):
        with Image.open(p) as im:
          
            base_name = os.path.splitext(os.path.basename(p))[0]
            gt_sizes[base_name] = im.size  # (w, h)
    return gt_sizes


def resize_array(data, target_w, target_h):
    """Rescale a numpy array (h, w) to target_w x target_h."""
    if HAS_CV2:
        resized = cv2.resize(data, (target_w, target_h), interpolation=cv2.INTER_LINEAR)
    else:
        # PIL fallback
        if data.dtype == np.uint8:
            mode = "L"
        else:
            data_min, data_max = data.min(), data.max()
            if data_max > data_min:
                data = ((data - data_min) / (data_max - data_min) * 255).astype(np.uint8)
            else:
                data = np.zeros_like(data, dtype=np.uint8)
            mode = "L"
        im = Image.fromarray(data, mode=mode)
        im = im.resize((target_w, target_h), Image.BILINEAR)
        resized = np.array(im)
        if data.dtype != np.uint8 and data_max > data_min:
            resized = resized.astype(np.float32) / 255.0 * (data_max - data_min) + data_min
    return resized


def resize_image_file(src_path, target_w, target_h):
    """Rescale a single .png file and overwrite it."""
    im = Image.open(src_path)
    src_w, src_h = im.size
    if (src_w, src_h) == (target_w, target_h):
        return False
    im = im.resize((target_w, target_h), Image.BILINEAR)
    im.save(src_path)
    return True


def resize_mat_file(src_path, target_w, target_h, key="result"):
    """Rescale a single .mat file and overwrite it."""
    if not HAS_SCIPY:
        print("  [WARN] scipy is unavailable, skipping .mat files")
        return False
    data = sio.loadmat(src_path)
    arr = data[key]
    h, w = arr.shape[:2]
    if (w, h) == (target_w, target_h):
        return False
    resized = resize_array(arr, target_w, target_h)
    data[key] = resized
    sio.savemat(src_path, data, do_compression=True)
    return True


def process_edmb(edmb_dir, gt_sizes, key="result"):
    """Iterate through all scale subdirectories under EDMB, and rescale the files."""
    if not os.path.isdir(edmb_dir):
        print(f"[ERROR] EDMB directory does not exist: {edmb_dir}")
        return

    scales = sorted([
        d for d in os.listdir(edmb_dir)
        if os.path.isdir(os.path.join(edmb_dir, d))
        and not d.startswith(".")
        and os.path.isdir(os.path.join(edmb_dir, d, "mat"))
        and os.path.isdir(os.path.join(edmb_dir, d, "png"))
    ])

    if not scales:
        print(f"[ERROR] No scale subdirectories containing mat/ and png/ found under {edmb_dir}")
        return

    print(f"Found {len(scales)} scales: {scales}")
    print(f"Number of GroundTruth files: {len(gt_sizes)}")
    print()

    total_png_resized = 0
    total_mat_resized = 0

    for scale in scales:
        png_dir = os.path.join(edmb_dir, scale, "png")
        mat_dir = os.path.join(edmb_dir, scale, "mat")
        png_files = sorted(glob.glob(os.path.join(png_dir, "*.png")))
        mat_files = sorted(glob.glob(os.path.join(mat_dir, "*.mat")))

        scale_png = 0
        scale_mat = 0

        for png_path in png_files:
            fname = os.path.basename(png_path)
            base_name = os.path.splitext(fname)[0] 
            if base_name not in gt_sizes:
                print(f"  [WARN] {fname} has no corresponding match in GT, skipping")
                continue
            gt_w, gt_h = gt_sizes[base_name]
            if resize_image_file(png_path, gt_w, gt_h):
                scale_png += 1

        for mat_path in mat_files:
            fname = os.path.basename(mat_path)
            base_name = os.path.splitext(fname)[0] 
            if base_name not in gt_sizes:
                continue
            gt_w, gt_h = gt_sizes[base_name]
            if resize_mat_file(mat_path, gt_w, gt_h, key):
                scale_mat += 1

        total_png_resized += scale_png
        total_mat_resized += scale_mat
        if scale_png or scale_mat:
            print(f"  [{scale}] PNG rescaled: {scale_png}, MAT rescaled: {scale_mat}")

    print()
    print(f"=== Finished ===")
    print(f"Total PNGs rescaled: {total_png_resized}")
    print(f"Total MATs rescaled: {total_mat_resized}")


def main():
    parser = argparse.ArgumentParser(description="Rescale EDMB prediction maps to GroundTruth resolution")
    parser.add_argument("--edmb_dir", type=str, required=True, help="EDMB root directory")
    parser.add_argument("--gt_dir", type=str, required=True, help="GroundTruths directory")
    parser.add_argument("--key", type=str, default="result", help="Key in the .mat file (default: result)")
    args = parser.parse_args()

    gt_sizes = load_gt_sizes(args.gt_dir)
    process_edmb(args.edmb_dir, gt_sizes, args.key)


if __name__ == "__main__":
    main()