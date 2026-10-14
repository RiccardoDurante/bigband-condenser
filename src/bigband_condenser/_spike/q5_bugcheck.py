"""Q5 - Transpose tag preservation in output.

Check if music21 writer omits <transpose> for parts sharing same instrument class (R24).

Status: STUB. See docs/pmi/SPIKE_M2_PLAN.md and KRONOS_KAI_KAIROS_FINDINGS.md.
"""
from bigband_condenser._spike.common import setup_logging, KRONOS_EXTRACT

logger = setup_logging()


def main() -> None:
    logger.info("Q5_BUGCHECK: not implemented yet")
    logger.info(f"Target sample: {KRONOS_EXTRACT}")
    raise NotImplementedError("Q5 stub - implement in M2 timebox")


if __name__ == "__main__":
    main()
