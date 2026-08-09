# CGM Clinical Safety Reanalysis

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21859990.svg)](https://doi.org/10.5281/zenodo.21859990)

This audit-focused repository accompanies “Lower Point Error Does Not Imply Clinical Safety: Re-evaluating CGM Forecasting through Event Prediction and Cross-Population Generalization” (manuscript V5.5).

It openly provides:

- an independent DTS point-accuracy Error Grid implementation with boundary tests;
- clinical-safety metrics for binary events, discrimination, false-alarm episodes, and lead time;
- trajectory-derived risk scoring, matched-specificity operating-point selection, and fixed-threshold external evaluation;
- privacy-preserving aggregate results corresponding to manuscript Tables 2–6;
- automated consistency tests and a script that rebuilds the principal Markdown tables and aggregate-data figures.

## Install and verify

```bash
conda env create -f environment.yml
conda activate cgm-safety-audit
python -m pip install -e .
pytest
python scripts/build_paper_outputs.py
```

Generated tables and figures are written to `output/`.

## Repository map

- `src/cgm_safety/`: auditable metric implementations.
- `derived/`: structured aggregate values used in the manuscript.
- `scripts/`: deterministic table and figure reconstruction.
- `tests/`: DTS boundaries, metric behavior, and manuscript-number checks.
- `docs/`: data provenance, privacy/licensing, and manuscript-output mapping.

## Data Availability

The clinical-safety evaluation code, DTS Error Grid implementation, aggregate result tables, tests, and scripts for rebuilding principal result tables and data figures are available in this repository and archived at [https://doi.org/10.5281/zenodo.21859990](https://doi.org/10.5281/zenodo.21859990). The public CGM datasets analyzed in the study are available from their original sources cited in the manuscript. Data provenance and licensing details are documented in `docs/PRIVACY_AND_LICENSE.md`.

## License and citation

Repository code is available under the MIT License. Dataset rights remain with their original providers. Citation metadata are provided in `CITATION.cff` and `.zenodo.json`.

Please cite the Zenodo archive for the software version used:

> Liu Q, Yang M, Wang Z, Wang S, Liu W, An X, Lu S, Liu M, Yang Q. CGM Clinical Safety Reanalysis. Zenodo. https://doi.org/10.5281/zenodo.21859990
