import logging
import os


def setup_logging(log_file="risk_kit_run.log"):
    # Use an absolute path for the log file
    log_file_path = os.path.join(os.path.dirname(__file__), log_file)

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the logging level

    # Create file handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)  # Set level for file handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Set level for console
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
