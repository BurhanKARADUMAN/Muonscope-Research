# LTspice design archives

Folders contain the **original schematics and custom symbols** obtained from the user-supplied source ZIPs. To honor manufacturer model licensing, vendor SPICE `.lib` and `.cir` files are not included. Copy legitimately obtained models beside each schematic before opening/running it in LTspice.

| Folder | Contents | Readout |
|---|---|---|
| `tlv3601/` | Intended original dual-TLV3601 schematic + schematic figures | `MUON_SUNUM.asc`; **presentation schematic, missing transient stimulus** |
| `lm358/` | Two LM358 amplifier sections in the previous presentation topology | `MUON_LM358.asc`; **not a valid ns-pulse front end** |
| `realistic-pmt/` | Three LM358 scenarios, PWL stimuli, generator/config and figures | **uncalibrated stress stimuli**, high peaks exceed a simple 50-ohm PMT rating check |

The `.inc` files reference the names `tlv3601.lib`, `LM358.lib`, `SN74LVC2G17.cir`, `SN74LVC1G08.cir`; manufacturers' libraries must be downloaded separately. Source symbols are included in each respective folder for easy opening. Model incompatibilities and simulation errors are possible; **LTspice transient runs were not revalidated**.

In the user-provided project, the TLV3601 schematic's PMT input ports do not include time-domain sources and the file has no transient test command. In contrast, the LM358 PWL scenario sheets do provide synthetic current-source stimuli. Read the [signal-integrity audit](../../docs/pmt-and-signal-integrity.md) before making any hardware claims from those plots.
