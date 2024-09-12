import logging


def setup_logging(log_file="risk_kit_run.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,  # Set to INFO or lower
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
