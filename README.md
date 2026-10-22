# PWED: Polychrome Wood-carving Edge Dataset

PWED (Polychrome Wood-carving Edge Dataset) is a pixel-level edge detection dataset for polychrome wood-carving images. The complete dataset contains **1,208 image-annotation pairs**: 351 photographs of real wood-carving artworks and 857 high-fidelity synthetic images generated with AI models.

The complete dataset is split into **966 training images, 121 validation images, and 121 test images**. Each RGB JPG image has one same-resolution, single-channel PNG edge annotation. Pixel value 255 denotes an edge and 0 denotes background. Released annotations preserve the original line width and are not thinned before release.

This repository is currently a **private pre-publication preparation repository**. Its small display subset is provided to inspect the directory structure, file pairing and evaluation workflow; it is not the complete PWED dataset. Following paper acceptance, the complete dataset will be released through this repository.

## Repository Contents

- `data/`: the current display subset, file manifest and split pair lists.
- `evaluation/`: ODS/OIS/AP evaluation code, the supplied evaluation labels and server-side run instructions.
- `THIRD_PARTY_NOTICES.md`: provenance and licence notices for reused evaluation components.
- `CHECKSUMS.sha256`: checksums for the currently included image and annotation files.

The current display subset contains 9 image-annotation pairs: 3 training, 3 validation and 3 test pairs. It also contains 3 corresponding pre-thinned MATLAB ground-truth files for the included test samples. These files are provided for demonstration and code review only.

## Experimental Setup

The six benchmark experiments were conducted on a Linux cloud deep-learning server using PyTorch.

| Component | Configuration |
| --- | --- |
| Operating system | Ubuntu 20.04 |
| GPU | 1 × NVIDIA GeForce RTX 4090, 24 GB |
| CPU | 16 cores |
| Memory | 32 GB RAM |
| System disk | 200 GB |

All six methods were trained or fine-tuned on the PWED training set. Optimizer and learning-rate settings followed the public configurations of the corresponding implementations. Training used the PWED training split; evaluation used single-scale inference on the combined validation and test splits, giving 242 evaluation images.

High-resolution inputs were preserved through model-specific cropping or sliding-window inference rather than being uniformly downsampled to one fixed small resolution.

## Baseline Methods

| Method | Paper | Venue | Code |
| --- | --- | --- | --- |
| RCF | Richer Convolutional Features for Edge Detection | CVPR 2017 | [RCF-PyTorch](https://github.com/yun-liu/RCF-PyTorch) |
| PiDiNet | Pixel Difference Networks for Efficient Edge Detection | ICCV 2021 | [PiDiNet](https://github.com/hellozhuo/pidinet) |
| EDTER | EDTER: Edge Detection with Transformer | CVPR 2022 | [EDTER](https://github.com/MengyangPu/EDTER) |
| SAUGE | SAUGE: Taming SAM for Uncertainty-Aligned Multi-Granularity Edge Detection | AAAI 2025 | [SAUGE](https://github.com/Star-xing1/SAUGE) |
| EDMB | EDMB: Edge Detector with Mamba | WACV 2025 | [EDMB](https://github.com/Li-yachuan/EDMB) |
| PiDiNet + MatchED | MatchED: Crisp Edge Detection Using End-to-End, Matching-based Supervision | CVPR 2026 | [MatchED](https://github.com/Bedrettin-Cetinkaya/MatchED) |

`PiDiNet + MatchED` denotes a PiDiNet model trained with MatchED supervision. RCF* and PiDiNet + MatchED* in the benchmark table indicate the fine-tuned configurations reported in the paper.

## Evaluation

All six methods use the same evaluation implementation. The protocol applies NMS to prediction maps, thresholds and thins predictions using the Guo-Hall routine, thins the ground-truth annotations, and computes ODS, OIS and AP. The current implementation uses greedy one-to-one KD-tree matching with a tolerance of `0.0075 × image diagonal` and up to 80 candidate ground-truth points per predicted edge point.

The repository code is a study-specific implementation based on the BSDS-style evaluation framework. It should not be interpreted as numerically identical to the original global assignment implementation. The exact matching, NMS, thinning, threshold and aggregation rules are documented in [evaluation/README.md](evaluation/README.md).

The current display subset does not contain predictions or the complete 242-image evaluation set, so it is not intended to reproduce the paper's full benchmark table. Full evaluation should be run on the server with the complete data and matching predictions.

## Data and Code Availability

The PWED dataset, evaluation code and run instructions will be made publicly available at [https://github.com/Git-Hub163/PWED](https://github.com/Git-Hub163/PWED) after the paper is accepted and the release information is finalised. A DOI is not available yet because the paper has not been accepted. The repository will record the code version corresponding to the reported results, matching tolerance, candidate-point limit, NMS and thinning settings, evaluation thresholds and metric aggregation procedure.

## Acknowledgements

We thank the authors of [RCF](https://github.com/yun-liu/RCF-PyTorch), [PiDiNet](https://github.com/hellozhuo/pidinet), [EDTER](https://github.com/MengyangPu/EDTER), [SAUGE](https://github.com/Star-xing1/SAUGE), [EDMB](https://github.com/Li-yachuan/EDMB) and [MatchED](https://github.com/Bedrettin-Cetinkaya/MatchED) for making their implementations available. The evaluation implementation also builds on [edge_eval_python](https://github.com/Walstruzz/edge_eval_python); reused components and notices are listed in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Citation

The dataset citation, paper DOI and final release version will be added after publication. The current repository is a private pre-publication preparation release.
