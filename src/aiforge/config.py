"""
AiForge Configuration Module

This module provides a centralized configuration management system for the AiForge project.
It handles the setup of essential directories and allows for flexible configuration through
environment variables.

The main class, AiForgeConfig, manages the following directories:
- Project root
- Data directory
- Temporary directory
- Test data directory

Usage:
    from aiforge.config import config
    
    # Accessing configuration directories
    data_dir = config.data_dir
    tmp_dir = config.tmp_dir
    test_data_dir = config.test_data_dir

Environment Variables:
    AIFORGE_PROJECT_ROOT: Sets the project root directory
    AIFORGE_DATA_DIR: Sets the data directory
    AIFORGE_TMP_DIR: Sets the temporary directory
    AIFORGE_TEST_DATA_DIR: Sets the test data directory

If environment variables are not set, default values are used based on the project structure.

Usage in other modules:
    from aiforge.config import config
    ... config.data_dir, config.tmp_dir ...

Author: [Your Name]
Date: [Current Date]
Version: 1.0
"""

import os
from pathlib import Path


class AiForgeConfig:
    """
    A configuration class for managing directories in the AiForge project.

    This class handles the setup and management of essential directories used in the AiForge project.
    It provides a centralized way to access project directories and allows for flexible configuration
    through environment variables.

    Attributes:
        project_root (Path): The root directory of the AiForge project.
        data_dir (Path): The directory for storing project data.
        tmp_dir (Path): The directory for temporary files.
        test_data_dir (Path): The directory for test data.

    Methods:
        _get_project_root(): Determines the project root directory.
        _get_directory(env_var, default_name): Sets up a directory based on environment variables or defaults.
    """

    def __init__(self):
        """
        Initializes the AiForgeConfig instance by setting up all required directories.
        """
        self.project_root = self._get_project_root()
        self.data_dir = self._get_directory("AIFORGE_DATA_DIR", "data")
        self.tmp_dir = self._get_directory("AIFORGE_TMP_DIR", "tmp")
        self.test_data_dir = self._get_directory("AIFORGE_TEST_DATA_DIR", "data_test")

    def _get_project_root(self):
        """
        Determines the project root directory.

        Returns:
            Path: The project root directory.

        The method first checks for an environment variable 'AIFORGE_PROJECT_ROOT'.
        If not set, it uses the current working directory as the project root.
        """
        env_root = os.environ.get("AIFORGE_PROJECT_ROOT")
        if env_root:
            return Path(env_root)
        return Path.cwd()

    def _get_directory(self, env_var, default_name):
        """
        Sets up a directory based on environment variables or defaults.

        Args:
            env_var (str): The name of the environment variable to check.
            default_name (str): The default directory name if the environment variable is not set.

        Returns:
            Path: The path to the directory.

        This method checks for an environment variable. If set, it uses that path.
        Otherwise, it creates a subdirectory in the project root using the default name.
        The method ensures that the directory exists before returning its path.
        """
        env_dir = os.environ.get(env_var)
        if env_dir:
            dir_path = Path(env_dir)
        else:
            dir_path = self.project_root / default_name

        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path


# Create a global instance of the configuration
config = AiForgeConfig()
