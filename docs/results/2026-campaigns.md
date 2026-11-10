# Historical simulations — 2026 run ledger

> **Evidence provenance**: The statistics below were reported in prior project discussions and report summaries dated **28 October–3 November 2026**. The original large Geant4 result directories / full per-event data / production source are **not part of the files provided for this repository build**. Therefore these are **reported historical results, not independently reprocessed or reproduced here**. No new numerical values have been fabricated to fill missing cells.

## Campaign A — geometry, readout and gap sweeps (28 October 2026)

| Metric | Historical value |
|---|---:|
| Completed runs | 444 |
| Primary muons | 24,800,040 |
| Configurations | 100 reported upper/lower gap combinations |
| Distinct comparisons | 222 reported paired comparisons |
| Stages | A–F: 20, 54, 200, 38, 72, 58 + 2 controls = 444 |

### Selected geometric-acceptance observations

A historical study used a 5 cm Pb target and varied top/bottom distances. Exact event definitions and config files must be restored before presenting these as independently verified results.

| Top gap / bottom gap | Crossings / scintillator interaction / electronics coincidences | Coincidence fraction of crossings |
|---|---|---|
| 1 cm / 1 cm | 126 / 40 / 24 | 19.0% |
| 3 cm / 1 cm | 115 / 32 / 13 | 11.3% |
| 5 cm / 5 cm | 117 / 23 / 12 | 10.3% |
| 1 cm / 10 cm | 127 / 17 / 7 | 5.5% |

For a reported high-statistics sample: 3,000,000 injected muons; 13,679 entered the cube, 13,679 were recorded leaving it, 1,754 left energy in both scintillators and 825 satisfied electronic coincidence (825/13,679 = 6.03%). **None of these values by itself establishes a stopped-muon count**. Do not reinterpret a geometrically rejected or undetected event as absorption.

## Campaign B — focus and spatial validation (3 November 2026)

| Metric | Historical reported result |
|---|---:|
| Validation / run status | 550/550 PASS |
| Primary muons | 1,251,006,000 |
| Cube/no-cube pairs | 275 |
| Stage counts | 4 + 56 + 32 + 150 + 200 + 48 + 30 + 30 = 550 |
| Discovery scan | 150 runs / 75 pairs |
| Holdout scan | 200 runs |
| 2D contrast correlation: discovery vs holdout | r = 0.941 |
| Same contrast sign | 24 of 25 positions |
| Predefined central 3×3 vs outer 16 holdout comparison | reported Z = −5.08 |

**Interpretation:** consistent spatial modulation under repeated mechanically controlled scans. This is not proof of event-by-event tracking, 3D tomography, or unique material identification.

### Material-screen observations (historical reports)

| Material | Reported relative coincidence change | Reported test statistic |
|---|---:|---:|
| Lead (Pb) | −1.27% | −2.73 Z |
| Aluminium (Al) | −1.22% | −2.63 Z |
| Concrete | −1.20% | −2.57 Z |
| Iron (Fe) | −1.13% | −2.44 Z |
| Copper (Cu) | −1.10% | −2.37 Z |
| Water | −1.05% | −2.25 Z |

The differences **between materials** were not resolved reliably. The per-material deficits versus a no-sample reference are not a substitute for tested pairwise separability. Similarly, earlier Pb fill/void/inclusion cases were not reliably distinguishable.

### What passed and what did not

- `PASS` indicates completed simulation workflow/QA conditions as reported, **not** detector calibration or physical performance verification.
- Stronger evidence exists for **geometry-dependent coincidence acceptance** and **repeatable coarse spatial contrast** than for **element identification**, **void detection** or **material-specific tomography**.
- The absolute count rates and input energy/angle spectra are model-dependent; a coincidence cut may introduce additional biases.
- Original source, raw CSVs, configuration hashes, Geant4 build logs and systematic sensitivity tables are required for independent publication-grade reproducibility.

## Archived electronics simulations

Earlier LTspice revisions examined 1–15 ns PMT pulses, nominal 8 ns / 200 mV stress cases, a weak PMT2, comparator output voltage and stretched coincidence pulses. Some initial revision logs had **zero `COINC_FAST` / `MONO_1US` outputs** and failed measurements. A later test series reportedly achieved 5 coincidence output pulses from 5 synthetic correlated inputs, but the original executable simulation/measurement logs are not fully present in this repository and cannot be independently certified. Avoid presenting one revision's result as universal performance.

## Missing archive / how to restore it

The historical production directory had a structure resembling `MUON_TAM_SIMULASYON_2026`, `results_focus_2026/geant4/.../reports`, `results_full/...`, and compressed stage archives. These datasets are large and absent from the currently provided uploads. Preserve their **original hashes**, add a public-safe `data_manifest.csv` (run ID, geometry, physics list, seed, generated/event counts, SHA256), and release data separately (e.g., a DOI-backed archive) rather than adding multi-GB raw files to Git history.

## Machine-readable historical summaries

[Selected gap observations](historical-gap-examples.csv) and [reported material-screen values](historical-materials.csv) are supplied as **transcriptions of prior historical summaries**, not raw output from newly executed Geant4 code. [`scripts/plot_historical_reports.py`](../../scripts/plot_historical_reports.py) redraws the associated disclaimer-labeled figures.
