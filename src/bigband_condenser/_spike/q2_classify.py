"""Q2 - Instrument classifier via partName string matching.

Expected: 19/19 correct on Kronos extract (per cloud FINDINGS v0.2).

Status: STUB. See docs/pmi/SPIKE_M2_PLAN.md and KRONOS_KAI_KAIROS_FINDINGS.md.
"""
from bigband_condenser._spike.common import setup_logging, KRONOS_EXTRACT

logger = setup_logging()


def main() -> None:
    logger.info("Q2_CLASSIFY: not implemented yet")
    logger.info(f"Target sample: {KRONOS_EXTRACT}")
    raise NotImplementedError("Q2 stub - implement in M2 timebox")


if __name__ == "__main__":
    main()
