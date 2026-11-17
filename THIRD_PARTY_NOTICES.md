# Third-Party Sources and Notices

The PWED repository includes a locally modified copy of [Walstruzz/edge_eval_python](https://github.com/Walstruzz/edge_eval_python), whose nested checkout records upstream commit `add539b95e9222ba9426924decee1c61ebcefb83`. The bundled files contain local modifications and must not be represented as an unmodified upstream checkout.

Observed modified components include `impl/bwmorph_thin.py`, `impl/correspond_pixels.py`, `impl/edges_eval_dir.py`, and `nms_process.py`. In particular, the active matching function uses greedy KD-tree correspondence with up to 80 candidates, and the thinning routine includes a density-based bypass. The original algorithm's guarantees and benchmark figures are not claimed for those modifications.

The upstream README credits:

- [HED edge evaluation](https://github.com/s9xie/hed_release-deprecated/tree/master/examples/eval).
- [Extended Berkeley segmentation benchmark](https://github.com/davidstutz/extended-berkeley-segmentation-benchmark).
- [Guo-Hall thinning implementation](https://gist.github.com/joefutrelle/562f25bbcf20691217b8).
- [Piotr Dollar's MATLAB toolbox](https://github.com/pdollar/toolbox) and [edge toolbox](https://github.com/pdollar/edges).
- [PyTorch HED implementation](https://github.com/xwjabc/hed).

Original source headers and `evaluation/edge_eval_python/cxx/README.md` are retained. The latter contains a non-commercial scientific/educational/artistic-use notice from the extended Berkeley benchmark; some C++ source headers additionally identify GPL version 2 or later. Preserve and assess the component-specific terms rather than assigning one blanket permissive licence to the mixed-source evaluation code.

Compiled libraries, Python bytecode, accidental zero-byte option-name files, model checkpoints and dataset files are excluded from this repository. Linux users rebuild the native library from the bundled source.
