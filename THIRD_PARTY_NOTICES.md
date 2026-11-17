# Third-Party Sources and Notices

Observed modified components include `impl/bwmorph_thin.py`, `impl/correspond_pixels.py`, `impl/edges_eval_dir.py`, and `nms_process.py`. In particular, the active matching function uses greedy KD-tree correspondence with up to 80 candidates, and the thinning routine includes a density-based bypass. 

The upstream README credits:

- [HED edge evaluation](https://github.com/s9xie/hed_release-deprecated/tree/master/examples/eval).
- [Extended Berkeley segmentation benchmark](https://github.com/davidstutz/extended-berkeley-segmentation-benchmark).
- [Guo-Hall thinning implementation](https://gist.github.com/joefutrelle/562f25bbcf20691217b8).
- [Piotr Dollar's MATLAB toolbox](https://github.com/pdollar/toolbox) and [edge toolbox](https://github.com/pdollar/edges).
- [PyTorch HED implementation](https://github.com/xwjabc/hed).

Original source headers and `evaluation/edge_eval_python/cxx/README.md` are retained. The latter contains a non-commercial scientific/educational/artistic-use notice from the extended Berkeley benchmark; some C++ source headers additionally identify GPL version 2 or later.
