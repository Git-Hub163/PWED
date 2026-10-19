# PWED Boundary Evaluation: ODS, OIS, and AP

This directory contains the supplied evaluation entry point, the locally modified `edge_eval_python` implementation, conversion helpers, three PNG annotations, and their corresponding pre-thinned `.mat` labels. The entry point retains its historical name, `run_edter_eval.py`, but accepts prediction directories and model names for other detectors.

**Execution platform:** Linux cloud server. Repository preparation on Windows does not run inference, convert labels, or compute metrics. The commands below have been reconciled with the source and the author's supplied command; a fresh server run of this repository snapshot is still required.

## 1. Install and Build on the Server

Run in the evaluation environment on Linux, after cloning the repository:

```bash
cd /root/PWED/evaluation
python -m pip install -r requirements.txt
mkdir -p edge_eval_python/cxx/lib
(cd edge_eval_python/cxx/src && bash build.sh)
```

Replace `/root/PWED` with the actual clone location. The native build requires `g++` and creates `edge_eval_python/cxx/lib/solve_csa.so`. This library is still required for NMS and is loaded at import time by the supplied modules, even though boundary correspondence uses the greedy matcher. Build from the supplied sources; machine-specific binaries are excluded from Git. The requirements file lists direct dependencies, not the unknown original server package versions. Export that server's actual versions before a final reproducible release.

## 2. Inputs

- `GroundTruths/*.png`: the three supplied PNG boundary annotations.
- `GroundTruths_mat/*.mat`: matching MATLAB files with the `groundTruth` variable and `Boundaries` field, already thinned according to the authors.
- A prediction directory such as `U2Net/`: grayscale confidence PNGs, one per supplied `.mat` stem, with the same height and width.

The included `.mat` stems are `A_2007_0`, `A_2007_0-1`, and `A_2007_0-2`. All ground-truth `.mat` files in the selected directory must have matching predictions. The current `U2Net/` directory is empty, so it is not included in Git and **the example needs predictions before it can run**. U2Net is a command example supplied by the authors, not an addition to the six baselines.

The entry point does not strip `_thin` suffixes, transpose arrays, or resize predictions. Any method-specific filename or geometry preparation must be declared and performed separately on the server.

## 3. Run on the Included Ground-Truth Subset

After placing matching predictions in `evaluation/U2Net/`:

```bash
cd /root/PWED/evaluation
python run_edter_eval.py \
  --root . \
  --pred_dir U2Net \
  --gt_mat_dir GroundTruths_mat \
  --gt_png_dir GroundTruths \
  --out_dir U2Net_eval_run \
  --model_name U2Net \
  --pred_mode auto \
  --workers -1 \
  --thrs 99 \
  --clean
cat U2Net_eval_run/summary.txt
```

`--clean` deletes and recreates the selected output directory. Use a dedicated output folder. A clean run prevents reuse of stale intermediate predictions, NMS images, or cached metric files. `--workers -1` uses the available CPU cores for threshold processing.

The author's existing server layout remains usable when the same code and matching inputs are under `/root/ping_gu`:

```bash
cd /root/ping_gu
rm -rf -- edge_eval_python/impl/__pycache__
python run_edter_eval.py \
  --root /root/ping_gu \
  --pred_dir U2Net \
  --gt_mat_dir GroundTruths_mat \
  --gt_png_dir GroundTruths \
  --out_dir U2Net_eval_run \
  --model_name U2Net \
  --pred_mode auto \
  --workers -1 \
  --thrs 99 \
  --clean
cat U2Net_eval_run/summary.txt
```

The evaluated scope is determined by that server directory's actual `.mat` files. It need not equal the three-sample GitHub subset.

## 4. Actual Metric and Post-Processing Rules

These details are read from the supplied implementation; packaging does not change them.

| Stage | Supplied implementation |
| --- | --- |
| Prediction loading | Convert grayscale PNG to float32 by dividing by 255; write `.mat` with key `result`. |
| Polarity | `edge_white`: unchanged; `edge_black`: invert; `auto`: invert each image when its mean exceeds 0.5. Record the inversion count and use explicit polarity when known. |
| NMS | Always applied by this entry point; triangle smoothing radii 1 and 4, native NMS radius 1, border parameter 5, multiplier 1.01; output quantized to uint8 PNG. |
| Thresholds | With `--thrs 99`, use 0.01, 0.02, ..., 0.99 and the `>=` comparison. |
| Prediction thinning | Apply the modified Guo-Hall thinning routine at each threshold, except that maps with edge density greater than 0.30 bypass thinning. |
| Correspondence | Greedy KD-tree matching, at most 80 GT candidates per prediction, one-to-one matches, tolerance `0.0075 * sqrt(H*H + W*W)` pixels. This is not the original global CSA assignment. |
| Multiple annotations | Union matched predictions across annotations for precision; sum matched GT and GT counts across annotations for recall. |
| F-measure | `2*P*R/max(2e-6, P+R)`, with the implementation's epsilon guards for count ratios. |
| ODS | Aggregate threshold-level counts across images; select the best F after 100-point linear interpolation between each pair of adjacent PR operating points. |
| OIS | For the aggregate OIS, select each image's discrete best-F threshold and sum its counts, then compute aggregate R/P/F. Per-image output also contains separately interpolated optimum values. |
| AP | Deduplicate recall using first-occurrence indices, linearly interpolate P at 101 recall values from 0 to 1, fill outside the observed range with zero, then sum and divide by 100; return zero if there is only one unique recall value. |

The greedy matcher and the density-based thinning shortcut can affect results relative to other evaluators. Report this protocol with the manuscript scores. NMS is mandatory in this entry point, so its use for PiDiNet + MatchED must agree with the actual experiment protocol rather than being inferred from this example.

## 5. Outputs

```text
U2Net_eval_run/
|-- summary.txt
|-- gt_mat_samples/
|-- pred_mat/
`-- nms/
    |-- U2Net/
    `-- U2Net-eval/
        |-- eval_bdry.txt
        |-- eval_bdry_img.txt
        |-- eval_bdry_thr.txt
        `-- <sample>_ev1.txt
```

`summary.txt` contains ODS, OIS, AP, ODS_T, ODS_R, ODS_P, OIS_R, and OIS_P. No metric values are bundled or invented.

## 6. Additional Helpers and Provenance

- `convert_gt_to_mat.py`: grayscale PNG `>128`, followed by the supplied thinning routine, to `groundTruth/Boundaries`. Included `.mat` files do not need reconversion.
- `png_to_mat.py`: prediction conversion with optional inversion.
- `rescale_edmb.py`: optional in-place rescaling helper, not called by the main entry point.
- `edge_eval_python/fix_shapes.py`: historical helper with fixed relative paths and in-place writes; it is not automatically executed or imported.

See [../THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) for upstream provenance and retained licences. The original upstream README's BSDS scores are reference results, not PWED scores.
