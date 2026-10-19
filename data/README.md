# PWED Dataset Subset

This repository contains only the subset selected by the authors for the current review snapshot. It does not contain the full PWED dataset.

| Split | Images | PNG annotations |
| --- | ---: | ---: |
| train | 3 | 3 |
| val | 3 | 3 |
| test | 3 | 3 |
| Total | 9 | 9 |

## Layout and Pairing

```text
data/
|-- Images/{train,val,test}/*.jpg
|-- GroundTruths/{train,val,test}/*.png
|-- manifest.csv
|-- splits/{train,val,test}_pairs.txt
`-- train_pair_aug.txt
```

Pair each image and annotation by split and identical filename stem. `manifest.csv` records the image path, annotation path, and, for the three included test samples, the corresponding evaluation PNG and `.mat` paths. Manifest paths are relative to the repository root. Paths in `splits/*_pairs.txt` are relative to `data/`. Each pair-list line contains `image_path annotation_path`.

The three test samples are `A_2007_0`, `A_2007_0-1`, and `A_2007_0-2`. The corresponding `evaluation/GroundTruths/` PNGs are paired with `evaluation/GroundTruths_mat/` MATLAB annotations. The authors supplied the `.mat` files with already-thinned boundaries; they were not regenerated during packaging.

`train_pair_aug.txt` is the inherited **30,912-line** full augmentation list. The `aug/` files named there are outside this subset. It is retained as a study record, not a runnable file list for the nine included samples.

## Download and Integrity

Clone [Git-Hub163/PWED](https://github.com/Git-Hub163/PWED), or use **Code > Download ZIP**. Private access requires authorisation. The repository-root `CHECKSUMS.sha256` covers the included JPG, PNG, and `.mat` files. On Linux, run from the repository root:

```bash
sha256sum --check CHECKSUMS.sha256
```

Only filename pairing and byte-level integrity are checked during local packaging. Image dimensions, annotation polarity, and internal `.mat` contents must be validated in the intended server environment. The supplied conversion script treats PNG values greater than 128 as boundary pixels; preserve the actual annotation convention when converting further labels.

## Release Scope

The current snapshot supports inspection of PWED's file layout and a small evaluation once predictions are supplied. It cannot reproduce results obtained on the full test set. Acquisition and annotation details, a formal dataset version/DOI, citation, and data licence should be completed before public release. Private repository access is for author review; it does not establish anonymous reviewer access or fulfil the formal data deposit by itself.
