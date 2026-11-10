# Detector system architecture

## Proposed experimental topology

Two plastic scintillator panels surround a target. A photosensor (original hardware design: **two Hamamatsu H10721-110 current-output PMT modules**) senses each panel's light. Negative PMT pulses pass through 50-ohm-class terminations, bias/AC-coupling and a fast comparator discriminator. A Schmitt stage shapes logic, an AND gate forms a coincidence decision, an extension stage produces an MCU-safe logic pulse, and an STM32 counter records events.

```text
cosmic muon ---> TOP scintillator --------> H10721-110 PMT ---> 50 Ω input --┐
                 target: optional Pb cube                                      ├-> TLV3601 -> Schmitt ->-┐
            ---> BOTTOM scintillator -----> H10721-110 PMT ---> 50 Ω input --┘                        |
                                   [separate identical discriminator channel]                     AND
                                                                                                -> pulse shaping
                                                                                                -> STM32 counter
```

Actual schematics use labels: `PMT1_SMA`, `PMT2_SMA`, `INM1`, `INM2`, `U3A_OUT`, `U3B_OUT`, `CH1_PS`, `CH2_PS`, `COINC_FAST`, `STM_SING1`, `STM_SING2`, `STM_COINC`.

## Physical vs computational modules

1. **Particle transport**: Geant4 follows muons and secondaries through geometry and materials.
2. **Scintillation**: energy loss → light yield + photon statistics; depends on material, wrapping, geometry, light transport.
3. **PMT response**: photons → photoelectrons → gain/current, with pulse dispersion, dark/background counts, voltage-control settings.
4. **Analog conditioning**: current-to-voltage conversion/termination, bias, protection, gain and comparator thresholds.
5. **Digital logic**: Schmitt edge cleaning, pulse width, coincidence gate/time window and recovery.
6. **DAQ**: microcontroller/FPGA counter readout, clock, dead time, logging.
7. **Statistical analysis**: paired sample/reference rates, efficiency, uncertainties, spatial scan and holdout validation.

**Only portions of this stack are currently implemented in each tool.** The Python illustration models geometry and a parametric effective loss; the C++ Geant4 demo models energy deposition; the LTspice archive contains original circuit schematics and synthetic PMT PWL inputs. No single validated end-to-end hardware calibration currently bridges all stages.

## Geometry parameters

The current runnable *illustration* chooses 100×100×10 mm scintillator panels, a 50 mm Pb cube and separate 50 mm top/bottom clearances. These dimensions are defaults for the new demo and should not be mistaken for the fully validated dimensions of the historical Geant4 campaign.

## Signals to probe

| Node | Measurement |
|---|---|
| `PMT1_SMA`, `PMT2_SMA` | Real terminated pulse amplitude/rise/charge and ringing |
| `INM1`, `INM2` | Comparator input bias and AC-coupled waveform |
| `U3A_OUT`, `U3B_OUT` | Comparator propagation, output level and dead-time/recovery |
| `CH1_PS`, `CH2_PS` | Width of conditioned discriminator pulses |
| `COINC_FAST` | Fast coincidence logic output |
| `STM_COINC` | Final MCU-safe pulse width and voltage |

Measure all channels using a bandwidth-aware 50-ohm oscilloscope input/probe without adding unaccounted probe capacitance.
