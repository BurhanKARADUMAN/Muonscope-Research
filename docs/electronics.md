# Coincidence front-end engineering notes

## Original comparator-based signal chain

`PMT -> 49.9 Ω input -> AC-coupling/bias -> TLV3601 threshold discriminator -> Schmitt SN74LVC2G17 -> SN74LVC1G08 AND -> pulse stretch -> 3.3 V MCU output`

Signals: `PMT1_SMA`, `PMT2_SMA`, `INM1`, `INM2`, `U3A_OUT`, `U3B_OUT`, `CH1_PS`, `CH2_PS`, `COINC_FAST`, `STM_COINC`, `STM_SING1`, `STM_SING2`. There are two input channels and a common coincidence path. Circuit sheets are **presentation/prototype schematics**, not released PCB fabrication data.

### Comparison

| Parameter | TLV3601 | LM358 |
|---|---|---|
| Intended type | Fast rail-to-rail comparator | General-purpose dual operational amplifier |
| Speed class | ~2.5 ns propagation (specified conditions) | ~0.3 V/µs typical slew rate; not a ns discriminator |
| Two channels | Two single-channel ICs | One dual-op-amp IC |
| Role in this project | Intended high-speed discriminator | Control/educational comparison **only** |
| Status | External vendor model required, transient unverified here | External model required, transient unverified here |

**LM358 is NOT pin-compatible** with TLV3601: changing a symbol means re-mapping pin assignments and supplies; it cannot be a real board drop-in. Slower pulse response does not validate comparator threshold claims.

## PCB and signal integrity

- Use a continuous low-inductance ground reference and short controlled-impedance SMA-to-front-end routing.
- Place proper power decoupling at IC supply pins; choose supply rails from guaranteed absolute maximum and logic-level specs.
- Check comparator input common-mode swing, propagation delay vs overdrive and hysteresis.
- Avoid excessive input capacitance and ring-prone cables; verify 50-ohm termination and PMT output loading.
- Measure comparator timing, Schmitt output, AND output and stretched STM input with appropriate probes.
- A `CABLE`, `CIN`, `PAR` or MCU load capacitor in the schematic may represent a **parasitic model**, not a component that should be purchased.
- Check STM32 logic voltage requirements and max pulse count frequency; configure timer/capture rather than relying on slow polling.

## Known development history

Early LTspice runs exhibited failed `COINC_FAST` and `MONO_1US` measurements despite visible comparator nodes. Other simulated versions passed simple synthetic coincidence tests, but **successful simulation of one test vector does not show a physical PMT signal can cross the threshold**. An operational prototype must be calibrated with an appropriate signal generator and observed real PMT output.

## Modeling and ownership

Custom `.asc` and `.asy` files are preserved; the device vendor's SPICE macro-models were not redistributed with this public-ready repository because their license/redistribution status has not been established. Get authentic source models from the device manufacturers and keep them alongside each `.asc` file locally.
