# aiforge/config.py

import os
from pathlib import Path


class AiForgeConfig:
    def __init__(self):
        self.project_root = self._get_project_root()
        self.data_dir = self._get_directory("AIFORGE_DATA_DIR", "data")
        self.tmp_dir = self._get_directory("AIFORGE_TMP_DIR", "tmp")

    def _get_project_root(self):
        # Try to get the project root from an environment variable
        env_root = os.environ.get("AIFORGE_PROJECT_ROOT")
        if env_root:
            return Path(env_root)

        # If not set, use the current working directory
        return Path.cwd()

    def _get_directory(self, env_var, default_name):
        # Try to get the directory from an environment variable
        env_dir = os.environ.get(env_var)
        if env_dir:
            dir_path = Path(env_dir)
        else:
            # If not set, use a subdirectory of the project root
            dir_path = self.project_root / default_name

        # Ensure the directory exists
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path


# Create a global instance of the configuration
config = AiForgeConfig()

# Usage in other modules:
# from aiforge.config import config
# ... config.data_dir, config.tmp_dir ...
