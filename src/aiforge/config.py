from pathlib import Path

# Project root directory
# PROJECT_ROOT = Path(__file__).resolve().parent

# Project root directory (assuming config.py is in src/paz)
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


# Data directory
DATA_DIR = PROJECT_ROOT / "data"

# Temporary directory
TMP_DIR = PROJECT_ROOT / "tmp"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
TMP_DIR.mkdir(exist_ok=True)
