# PWED Evaluation: ODS, OIS and AP

This guide describes the evaluation code used to compute ODS, OIS and AP. Predictions and ground-truth files are supplied separately on the Linux server; neither dataset samples nor prediction outputs are distributed in this repository.

The evaluator is applied consistently to all six methods. The public release will identify the code version used for the reported results and document the matching tolerance, candidate-point limit, NMS and thinning settings, threshold grid, and metric aggregation procedures.

## Server Setup

Run evaluation on the Linux cloud server. Metric computation consumes saved prediction maps and does not require rerunning model inference.

Clone this repository on the server. The prediction and ground-truth directories remain under `/root/ping_gu`:

```bash
git clone https://github.com/Git-Hub163/PWED.git /root/PWED
cd /root/ping_gu
cp -a /root/PWED/evaluation/edge_eval_python/. edge_eval_python/
python -m pip install -r /root/PWED/evaluation/requirements.txt
mkdir -p edge_eval_python/cxx/lib
(cd edge_eval_python/cxx/src && bash build.sh)
```

The build requires `g++` and creates `edge_eval_python/cxx/lib/solve_csa.so`, used by the native NMS routine. Build and run this code in the Linux server environment.

## Inputs

- Prediction maps: grayscale PNG confidence maps in a method-specific directory such as `/root/ping_gu/RCF/`.
- Ground-truth labels: matching BSDS-format `.mat` files in `/root/ping_gu/GroundTruths_mat/`, containing `groundTruth` and `Boundaries`.
- Original ground-truth PNGs: `/root/ping_gu/GroundTruths/`, used by the entry point for label inspection.
- Filenames: prediction stems must match the corresponding `.mat` stems; prediction and label dimensions must agree.
- Dataset split: PWED uses training and test sets. Evaluation is performed on the test set.

The evaluator does not automatically rename `_thin` suffixes, transpose predictions or resize mismatched maps. Resolve any method-specific stem or dimension conversion before running evaluation and record it with the experiment settings.

## Run

Set `PRED_DIR` and `MODEL_NAME` to the prediction folder and method label for each run. The same evaluator and settings are used for all six methods.

```bash
cd /root/ping_gu
PRED_DIR=RCF
MODEL_NAME=RCF
OUT_DIR=${MODEL_NAME}_eval_run
rm -rf -- edge_eval_python/impl/__pycache__ "$OUT_DIR"
python /root/PWED/evaluation/run_edter_eval.py \
  --root /root/ping_gu \
  --pred_dir "$PRED_DIR" \
  --gt_mat_dir GroundTruths_mat \
  --gt_png_dir GroundTruths \
  --out_dir "$OUT_DIR" \
  --model_name "$MODEL_NAME" \
  --pred_mode edge_white \
  --workers -1 \
  --thrs 99 \
  --clean
cat "$OUT_DIR/summary.txt"
```

Choose `--pred_mode edge_white` when high values represent edges and `edge_black` when low values represent edges. `auto` inverts a map when its mean intensity exceeds 0.5; use an explicit mode when the output polarity is known. Repeat the command with each method's prediction directory and model name.

`--clean` recreates the specified output directory. Use a dedicated output path for each method. `--workers -1` uses all available CPU cores, and `--thrs 99` evaluates thresholds from 0.01 through 0.99 in increments of 0.01.

## Evaluation Protocol

### Prediction conversion and NMS

Grayscale PNG predictions are normalised to float32 `[0, 1]` and saved as MATLAB files using the key `result`. NMS is applied before metric calculation. It uses triangle smoothing radii 1 and 4, NMS radius 1, border parameter 5 and multiplier 1.01; the resulting map is quantised to 8-bit PNG.

### Ground-truth and prediction thinning

Ground-truth PNGs are binarised using `pixel value > 128` and thinned with the supplied Guo-Hall routine before conversion to BSDS-format `.mat` files. During evaluation, predictions are thresholded and thinned with the same routine. The current implementation skips thinning when foreground pixels exceed 30% of a binary prediction map.

### Matching

The evaluator uses greedy one-to-one matching based on KD-tree nearest-neighbour search. The tolerance is `0.0075 × sqrt(H² + W²)` pixels. For each predicted edge point, up to 80 ground-truth candidates are queried; predicted points are processed in ascending nearest-candidate distance, and a ground-truth point can be assigned at most once. 

### Thresholds and metrics

With `--thrs 99`, the threshold grid is 0.01, 0.02, ..., 0.99, using `>=` to binarise maps.

- **ODS:** aggregate matching counts across images at each threshold, interpolate precision and recall at 100 positions between adjacent threshold points, and report the maximum dataset-level F-measure.
- **OIS:** select the F-measure-maximising discrete threshold for each image, aggregate the corresponding match counts, and calculate overall precision, recall and F-measure.
- **AP:** deduplicate recall values, interpolate precision at 101 recall positions from 0 to 1, use zero outside the observed recall range, and sum the interpolated values divided by 100. AP is zero if only one unique recall value remains.

PWED provides one reviewed ground-truth annotation per image. The evaluator can read multiple annotations: matched predictions are unioned for precision, while matched and total ground-truth counts are accumulated for recall.

## Outputs

The output directory contains converted predictions, NMS maps, per-image threshold records, aggregate evaluation files and `summary.txt`. The summary reports ODS, OIS, AP and associated precision/recall values. Exact implementation details are in `run_edter_eval.py`, `edge_eval_python/impl/edges_eval_dir.py`, `edge_eval_python/impl/correspond_pixels.py` and `edge_eval_python/nms_process.py`.

## Release Record

The public repository will identify the commit corresponding to the reported results. It will include the evaluator and instructions above; dataset files and predictions are distributed separately. Third-party provenance and applicable notices are listed in [`../THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).
