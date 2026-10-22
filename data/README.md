# PWED Data

## Complete Dataset

PWED contains **1,208 RGB image-annotation pairs** for pixel-level edge detection in polychrome wood-carving imagery:

- 351 photographs of real wood-carving artworks.
- 857 high-fidelity synthetic images generated with AI models.
- 966 training images, 121 validation images and 121 test images.
- 281 real and 685 synthetic images in the training split.
- 35 real and 86 synthetic images in each of the validation and test splits.

Each image is stored as a JPG file and has one same-resolution, single-channel PNG annotation. Pixel value 255 denotes an edge and 0 denotes background. The released annotations preserve the original line width and are not skeletonised or morphologically thinned before release.

The complete dataset will be released after paper acceptance. The repository URL is [https://github.com/Git-Hub163/PWED](https://github.com/Git-Hub163/PWED). A DOI is not available yet because the paper has not been accepted.

## Current Display Subset

The files currently stored in this repository are a small display subset for checking file organisation and pairing:

| Split | Image files | PNG annotations |
| --- | ---: | ---: |
| train | 3 | 3 |
| val | 3 | 3 |
| test | 3 | 3 |
| Total | 9 | 9 |

The subset is not the complete PWED dataset and cannot reproduce the paper's full evaluation results. The evaluation directory contains 3 matching pre-thinned `.mat` labels for the included test samples only.

## Directory Structure

```text
data/
|-- Images/{train,val,test}/*.jpg
|-- GroundTruths/{train,val,test}/*.png
|-- manifest.csv
|-- splits/{train,val,test}_pairs.txt
`-- train_pair_aug.txt
```

Images and annotations are paired by identical filename stem within each split. The complete release will also provide fixed `ImageSets` lists for the 966/121/121 split.

The training protocol supports 32-fold geometric augmentation from two random-flip states and 16 rotation angles. Any training report should state the crop, padding, augmentation and inference settings used by the model implementation.

## Annotation Procedure

Three polychrome wood-carving experts and four annotators produced the annotations. The team trial-annotated 50 images to establish consistent line widths, boundary assignment and texture criteria. Completed annotations underwent two rounds of blind review; approximately 15% required redrawing. Annotation and review took seven months.

## Integrity

`manifest.csv` records the current subset. `splits/` contains relative image-annotation pairs. `CHECKSUMS.sha256` at the repository root covers the currently included JPG, PNG and `.mat` files.

```bash
sha256sum --check CHECKSUMS.sha256
```

The full dataset release will add the final archive or data record, version identifier, licence, citation information and complete checksums.
