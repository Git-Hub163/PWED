# PWED Evaluation: ODS, OIS and AP

This directory contains the evaluation implementation used to compute ODS, OIS and AP, together with conversion helpers and a small set of pre-thinned ground-truth `.mat` files. The repository's three `.mat` labels are demonstration samples only; the reported benchmark evaluates the combined validation and test splits of PWED, containing 242 images.

All six methods use the same evaluation implementation and protocol. This standardises the comparison within the study. The implementation is based on a BSDS-style evaluation framework but uses the study-specific matching implementation documented below.

## Server Environment

Run the evaluation on the Linux cloud server. The local Windows checkout is for code and documentation preparation; it is not used for GPU inference or metric generation.

```text
Operating system: Ubuntu 20.04
GPU: 1 × NVIDIA GeForce RTX 4090, 24 GB
CPU: 16 cores
Memory: 32 GB RAM
System disk: 200 GB
Framework: PyTorch
```

## Inputs

- Prediction maps: grayscale PNG confidence maps with stems matching the ground-truth `.mat` files.
- `GroundTruths/*.png`: original PNG labels for the demonstration samples.
- `GroundTruths_mat/*.mat`: BSDS-format labels containing `groundTruth` and `Boundaries`.
- Complete evaluation: the full 242-image validation-plus-test set and predictions generated with the corresponding model configurations.

The current repository includes 3 demonstration test samples and their 3 `.mat` labels. It does not include the complete PWED dataset or prediction outputs.

## Build and Run

Install dependencies and build the native NMS library in the server environment:

```bash
cd /root/ping_gu
python -m pip install -r /path/to/PWED/evaluation/requirements.txt
mkdir -p edge_eval_python/cxx/lib
(cd edge_eval_python/cxx/src && bash build.sh)
```

Place prediction PNGs in the selected prediction directory, then run:

```bash
cd /root/ping_gu
rm -rf -- edge_eval_python/impl/__pycache__ U2Net_eval_run
python /path/to/PWED/evaluation/run_edter_eval.py \
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

`U2Net` is the name used in the supplied example command; it is not an additional baseline in the six-method comparison. For the benchmark methods, replace the prediction directory and model name while preserving the same evaluation code and protocol.

## Evaluation Protocol

### Prediction conversion

Grayscale PNG predictions are converted to float32 values in `[0, 1]` and written to MATLAB files with the key `result`. `--pred_mode edge_white` keeps the polarity; `--pred_mode edge_black` inverts it; `--pred_mode auto` inverts an image when its mean intensity exceeds 0.5. Use an explicit polarity when it is known from the model output.

### NMS and thinning

The entry point applies NMS before metric evaluation. NMS uses the supplied native implementation with triangle smoothing radii 1 and 4, NMS radius 1, border parameter 5 and multiplier 1.01, then writes an 8-bit PNG map.

At each threshold, the NMS map is binarised and processed with the supplied Guo-Hall thinning implementation. The current implementation skips thinning when foreground pixels occupy more than 30% of the binary map. Ground-truth annotations are converted with the same thinning routine before being stored as `.mat` labels; the evaluator then reads those pre-thinned boundaries.

### Matching

The evaluator uses greedy one-to-one matching based on KD-tree nearest-neighbour search. The matching tolerance is `0.0075 × sqrt(H² + W²)` pixels, where `H` and `W` are the image dimensions. For each predicted edge point, up to 80 candidate ground-truth points are queried. Predicted points are processed in ascending nearest-candidate distance, and each ground-truth point can be assigned at most once.

This is the common matching procedure for all six methods in this study. It is a study-specific implementation based on the BSDS evaluation framework and should not be interpreted as numerically identical to the original global assignment implementation.

### Thresholds and metrics

With `--thrs 99`, thresholds are `1/100, 2/100, ..., 99/100`, using `>=` for binarisation. For multiple ground-truth annotations, matched predictions are unioned for precision, while matched and total ground-truth counts are accumulated for recall. PWED supplies one reviewed annotation per image.

- **ODS:** aggregate counts across images at each threshold. Interpolate precision and recall at 100 positions between adjacent threshold points, then select the maximum dataset-level F-measure.
- **OIS:** select each image's F-measure-maximising discrete threshold, sum the corresponding match counts across images, then calculate aggregate precision, recall and F-measure. Per-image records also store an interpolated optimum; aggregate OIS uses the discrete-threshold counts.
- **AP:** deduplicate recall values, interpolate precision at 101 recall positions from 0 to 1, use zero outside the observed recall range, and sum the interpolated values divided by 100. If only one unique recall value remains, AP is zero.

The exact implementation is in `edge_eval_python/impl/edges_eval_dir.py` and `edge_eval_python/impl/correspond_pixels.py`. Clear stale evaluation outputs after changing matching, image stems, shapes or label files.

## Outputs

The evaluation writes converted predictions, NMS maps, per-image threshold records, the aggregate evaluation file and `summary.txt`. The summary reports ODS, OIS, AP and their associated precision/recall values.

## Reproducibility Record

The public release will record the repository commit used for the paper, complete PWED data version, model checkpoints, prediction-generation commands, matching tolerance, candidate limit, NMS and thinning settings, threshold grid, and metric aggregation rules. The current display subset is intended for repository and workflow inspection; it is not a replacement for the complete 242-image evaluation set.
