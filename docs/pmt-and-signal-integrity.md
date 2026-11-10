# PMT realism and signal-integrity audit

## Module identification

The detector concept references **Hamamatsu H10721-110**, a current-output PMT module. Manufacturer references (see [references](references.md)) list approximately 0.57 ns typical rise time and up to 100 µA maximum output signal current. Exact conditions and absolute maximum ratings are specified by the manufacturer; read the datasheet before designing external terminations, power supply or protection.

## Why the historical input waveform needs a disclaimer

A simple passive 49.9-ohm termination obeys Ohm's law:

| Current into 49.9 Ω | Implied voltage |
|---:|---:|
| 1 µA | 0.0499 mV |
| 10 µA | 0.499 mV |
| 50 µA | 2.495 mV |
| 100 µA | 4.99 mV |

The previous PWL test used a representative `−220 mV` PMT1 pulse and `−145 mV` PMT2 pulse at 49.9 Ω. Those would require approximately **4.41 mA** and **2.91 mA**, respectively, if modeled as unamplified resistive output. This is far beyond the listed 100 µA maximum output. The stimulus is therefore preserved solely as a **legacy high-amplitude analog stress case**: it is not a prediction of typical muon-induced H10721-110 pulses.

**Important nuance:** a current-output PMT signal depends on pulse charge/time, impedance, bandwidth, input capacitance, coupling and actual instrumentation. The upper bound above is a simple resistive sanity check, not a calibrated transient transfer function. The output specification may itself depend on timing and definitions; use measured current and voltage traces and the manufacturer's recommended operating circuit.

## Comparator-overdrive challenge

TLV3601's quoted maximum input offset is ±5 mV in its product overview, comparable to the *simple* 49.9 Ω/100 µA maximum voltage estimate. The analog chain may therefore need carefully designed wideband gain, offset removal, hysteresis, noise shaping and a realistic threshold budget. A Geant4 photoelectron count is not directly a voltage threshold.

## Suggested measurement sequence

1. Identify exact scintillator material/dimensions/optical coupling and PMT operating control voltage.
2. Check module safe output/current and specified load conditions.
3. Acquire baseline noise, single-detector dark events and real muon candidate traces using an appropriately bandwidth-rated and calibrated front end.
4. Measure terminated waveform area (charge), amplitude distribution, rise/fall characteristics and event coincidence timing.
5. Fit signal-vs-photoelectron transfer (with uncertainties), then implement an LTspice source or amplifier model constrained to observed waveforms.
6. Sweep comparator threshold/temperature/voltage, verify false coincidence rate and dead time on a hardware prototype.
7. Update the Geant4 digitizer using measured conversion/photoelectron-statistics parameters.

The repository's new Python pulse plot deliberately uses **1–3.2 mV** illustrative pulses across a nominal 50-ohm-class load. Those are *still not measured waveforms*.
