from pathlib import Path

import pytest

from aiforge.config import config
from aiforge.utils.file_utils import open_project_file


@pytest.fixture(scope="module")
def setup_test_files():
    # Create test files
    (config.data_dir / "test_file_data.txt").write_text("Test data file content")
    (config.tmp_dir / "test_file_tmp.txt").write_text("Test tmp file content")

    yield

    # Clean up test files
    (config.data_dir / "test_file_data.txt").unlink(missing_ok=True)
    (config.tmp_dir / "test_file_tmp.txt").unlink(missing_ok=True)
    (config.tmp_dir / "test_file_write.txt").unlink(missing_ok=True)


def test_open_project_file_data_directory(setup_test_files):
    with open_project_file("data", "test_file_data.txt", "r") as file:
        assert file is not None
        content = file.read()
        assert content == "Test data file content"


def test_open_project_file_tmp_directory(setup_test_files):
    with open_project_file("tmp", "test_file_tmp.txt", "r") as file:
        assert file is not None
        content = file.read()
        assert content == "Test tmp file content"


def test_open_project_file_write_mode(setup_test_files):
    with open_project_file("tmp", "test_file_write.txt", "w") as file:
        assert file is not None
        file.write("New content")

    # Verify the content was written
    with open(config.tmp_dir / "test_file_write.txt", "r") as file:
        content = file.read()
        assert content == "New content"


def test_open_project_file_nonexistent_file():
    result = open_project_file("data", "nonexistent.txt", "r")
    assert result is None


def test_open_project_file_invalid_directory():
    with pytest.raises(
        ValueError, match="Invalid directory specified. Use 'data' or 'tmp'."
    ):
        open_project_file("invalid", "test.txt")


# Run the tests with: pytest test_file_utils.py
