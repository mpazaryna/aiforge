import os
from pathlib import Path

# Determine the project root directory
PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent.parent
)  # Adjust to point to the project root

# Configuration settings
DATA_DIRECTORY = PROJECT_ROOT / "data"  # Set to the root data directory
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
LOGGING_FILENAME = os.getenv("LOGGING_FILENAME", "model_evaluation.log")
OUTPUT_JSON_FILENAME = (
    DATA_DIRECTORY / "model_evaluation_output.json"
)  # Use the root data directory
