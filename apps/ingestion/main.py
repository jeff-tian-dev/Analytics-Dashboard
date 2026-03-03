import logging
import sys

from .ingest import run_once


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger("ingestion")

    try:
        run_once()
    except Exception:
        logger.exception("Fatal error during ingestion")
        sys.exit(1)


if __name__ == "__main__":
    main()
