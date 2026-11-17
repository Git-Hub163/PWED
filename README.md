# PWED Evaluation Code

This repository provides the code and server-side instructions for computing ODS, OIS and AP on PWED predictions. Dataset images, ground-truth labels, model implementations and model predictions are maintained separately and are not included here.

The evaluation guide documents the matching tolerance, candidate-point limit, NMS and thinning settings, threshold grid, metric definitions and aggregation procedures. The public release will identify the code version corresponding to the reported results.

## Contents

- [`evaluation/README.md`](evaluation/README.md): server setup, input requirements and run command.
- [`evaluation/`](evaluation/): metric evaluator, prediction conversion utilities and matching/NMS implementation.
- [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md): provenance and licence notices for reused evaluation components.

The current repository is private during pre-publication preparation. The evaluation code and instructions will be made public after the paper is accepted.
