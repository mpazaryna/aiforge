import os
from pathlib import Path

import pytest

from aiforge.config import AiForgeConfig


@pytest.fixture(scope="session")
def temp_env(tmp_path_factory):
    """Fixture to set up a temporary environment for testing."""
    tmp_path = tmp_path_factory.mktemp("aiforge")
    original_env = os.environ.copy()
    os.environ["AIFORGE_PROJECT_ROOT"] = str(tmp_path)
    os.environ["AIFORGE_DATA_DIR"] = str(tmp_path / "data")
    os.environ["AIFORGE_TMP_DIR"] = str(tmp_path / "tmp")
    os.environ["AIFORGE_TEST_DATA_DIR"] = str(tmp_path / "data/test")
    yield tmp_path
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture(scope="function")
def config(temp_env):
    """Fixture to provide an AiForgeConfig instance."""
    config = AiForgeConfig()
    config.ensure_directories_exist()  # Only create directories when needed
    return config


def test_subdirectory_in_tmp(config):
    """Test creating a subdirectory in tmp, writing a file, and cleaning up."""
    # Create a subdirectory in the tmp directory
    subdir_name = "test_subdir"
    subdir_path = Path(config.tmp_dir) / subdir_name
    subdir_path.mkdir(exist_ok=True)

    # Create a file in the subdirectory
    file_name = "test_file.txt"
    file_path = subdir_path / file_name
    file_content = "This is a test file."

    with file_path.open("w") as f:
        f.write(file_content)

    # Assert that the file exists and has the correct content
    assert file_path.exists()
    assert file_path.read_text() == file_content

    # Clean up: remove the file and the subdirectory
    file_path.unlink()
    subdir_path.rmdir()

    # Assert that the subdirectory and file no longer exist
    assert not file_path.exists()
    assert not subdir_path.exists()


def test_config_initialization(temp_env):
    """Test that AiForgeConfig initializes correctly with environment variables."""
    config = AiForgeConfig()
    config.ensure_directories_exist()

    assert os.environ["AIFORGE_PROJECT_ROOT"] == str(temp_env)
    assert os.path.samefile(config.tmp_dir, os.environ["AIFORGE_TMP_DIR"])
    assert os.path.samefile(config.data_dir, os.environ["AIFORGE_DATA_DIR"])
    assert os.path.samefile(config.test_data_dir, os.environ["AIFORGE_TEST_DATA_DIR"])


def test_directory_existence(config):
    """Test that the required directories exist."""
    assert Path(config.tmp_dir).exists()
    assert Path(config.data_dir).exists()
    assert Path(config.test_data_dir).exists()


# You can add more tests as needed
