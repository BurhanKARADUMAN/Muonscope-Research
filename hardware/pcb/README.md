# PCB design status

The research group previously developed a multi-revision PMT coincidence front end, including KiCad/LTspice engineering discussions. **A historical Rev AB KiCad `.kicad_sch` engineering schematic was recovered from the project file archive** and is included as `MUON_RevAB_TAM_CIZILMIS_PROTOTIP.kicad_sch` (title block: 17 Oct 2026). It is a **schematic candidate requiring ERC, not fabrication approval**. No completed production `.kicad_pcb` or verified Gerber set is available.

Before a Gerber release: freeze schematic netlist and references, replace placeholder regulators, validate protection and supply decoupling, check vendor footprint pin mapping, derive signal-integrity constraints, run ERC/DRC and document bench validation. The first board should have test points for input, comparator and coincidence outputs.
