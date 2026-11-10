# Reproducibility, dataset policy, asset provenance

## Quick reproducibility command

```bash
python -m pip install -e '.[dev]'
pytest -q
python -m muonscope demo --output-dir outputs/reproduction --seed 2026 --primaries-per-point 15000 --grid-size 11
```

The Python demo's seed, model label and number of injected primaries are written to `summary.json` along with derived counts. Data-dependent stats are **not** universal: change the random seed / geometry / threshold and they will change.

## Provenance classes

| Tag | Meaning | Example |
|---|---|---|
| `TOY_SURROGATE_NOT_GEANT4` | Reproducible illustrative Python simulation | `examples/demo/scan_counts.csv` |
| `ARCHIVED_LTSPICE_STIMULUS` | Archived uncalibrated LTspice PWL stress waveform | `hardware/ltspice/realistic-pmt/*` |
| `HISTORICALLY_REPORTED` | Prior conversation/report numbers not reprocessed in this ZIP | `docs/results/2026-campaigns.md` |
| `NEW_GEANT4_EXAMPLE_UNVALIDATED` | Source provided, no local Geant4 build/runtime | `simulation/geant4/main.cc` |
| `MEASURED` | Experimental evidence from a laboratory setup | **None included** |

## Third-party material

The uploaded original user-owned `.asc` schematics, custom `.asy` symbol files and accompanying demonstration images were preserved as supplied. A separate historical KiCad Rev AB `.kicad_sch` engineering schematic was recovered from available project-file storage; it is not a validated PCB. SPICE vendor models (`tlv3601.lib`, `LM358.lib`, `SN74LVC2G17.cir`, `SN74LVC1G08.cir`) and external manufacturer PDFs were intentionally **excluded** pending review of redistribution permissions. The source `.inc` files may reference these model files by name. The MIT license applies to newly authored project code/docs, not automatically to external manufacturer models, product names or datasheets.

## Large data management

Raw production runs may exceed GitHub practical repository sizes. Keep original output trees offline; create a checksummed manifest with a stable storage link, dataset version and DOI for release. Do not repackage the historical results as if recreated by the new toy demonstration.
