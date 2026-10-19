# PWED: Dataset Samples and Edge Detection Evaluation

The six baseline experiments (RCF, PiDiNet, EDTER, SAUGE, EDMB, and PiDiNet + MatchED) were carried out on a Linux-based cloud deep learning server equipped with an NVIDIA GeForce RTX 4090 GPU, using PyTorch.

This repository accompanies the preparation of a *Scientific Data* submission for **PWED**. It contains a selected dataset subset, links to six baseline methods, and the supplied ODS/OIS/AP evaluation implementation.

**Review status:** This repository is intended to remain private until the authors approve public release. The current subset contains **9 image/annotation pairs** (3 training, 3 validation, and 3 test pairs), plus **3 pre-thinned MATLAB ground-truth files** for the included test images. This is a partial release, not the complete PWED dataset. Predictions and benchmark scores are not included.

## Download

Repository: [Git-Hub163/PWED](https://github.com/Git-Hub163/PWED). While private, access is restricted to the owner and authorised collaborators.

```bash
git clone https://github.com/Git-Hub163/PWED.git
cd PWED
```

The GitHub **Code > Download ZIP** menu also downloads the included subset for users who have access. See [data/README.md](data/README.md) and [data/manifest.csv](data/manifest.csv) for the files and split membership.

## 1. Experimental Environment

| Item | Study setting |
| --- | --- |
| Execution platform | Linux-based cloud deep learning server |
| GPU | NVIDIA GeForce RTX 4090 |
| Deep learning framework | PyTorch |
| Linux distribution and version | TODO: record the actual version |
| Python / PyTorch / CUDA / cuDNN | TODO: record versions separately for each method if needed |
| Evaluation dependencies | TODO: export from the environment that produced the reported metrics |

The environment description above is supplied by the study authors. Upstream repository requirements do not establish which environment was used in this study.

## 2. Dataset and Data Access

- Dataset name: **PWED**; this snapshot is a selected subset.
- Original images: `data/Images/{train,val,test}/*.jpg`.
- Paired annotations: `data/GroundTruths/{train,val,test}/*.png`, matched by filename stem within each split.
- Included split sizes: **train 3 / val 3 / test 3** image/annotation pairs.
- Evaluation annotations: `evaluation/GroundTruths/*.png` and `evaluation/GroundTruths_mat/*.mat` for the **3 included test samples**. The `.mat` boundaries have already been thinned, as supplied by the authors.
- [Manifest](data/manifest.csv), [subset pair lists](data/splits/), and [SHA-256 checksums](CHECKSUMS.sha256) describe the included files. No image rescaling or label regeneration was performed during repository preparation.
- `data/train_pair_aug.txt` is an inherited 30,912-line augmented-training list. Its referenced `aug/` files are not included; use `data/splits/` to enumerate the actual subset.
- Dataset acquisition details, formal version/DOI, citation, and data licence remain to be supplied before public release.

For *Scientific Data*, ensure the data described by the manuscript are available for editorial and peer review. For non-sensitive data, first-round access must support seamless, anonymous download; from the second round onward, the journal requires public availability in a formal repository that meets its policy. A small demonstration subset should be labelled as such and should not be described as the complete data resource evaluated in the paper.

Use an appropriate data repository for the archival data release, and use this GitHub repository as the entry point for documentation and code. Zenodo and figshare are examples to assess against the journal's repository criteria and the dataset's requirements.

Policy sources, checked on 2026-10-19:

- [Scientific Data: Data Policies](https://www.nature.com/sdata/policies/data-policies)
- [Scientific Data: Data Repository Guidance](https://www.nature.com/sdata/policies/repositories)
- [Scientific Data: Editorial and Publishing Policies](https://www.nature.com/sdata/policies/editorial-and-publishing-policies)

See [dataset documentation](data/README.md) for the release checklist.

## 3. Reproduced Baselines

The following links identify the upstream publications and implementations. The exact implementation and commit used for each experiment in this study still need to be recorded.

| Baseline | Paper title | Conference | Upstream code | Publication |
| --- | --- | --- | --- | --- |
| RCF | Richer Convolutional Features for Edge Detection | CVPR 2017 | [Author-provided PyTorch implementation](https://github.com/yun-liu/RCF-PyTorch); [original repository](https://github.com/yun-liu/rcf) | [CVF](https://openaccess.thecvf.com/content_cvpr_2017/html/Liu_Richer_Convolutional_Features_CVPR_2017_paper.html) |
| PiDiNet | Pixel Difference Networks for Efficient Edge Detection | ICCV 2021 | [Code](https://github.com/hellozhuo/pidinet) | [CVF](https://openaccess.thecvf.com/content/ICCV2021/html/Su_Pixel_Difference_Networks_for_Efficient_Edge_Detection_ICCV_2021_paper.html) |
| EDTER | EDTER: Edge Detection with Transformer | CVPR 2022 | [Code](https://github.com/MengyangPu/EDTER) | [CVF](https://openaccess.thecvf.com/content/CVPR2022/html/Pu_EDTER_Edge_Detection_With_Transformer_CVPR_2022_paper.html) |
| SAUGE | SAUGE: Taming SAM for Uncertainty-Aligned Multi-Granularity Edge Detection | AAAI 2025 | [Code](https://github.com/Star-xing1/SAUGE) | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/32615) |
| EDMB | EDMB: Edge Detector with Mamba | WACV 2025 | [Code](https://github.com/Li-yachuan/EDMB) | [CVF](https://openaccess.thecvf.com/content/WACV2025/html/Li_EDMB_Edge_Detector_with_Mamba_WACV_2025_paper.html) |
| PiDiNet + MatchED | MatchED: Crisp Edge Detection Using End-to-End, Matching-based Supervision | CVPR 2026 | [MatchED code](https://github.com/Bedrettin-Cetinkaya/MatchED) | [CVF](https://openaccess.thecvf.com/content/CVPR2026/html/Cetinkaya_MatchED_Crisp_Edge_Detection_Using_End-to-End_Matching-based_Supervision_CVPR_2026_paper.html) |

All six publication entries above are conference publications. RCF and PiDiNet also have later journal-related work; cite the versions that correspond to this study.

Here, **PiDiNet + MatchED** denotes the PiDiNet detector with MatchED matching-based supervision. The sixth paper title is the title of the MatchED publication.

For each method, provide the exact source URL and commit, local modifications, model configuration, checkpoint source or training record, inference settings, and corresponding evaluation command. RCF's original repository uses Caffe, so identify the actual PyTorch implementation used in this study. Do not substitute a reference implementation for the implementation actually evaluated.

## 4. Evaluation Code and Protocol

The supplied evaluation code computes:

- **ODS (Optimal Dataset Scale):** the best dataset-level boundary F-measure obtained using a single threshold across the evaluated images.
- **OIS (Optimal Image Scale):** choose each image's discrete best-F threshold, aggregate the corresponding matching counts, and compute F from the aggregated precision and recall.
- **AP (Average Precision):** the implementation's interpolated precision values at 101 recall locations from 0 to 1, summed and divided by 100. This exact convention is documented rather than silently replaced with another AP function.

The protocol must state the test split, prediction and ground-truth formats, filename matching, dimensions, edge polarity, confidence scale, NMS/thinning policy, threshold sweep, spatial matching tolerance and its units, correspondence algorithm, multiple-annotation handling, and AP integration convention. These settings must be consistent with the reported results.

NMS and thinning must be declared per method. In particular, do not silently apply the same post-processing to PiDiNet + MatchED without documenting how it relates to the reported evaluation protocol.

See [evaluation/README.md](evaluation/README.md) for the Linux build instructions, input format, exact command, and outputs. The active matcher is a **greedy KD-tree one-to-one matcher with up to 80 candidates**, with a tolerance of **0.0075 times the image diagonal**. It is a local modification of the upstream evaluator and must not be described as identical to its original CSA matching algorithm.

The provided `run_edter_eval.py` entry point supports the author's U2Net command as an evaluation example. **U2Net is not a seventh baseline** in the six-method comparison. No U2Net prediction files were supplied, so this snapshot cannot produce scores until matching predictions are added on the server. Local preparation involved file/text checks only; the evaluator has not been rerun here.

## 5. Reproducibility and Benchmark Results

TODO: add the six methods' ODS, OIS, AP, evaluated sample count, dataset version, split identifier, checkpoint identifier, and evaluation settings. Distinguish results on a released subset from results on the full test set. Do not use upstream BSDS/NYUD numbers as results on this dataset.

Before reporting reproducibility of the full benchmark, add the configuration files, inference/evaluation commands, dependency records, precision-recall data, and metric summary files corresponding to the published table. The current subset supports inspection and an evaluation run with supplied predictions, but cannot reproduce full-test-set scores.

## 6. Citation, Licences, and Contact

- Dataset name: PWED; formal citation / version-specific DOI: TODO.
- Manuscript citation / DOI: TODO when available.
- Code release tag, commit, and archival DOI: TODO.
- Code licence: TODO, after checking ownership and dependencies.
- Data licence: TODO; document separately from the code licence.
- Third-party notices: see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md); original source notices and the C++ component's licence text are retained.
- Contact: TODO.

The upstream method links above provide attribution. Add verified bibliographic records for the dataset, manuscript, and reused evaluation tools when the release is prepared.
