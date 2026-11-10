# Contributing

Welcome! This is an academic research prototype. Open an issue before major changes.

1. Create a new feature branch; do not push to the author's previous repositories.
2. Install: `python -m pip install -e '.[dev]'`.
3. Run `pytest -q` and the example pipeline.
4. Distinguish **measured**, **Geant4-generated**, **historically reported**, and **toy-demo** results in every PR.
5. Provide full geometry, Geant4 version, physics list, RNG seeds, event counts, threshold assumptions and raw evidence for new quantitative claims.
6. Do not commit vendor SPICE models or detector datasheets without permission to redistribute them.
