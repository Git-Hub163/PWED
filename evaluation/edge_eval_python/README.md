# PWED Evaluation Components

This directory contains a locally modified copy of [`edge_eval_python`](https://github.com/Walstruzz/edge_eval_python), used by the PWED evaluation entry point. It is not an unmodified upstream release. The local matching and thinning behavior is described in [the PWED evaluation guide](../README.md).

To build and run the PWED evaluation, follow [the server instructions](../README.md). The native library is built from the included C++ sources; compiled binaries and upstream example datasets are not included.

Upstream BSDS500 example scores and figures are intentionally not reproduced here. They are not PWED results. See [third-party provenance and licence notices](../../THIRD_PARTY_NOTICES.md) for source attribution and applicable terms.
