import logging
from pathlib import Path

from risk_kit.logging_config import setup_logging


def test_logging_writes_to_logs_directory():
    log_dir = Path(__file__).parent.parent.parent.parent / "logs"
    log_file = log_dir / "test_risk_kit.log"

    log_dir.mkdir(exist_ok=True)
    setup_logging(log_file=str(log_file))

    logger = logging.getLogger(__name__)

    logger.debug("This is a debug message from pytest")
    logger.info("This is an info message from pytest")
    logger.warning("This is a warning message from pytest")
    logger.error("This is an error message from pytest")

    assert log_file.exists(), f"Log file does not exist at {log_file}"

    log_content = log_file.read_text()
    print(f"Log file content:\n{log_content}")

    assert "debug message from pytest" in log_content
    assert "info message from pytest" in log_content
    assert "warning message from pytest" in log_content
    assert "error message from pytest" in log_content

    print(f"Test passed. Log messages have been written to {log_file}")
