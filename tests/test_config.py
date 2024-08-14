import os
import sys
from pathlib import Path

import pytest

from aiforge.config import AiForgeConfig


@pytest.fixture
def temp_env(tmp_path):
    """Fixture to set up a temporary environment for testing."""
    original_env = os.environ.copy()
    os.environ["AIFORGE_PROJECT_ROOT"] = str(tmp_path)
    os.environ["AIFORGE_TMP_DIR"] = str(tmp_path / "custom_tmp")
    os.environ["AIFORGE_DATA_DIR"] = str(tmp_path / "custom_data")
    os.environ["AIFORGE_TEST_DATA_DIR"] = str(tmp_path / "custom_test_data")
    yield tmp_path
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture(autouse=True)
def reset_config_env(temp_env):
    """Reset environment variables before each test."""
    original_env = os.environ.copy()
    os.environ["AIFORGE_PROJECT_ROOT"] = str(temp_env)
    os.environ["AIFORGE_TMP_DIR"] = str(temp_env / "custom_tmp")
    os.environ["AIFORGE_DATA_DIR"] = str(temp_env / "custom_data")
    os.environ["AIFORGE_TEST_DATA_DIR"] = str(temp_env / "custom_test_data")
    yield
    os.environ.clear()
    os.environ.update(original_env)


def test_global_config_instance(temp_env):
    """Test that the global config instance is created correctly."""
    import importlib

    import aiforge.config

    # Debug information
    print(f"Python version: {sys.version}")
    print(f"aiforge.config module location: {aiforge.config.__file__}")
    print(f"AiForgeConfig in test file: {AiForgeConfig}")
    print(f"AiForgeConfig in aiforge.config: {aiforge.config.AiForgeConfig}")

    importlib.reload(aiforge.config)

    config = aiforge.config.config

    print(f"Type of config: {type(config)}")
    print(f"Config object: {config}")

    assert isinstance(config, aiforge.config.AiForgeConfig)

    # Rest of the assertions
    assert config.project_root == temp_env
    assert config.data_dir == temp_env / "custom_data"
    assert config.tmp_dir == temp_env / "custom_tmp"
    assert config.test_data_dir == temp_env / "custom_test_data"

    # Verify that the directories exist
    assert config.data_dir.exists()
    assert config.tmp_dir.exists()
    assert config.test_data_dir.exists()


def test_config_initialization(temp_env):
    """Test that AiForgeConfig initializes correctly with environment variables."""
    test_config = AiForgeConfig()
    assert test_config.project_root == temp_env
    assert test_config.tmp_dir == temp_env / "custom_tmp"
    assert test_config.data_dir == temp_env / "custom_data"
    assert test_config.test_data_dir == temp_env / "custom_test_data"


def test_write_file_to_tmp(temp_env):
    """Test writing a file to the tmp directory."""
    test_config = AiForgeConfig()
    file_path = test_config.tmp_dir / "test_file.txt"
    with file_path.open("w") as f:
        f.write("Test content")

    assert file_path.exists()
    assert file_path.read_text() == "Test content"


def test_write_file_to_sample_subdir(temp_env):
    """Test writing a file to tmp/sample_subdir."""
    test_config = AiForgeConfig()
    subdir_path = test_config.tmp_dir / "sample_subdir"
    subdir_path.mkdir(exist_ok=True)
    file_path = subdir_path / "test_subdir_file.txt"

    with file_path.open("w") as f:
        f.write("Subdir test content")

    assert file_path.exists()
    assert file_path.read_text() == "Subdir test content"


def test_custom_data_dir(temp_env):
    """Test setting a custom data directory through environment variable."""
    custom_data_dir = temp_env / "custom_data"
    test_config = AiForgeConfig()
    assert test_config.data_dir == custom_data_dir
    assert custom_data_dir.exists()


def test_directory_creation(temp_env):
    """Test that directories are created if they don't exist."""
    # Remove the environment variables to test default directory creation
    for env_var in ["AIFORGE_DATA_DIR", "AIFORGE_TMP_DIR", "AIFORGE_TEST_DATA_DIR"]:
        os.environ.pop(env_var, None)

    test_config = AiForgeConfig()

    # Check that default directories are created
    assert (temp_env / "data/out").exists()
    assert (temp_env / "tmp").exists()
    assert (temp_env / "data/test").exists()

    # Ensure directories are empty before attempting to remove them
    for dir_path in [
        (temp_env / "data/out"),
        (temp_env / "tmp"),
        (temp_env / "data/test"),
    ]:
        for item in dir_path.iterdir():
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                for sub_item in item.iterdir():
                    sub_item.unlink()
                item.rmdir()
        dir_path.rmdir()
        assert not dir_path.exists()

    # Recreate config to trigger directory creation
    test_config = AiForgeConfig()
    assert (temp_env / "data/out").exists()
    assert (temp_env / "tmp").exists()
    assert (temp_env / "data/test").exists()


# ... (other test functions)
