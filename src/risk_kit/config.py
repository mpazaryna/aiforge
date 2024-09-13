import os
from functools import cached_property
from pathlib import Path


class RiskKitConfig:
    """
    A configuration class for managing directories in the RiskKit module.
    """

    @cached_property
    def project_root(self):
        """Lazy-loaded project root directory."""
        env_root = os.environ.get("RISKKIT_PROJECT_ROOT")
        return Path(env_root) if env_root else Path(__file__).parent.parent.parent

    @cached_property
    def logs_dir(self):
        """Lazy-loaded logs directory."""
        return self._get_directory("RISKKIT_LOGS_DIR", "logs")

    def _get_directory(self, env_var, default_name):
        """
        Sets up a directory based on environment variables or defaults.
        """
        env_dir = os.environ.get(env_var)
        if env_dir:
            dir_path = Path(env_dir)
        else:
            dir_path = self.project_root / default_name

        return dir_path

    def ensure_directories_exist(self):
        """
        Ensures all directories exist. Call this method explicitly when you want to create the directories.
        """
        self.logs_dir.mkdir(parents=True, exist_ok=True)


# Create a global instance of the configuration
config = RiskKitConfig()
