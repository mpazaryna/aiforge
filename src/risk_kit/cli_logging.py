import logging
from pathlib import Path

from risk_kit.logging_config import setup_logging


def main():
    # Define the log directory and file
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_file = log_dir / "risk_kit.log"

    # Ensure the logs directory exists
    log_dir.mkdir(exist_ok=True)

    # Setup logging
    setup_logging(log_file=str(log_file))

    # Get a logger
    logger = logging.getLogger(__name__)

    # Log some test messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    print(f"Log messages have been written to {log_file}")
    print("You can now examine the log file manually.")


if __name__ == "__main__":
    main()
