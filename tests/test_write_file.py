import os
from pathlib import Path

import pytest

from aiforge.config import AiForgeConfig
from aiforge.utils.file_utils import get_file, write_to_file


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    # Set up test environment variables
    test_root = Path.cwd() / "test_root"
    monkeypatch.setenv("AIFORGE_PROJECT_ROOT", str(test_root))
    monkeypatch.setenv("AIFORGE_DATA_DIR", str(test_root / "test_data"))
    monkeypatch.setenv("AIFORGE_TMP_DIR", str(test_root / "test_tmp"))

    # Create a new config instance for each test
    test_config = AiForgeConfig()

    # Create test directories
    test_config.data_dir.mkdir(parents=True, exist_ok=True)
    test_config.tmp_dir.mkdir(parents=True, exist_ok=True)

    yield test_config

    # Clean up
    import shutil

    shutil.rmtree(test_root)


@pytest.mark.parametrize("persistent", [True, False])
def test_write_to_file(persistent, setup_test_environment, monkeypatch):
    monkeypatch.setattr("aiforge.utils.file_utils.config", setup_test_environment)

    content = "Test content"
    filename = "test_file.txt"

    file_path = write_to_file(content, filename, persistent)

    expected_dir = (
        setup_test_environment.data_dir
        if persistent
        else setup_test_environment.tmp_dir
    )
    assert file_path == expected_dir / filename
    assert file_path.exists()

    with open(file_path, "r") as f:
        assert f.read() == content


def test_write_to_file_with_tuples(setup_test_environment, monkeypatch):
    monkeypatch.setattr("aiforge.utils.file_utils.config", setup_test_environment)

    content = [("Title 1", "Content 1"), ("Title 2", "Content 2")]
    filename = "test_file_tuples.txt"

    file_path = write_to_file(content, filename, False)

    assert file_path == setup_test_environment.tmp_dir / filename
    assert file_path.exists()

    with open(file_path, "r") as f:
        file_content = f.read()
        assert "Content from Title 1:" in file_content
        assert "Content 1" in file_content
        assert "Content from Title 2:" in file_content
        assert "Content 2" in file_content


def test_config_directories(setup_test_environment):
    assert setup_test_environment.project_root == Path.cwd() / "test_root"
    assert setup_test_environment.data_dir == Path.cwd() / "test_root" / "test_data"
    assert setup_test_environment.tmp_dir == Path.cwd() / "test_root" / "test_tmp"


def test_get_file_binary(setup_test_environment, monkeypatch):
    monkeypatch.setattr("aiforge.utils.file_utils.config", setup_test_environment)

    # Create a test PNG file
    test_png_path = setup_test_environment.tmp_dir / "test.png"
    test_png_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"

    with open(test_png_path, "wb") as f:
        f.write(test_png_content)

    # Try to get the file
    file_content = get_file("test.png", persistent=False, binary=True)

    # Check that we got some content
    assert file_content, "File content is empty"

    # Check that the content is bytes
    assert isinstance(file_content, bytes), "File content is not in binary format"

    # Check for PNG signature
    assert file_content.startswith(b"\x89PNG"), "File does not start with PNG signature"


# You can add more tests here as needed
