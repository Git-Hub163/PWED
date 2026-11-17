# PWED Evaluation Code

This repository provides the code and server-side instructions for computing ODS, OIS and AP on PWED predictions. Dataset images, ground-truth labels, model implementations and model predictions are maintained separately and are not included here.

The evaluation guide documents the matching tolerance, candidate-point limit, NMS and thinning settings, threshold grid, metric definitions and aggregation procedures. The public release will identify the code version corresponding to the reported results.

## Contents

- [`evaluation/README.md`](evaluation/README.md): server setup, input requirements and run command.
- [`evaluation/`](evaluation/): metric evaluator, prediction conversion utilities and matching/NMS implementation.
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md): provenance and licence notices for reused evaluation components.

## Baseline Implementations

- [RCF: Richer Convolutional Features for Edge Detection](https://github.com/yun-liu/RCF-PyTorch)
- [PiDiNet: Pixel Difference Networks for Efficient Edge Detection](https://github.com/hellozhuo/pidinet)
- [EDTER: Edge Detection with Transformer](https://github.com/MengyangPu/EDTER)
- [SAUGE: Taming SAM for Uncertainty-Aligned Multi-Granularity Edge Detection](https://github.com/Star-xing1/SAUGE)
- [EDMB: Edge Detector with Mamba](https://github.com/Li-yachuan/EDMB)
- [PiDiNet + MatchED: Crisp Edge Detection Using End-to-End, Matching-based Supervision](https://github.com/Bedrettin-Cetinkaya/MatchED)
