# Calibration and experimental validation protocol

| Stage | Controlled test | Evidence to save | Acceptance criterion (to be set, not asserted) |
|---|---|---|---|
| 1. PMT module | Confirm model and safe voltage/control | Photos, supply/current settings, datasheet revision | Safe operation at manufacturer-specified settings |
| 2. Oscilloscope | Dark/noise and representative candidate waveforms | CSV traces incl. timebase/termination | Repeatable baseline, bandwidth known |
| 3. Signal transfer | Calibrated current/charge injection through 50 Ω frontend | Pulse shape and amplitude-vs-injected-charge curve | Measured transfer, uncertainty quantified |
| 4. Comparator | Threshold and overdrive sweep | `PMT_SMA`, `INM`, comparator waveforms | Width/delay/false-positive budget measured |
| 5. Coincidence | Dual pulser with variable time delay | Efficiency curve vs `Δt`, accidental rates | Fitted coincidence width and dead time |
| 6. STM32 | Count known pulse train using hardware timer | input vs recorded counts, rollover logs | Quantified count losses, timestamp resolution |
| 7. Geometry | Move a known reference target/stage grid | Stage positions, live time, empty/sample counts | Repeatable spatial registration |
| 8. Physics | Compare Geant4 & real coincidence data | geometry hashes, configs and raw runs | Meaningful discrepancy/systematics report |

## Data schema suggestion

One row per scan position / acquisition: `run_id`, `timestamp_utc`, `scan_x_mm`, `scan_y_mm`, `top_gap_mm`, `bottom_gap_mm`, `target`, `live_time_s`, `raw_single_1`, `raw_single_2`, `coincidences`, `noise_rms_mv`, `threshold_ch1_mv`, `threshold_ch2_mv`, `coincidence_window_ns`, `temperature_C`, `config_sha256`.

Separate `blank`, `background` and `target` runs; treat a raw event count without effective exposure as insufficient for a quantitative material claim. Add thresholds, optical settings and geometric tolerances to the systematics budget.
