# Geant4 standalone example

This is a **new, minimal Geant4 demonstration**, not a copy of the 2026 550-run production engine (which was not part of the current uploaded files). It provides real Geant4 energy-deposition transport with FTFP_BERT; it does **not** model scintillation optics, PMT electrons, timing thresholds, amplification, or STM32 readout.

## Requirements
- Geant4 (target: 11.3.x; **not compiled or runtime-tested** in the creation environment)
- CMake >=3.16 and C++17
- `Geant4_DIR` configured if CMake cannot discover it

```bash
cmake -S simulation/geant4 -B simulation/geant4/build -DGeant4_DIR=/path/to/geant4/lib/Geant4-11.3.2
cmake --build simulation/geant4/build --config Release
./simulation/geant4/build/muonscope_g4 --events 100000 --seed 22 --upper-gap-mm 50 --lower-gap-mm 100 --target lead --output lead.csv
./simulation/geant4/build/muonscope_g4 --events 100000 --seed 22 --upper-gap-mm 50 --lower-gap-mm 100 --target none --output empty.csv
```

On Windows, run `muonscope_g4.exe` from your selected build configuration. `--target lead` enables a Pb cube, any other target value currently disables it; only `lead` and `none` are documented.

## The model
- Plastic-like medium: NIST `G4_POLYSTYRENE`, two 100×100×10 mm panels by default
- 50 mm lead cube centered between detectors
- Plane clearances separately adjustable in mm
- Muons: mu-minus, fixed 3 GeV, downward cosine-squared zenith intensity with projected-area weighting
- CSV: per-event energy deposits, approximate first-hit position and both-plane energy-deposit indicator

**Important:** A positive energy deposit in a scintillator is not a calibrated PMT signal or trigger. A complete model needs light yield, optical collection, photoelectron statistics, PMT response, noise and analog/electronic threshold conversion. This Geant4 demo **cannot reproduce** the historical 550-run results without the original engine, exact geometry/configuration, random seeds and readout model.

**No validated results are claimed for this Geant4 source until compiled/run in a Geant4 environment.**
