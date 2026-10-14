"""Q4 - Round-trip and XML pass-through strategy.

music21.write() fails on Finale drum parts (sub-32th durations, see R27 critical).
Explore XML pass-through strategy for drums as mitigation.

Status: STUB. See docs/pmi/SPIKE_M2_PLAN.md and KRONOS_KAI_KAIROS_FINDINGS.md section 5.
"""
from bigband_condenser._spike.common import setup_logging, KRONOS_EXTRACT

logger = setup_logging()


def main() -> None:
    logger.info("Q4_WRITE: not implemented yet")
    logger.info(f"Target sample: {KRONOS_EXTRACT}")
    raise NotImplementedError("Q4 stub - implement in M2 timebox (CRITICAL - see R27)")


if __name__ == "__main__":
    main()
