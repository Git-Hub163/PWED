#!/usr/bin/env python3
"""
Run EDTER prediction evaluation on the server.

This script does not modify original EDTER predictions or GroundTruth files.
It writes converted predictions, GT .mat samples, NMS output, and metrics under
EDTER_eval_run/ by default.
"""

import argparse
import random
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import io as sio


def ensure_imports(root):
    edge_eval_dir = root / "edge_eval_python"
    if not edge_eval_dir.is_dir():
        raise FileNotFoundError(f"Missing edge_eval_python directory: {edge_eval_dir}")
    sys.path.insert(0, str(edge_eval_dir))
    from nms_process import nms_process
    from impl.bwmorph_thin import bwmorph_thin
    from impl.edges_eval_dir import edges_eval_dir
    return nms_process, bwmorph_thin, edges_eval_dir


def clean_dir(path):
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def squeeze_boundary(value):
    arr = np.asarray(value)
    while arr.dtype == object and arr.size == 1:
        arr = np.asarray(arr.item())
    return np.squeeze(arr)


def load_gt_boundaries(mat_path):
    mat = sio.loadmat(mat_path)
    if "groundTruth" not in mat:
        raise KeyError(f"{mat_path} does not contain key 'groundTruth'")

    gt = mat["groundTruth"]
    boundaries = []
    for entry in np.ravel(gt):
        item = entry.item() if hasattr(entry, "item") else entry
        boundary = None

        if isinstance(item, tuple) and len(item) >= 2:
            boundary = item[1]
        elif hasattr(item, "dtype") and item.dtype.names and "Boundaries" in item.dtype.names:
            boundary = item["Boundaries"]
        elif isinstance(item, dict) and "Boundaries" in item:
            boundary = item["Boundaries"]

        if boundary is None:
            raise ValueError(f"Cannot read Boundaries from {mat_path}")

        boundaries.append(squeeze_boundary(boundary).astype(bool))

    return boundaries


def save_bool_png(array, out_path):
    out = (array.astype(np.uint8) * 255)
    Image.fromarray(out).save(out_path)


def export_gt_samples(gt_mat_dir, gt_png_dir, out_dir, sample_count, seed, bwmorph_thin):
    mat_files = sorted(gt_mat_dir.glob("*.mat"))
    if not mat_files:
        raise FileNotFoundError(f"No .mat files found in {gt_mat_dir}")

    random.seed(seed)
    selected = random.sample(mat_files, min(sample_count, len(mat_files)))
    sample_dir = out_dir / "gt_mat_samples"
    sample_dir.mkdir(parents=True, exist_ok=True)

    report_lines = [
        "name,before_pixels,after_thin_pixels,changed_pixels,density,mat_png,thin_again_png,source_gt_png"
    ]
    for mat_path in selected:
        boundaries = load_gt_boundaries(mat_path)
        boundary = boundaries[0]
        thinned_again = bwmorph_thin(boundary)
        changed = np.logical_xor(boundary, thinned_again)

        stem = mat_path.stem
        mat_png = sample_dir / f"{stem}_mat_boundaries.png"
        thin_png = sample_dir / f"{stem}_after_thin_again.png"
        source_png_out = ""
        save_bool_png(boundary, mat_png)
        save_bool_png(thinned_again, thin_png)

        source_png = gt_png_dir / f"{stem}.png"
        if source_png.is_file():
            source_png_out = str(sample_dir / f"{stem}_source_gt.png")
            Image.open(source_png).convert("L").save(source_png_out)

        density = float(np.count_nonzero(boundary)) / float(boundary.size)
        report_lines.append(
            f"{stem},{np.count_nonzero(boundary)},{np.count_nonzero(thinned_again)},"
            f"{np.count_nonzero(changed)},{density:.8f},{mat_png},{thin_png},{source_png_out}"
        )

    report_path = sample_dir / "sample_report.csv"
    report_path.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    return sample_dir, report_path


def convert_predictions(pred_dir, out_mat_dir, pred_mode):
    png_files = sorted(pred_dir.glob("*.png"))
    if not png_files:
        raise FileNotFoundError(f"No .png prediction files found in {pred_dir}")

    out_mat_dir.mkdir(parents=True, exist_ok=True)
    inverted = 0
    for png_path in png_files:
        image = np.asarray(Image.open(png_path).convert("L"), dtype=np.float32) / 255.0

        if pred_mode == "auto":
            invert = float(image.mean()) > 0.5
        elif pred_mode == "edge_black":
            invert = True
        elif pred_mode == "edge_white":
            invert = False
        else:
            raise ValueError(f"Unknown pred mode: {pred_mode}")

        if invert:
            image = 1.0 - image
            inverted += 1

        sio.savemat(out_mat_dir / f"{png_path.stem}.mat", {"result": image.astype(np.float32)}, do_compression=True)

    return len(png_files), inverted


def check_prediction_gt_match(pred_mat_dir, gt_mat_dir):
    pred_stems = {p.stem for p in pred_mat_dir.glob("*.mat")}
    gt_stems = {p.stem for p in gt_mat_dir.glob("*.mat")}
    missing = sorted(gt_stems - pred_stems)
    extra = sorted(pred_stems - gt_stems)
    if missing:
        preview = ", ".join(missing[:10])
        raise FileNotFoundError(
            f"{len(missing)} GT files have no matching prediction .mat. First missing: {preview}"
        )
    return len(gt_stems), len(extra)


def read_metrics(eval_file):
    values = np.loadtxt(eval_file, dtype=np.float64).reshape(-1)
    return {
        "ODS_T": values[0],
        "ODS_R": values[1],
        "ODS_P": values[2],
        "ODS": values[3],
        "OIS_R": values[4],
        "OIS_P": values[5],
        "OIS": values[6],
        "AP": values[7],
    }


def main():
    parser = argparse.ArgumentParser(description="Convert EDTER PNG predictions, run NMS, and evaluate ODS/OIS/AP.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Project root containing EDTER and GroundTruths_mat")
    parser.add_argument("--pred_dir", type=Path, default=Path("EDTER"), help="EDTER PNG prediction directory")
    parser.add_argument("--gt_mat_dir", type=Path, default=Path("GroundTruths_mat"), help="GT .mat directory")
    parser.add_argument("--gt_png_dir", type=Path, default=Path("GroundTruths"), help="Original GT PNG directory")
    parser.add_argument("--out_dir", type=Path, default=Path("EDTER_eval_run"), help="Output directory")
    parser.add_argument("--model_name", type=str, default="EDTER", help="Model name used inside NMS output")
    parser.add_argument("--pred_mode", choices=["auto", "edge_white", "edge_black"], default="auto")
    parser.add_argument("--workers", type=int, default=-1)
    parser.add_argument("--thrs", type=int, default=99)
    parser.add_argument("--sample_count", type=int, default=2)
    parser.add_argument("--seed", type=int, default=20260714)
    parser.add_argument("--clean", action="store_true", help="Remove previous out_dir before running")
    args = parser.parse_args()

    root = args.root.resolve()
    pred_dir = (root / args.pred_dir).resolve()
    gt_mat_dir = (root / args.gt_mat_dir).resolve()
    gt_png_dir = (root / args.gt_png_dir).resolve()
    out_dir = (root / args.out_dir).resolve()

    if args.clean:
        clean_dir(out_dir)
    else:
        out_dir.mkdir(parents=True, exist_ok=True)

    nms_process, bwmorph_thin, edges_eval_dir = ensure_imports(root)

    pred_mat_dir = out_dir / "pred_mat"
    nms_dir = out_dir / "nms"
    if args.clean:
        pred_mat_dir.mkdir(parents=True, exist_ok=True)
        nms_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] Exporting {args.sample_count} random GT .mat visualizations...")
    sample_dir, report_path = export_gt_samples(
        gt_mat_dir, gt_png_dir, out_dir, args.sample_count, args.seed, bwmorph_thin
    )
    print(f"      samples: {sample_dir}")
    print(f"      report : {report_path}")

    print("[2/4] Converting EDTER PNG predictions to .mat with key='result'...")
    converted, inverted = convert_predictions(pred_dir, pred_mat_dir, args.pred_mode)
    print(f"      converted: {converted} files")
    print(f"      inverted : {inverted} files (pred_mode={args.pred_mode})")

    matched, extra = check_prediction_gt_match(pred_mat_dir, gt_mat_dir)
    print(f"      matched GT/prediction pairs: {matched}")
    if extra:
        print(f"      note: {extra} prediction files do not have GT and will not be evaluated")

    print("[3/4] Running NMS...")
    nms_process(args.model_name, str(pred_mat_dir), str(nms_dir), key="result", file_format=".mat")
    nms_model_dir = nms_dir / args.model_name
    print(f"      nms output: {nms_model_dir}")

    print("[4/4] Evaluating ODS/OIS/AP...")
    edges_eval_dir(str(nms_model_dir), str(gt_mat_dir), thrs=args.thrs, max_dist=0.0075, thin=True, workers=args.workers)
    eval_dir = Path(f"{nms_model_dir}-eval")
    eval_file = eval_dir / "eval_bdry.txt"
    metrics = read_metrics(eval_file)

    summary = [
        f"eval_file={eval_file}",
        f"ODS={metrics['ODS']:.6f}",
        f"OIS={metrics['OIS']:.6f}",
        f"AP={metrics['AP']:.6f}",
        f"ODS_T={metrics['ODS_T']:.6f}",
        f"ODS_R={metrics['ODS_R']:.6f}",
        f"ODS_P={metrics['ODS_P']:.6f}",
        f"OIS_R={metrics['OIS_R']:.6f}",
        f"OIS_P={metrics['OIS_P']:.6f}",
    ]
    summary_path = out_dir / "summary.txt"
    summary_path.write_text("\n".join(summary) + "\n", encoding="utf-8")

    print("[RESULT]")
    for line in summary:
        print(f"      {line}")
    print(f"      summary: {summary_path}")


if __name__ == "__main__":
    main()
