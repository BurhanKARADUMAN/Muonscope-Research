# Scientific boundaries and open issues

## What is tested

- `pytest` checks deterministic paired toy counting, geometry ray/cube intersection, Wilson confidence bounds, pulse generation, threshold crossings, one-to-one coincidence logic and dead time.
- Python `muonscope demo` outputs figures/CSV/JSON with declared assumptions, seeds and event counts.
- Historical .asc/.asy input files were extracted from supplied ZIPs, retaining filenames and case distinctions.

## What is not tested here

- The new C++ Geant4 example was **not compiled or executed against the user's Windows Geant4 11.3 installation**.
- Historical 444-/550-run Geant4 source/data were **not mounted/uploaded to the current build**; the summary table is not an independent reanalysis.
- Archived LTspice circuits were **not simulated on LTspice Windows** during this repository build; models are not bundled.
- No PMT module output was measured/calibrated, no complete optical transport or photodetector gain model was validated.
- No actual board was fabricated or characterised; no STM32 firmware or physical DAQ evidence is included.
- The toy model's `effective_loss_per_cm` is not a cross section, material attenuation coefficient or measured detector efficiency.
- This is **two-plane radiographic counting**, not full 3D PoCA scattering tomography.

## Specific improvement priorities

1. Restore original simulation/configuration hashes and direct raw readout efficiency vs cube gap.
2. Check manufacturer PMT load/signal ratings and design a calibrated nanosecond-capable transimpedance/voltage gain stage if needed.
3. Re-run an end-to-end Geant4 optical/photodetector digitizer with uncertainty propagation.
4. Add tests for accidental coincidences, cable delays, threshold dispersion, pile-up, reflections and discriminator time walk.
5. Verify repeatability on blinded targets and holdout geometries, and calibrate material separation using sufficiently distinct known objects.
6. Build tracking readout with at least four position planes for event-wise scattering tomography if that is the research objective.
