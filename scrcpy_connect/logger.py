import logging


def setup_logging(log_level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, log_level), 
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
