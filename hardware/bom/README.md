# Preliminary hardware bill of materials

The [CSV](hardware_bom.csv) is an **early procurement planning list** for **one two-channel prototype**, with extra backup quantities. It is **not** a PCB manufacturing BOM, approved schematic, footprint list, or a claim of vendor stock.

Critical ICs: `TLV3601 ×2`, `SN74LVC2G17 ×3`, `SN74LVC1G08 ×1`. Auxiliary diode choices include `BAT54` and `BAS70`, plus SMA, passive input termination and decoupling. Some schematic capacitors represent cable/loading parasitics, not actual purchased parts. STM32 target board previously discussed: `NUCLEO-F746ZG`; verify specific MCU GPIO/timer and voltage interface before wiring.

Order priority: fast comparator/Schmitt/AND devices, validated SMA connectors and 49.9 Ω terminations, signal/power integrity components, then measured-value passives after analog rework. The PMT front end may need a **new broadband amplifier**; do not assume the first-draft parts list builds a working nanosecond muon detector.

Manufacturer links and datasheets are in [references](../../docs/references.md). Availability at Renko/Rentech or other vendors is not asserted here.
