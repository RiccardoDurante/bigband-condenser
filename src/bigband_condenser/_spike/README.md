# _spike/ - Big Band Condenser M2 Feasibility Spike

**Status**: experimental, NOT production code.

This folder contains throwaway scripts used during the Milestone 2 feasibility spike. These files answer the 6 spike questions defined in `docs/pmi/SPIKE_M2_PLAN.md`:

- `q1_parse.py` - Parse integrity on Kronos extract
- `q2_classify.py` - Instrument classification via partName
- `q3_transpose.py` - Concert pitch transposition verification
- `q4_write.py` - Round-trip (music21.write) + XML pass-through strategy for drums
- `q5_bugcheck.py` - Transpose tag preservation in output
- `q6_structure.py` - 4-staff condensed structure skeleton

Shared helpers in `common.py` (sample paths, logging, constants).

## Policy

- Code here will be rewritten in `src/bigband_condenser/` top-level during M3-M8 as production code.
- Not imported by any production module.
- No test coverage required at spike stage.
- When spike closes (M2 complete), snapshot in `docs/pmi/releases/<date>_M2/spike_code/` and either keep as archived reference or remove.

See `docs/pmi/KRONOS_KAI_KAIROS_FINDINGS.md` for preliminary cloud findings that pre-dated the local spike execution.
