# Measurement model and statistical methodology

## Cosmic-muon incidence

MuonScope's rapid Python demonstration samples a *simplified* sea-level intensity proportional to `cos²(theta)` and includes the horizontal detector's projected-area factor. Hence the sampled distribution in `c = cos(theta)` is `p(c) = 4c³`, `c = U^(1/4)` on `[0, 1]`. Azimuth is uniform. This ignores energy dependence, altitude, building overburden, geomagnetic effects and charge sign. **It is not a validated absolute muon flux generator.**

## Two-panel geometry

Tracks are launched across the top plane and intersect the bottom plane if the projected position lies within its active area. A segment/AABB intersection computes the distance inside a central cube. The Python **toy** case assigns an effective survival probability:

`P_survive = exp[-k_eff (L_cube / 10 mm)]`

Here `k_eff` is specified in `1/cm` and is deliberately a user-tunable **surrogate parameter**, not lead's physical stopping coefficient. The toy model does not predict multiple Coulomb scattering, energy-loss straggling, secondaries, photoelectrons or detector thresholds. For those questions, use Geant4 with a documented physics configuration and experimentally calibrated digitization.

## Paired tests and uncertainty

The toy baseline/sample experiment shares incoming tracks and pre-sample detector acceptance. For `n = reference coincidence count` and `k = survived sample coincidences`, `T = k/n`. Conditional on the simplified random-loss model, the sampling error is binomial. This repository reports the two-sided 95% **Wilson score interval** for `T`. This is *not* the same as treating two independent count rates with Poisson errors. When modeling two separately acquired exposures, include exposure/live-time normalization, dark background, systematic uncertainties and use an appropriate independent-count likelihood.

## Raster scanning

`muonscope demo` shifts the phantom laterally relative to a pair of simulated detector panels and repeats trials over a grid. Each pixel is a **separate mechanically scanned acquisition**, with a true (simulator-internal) spatial coordinate. A pair of unsegmented PMTs cannot give x/y hit position for every individual muon. Spatial information arises from **controlled stage coordinates** in this measurement mode.

## Why this is not PoCA tomography

Scattering tomography reconstructs deflection using incoming and outgoing trajectories; a single upper hit and single lower hit do not measure two independent directions. At least two position measurements before and after the target (typically **four or more tracking layers**) are needed, plus alignment, resolution models and a reconstruction algorithm. The provided project focuses on **radiographic transmission / coincidence scans**, with scattering tomography as a future extension.

## Definitions and traps

- **Primary:** one generated particle in the transport simulation.
- **Crossed target:** geometrical path intersected object volume; does not imply absorption.
- **Deposited energy:** energy deposited in a sensitive volume, not a PMT voltage waveform.
- **Detected:** requires thresholds, live time and digitization; never equate directly to a Geant4 step.
- **Stopped muon:** requires a proper transport/status criterion; “not coincident” does **not** imply stopped inside the cube.
- **Transmission:** always specify reference definition and whether exposures are paired or independent.
