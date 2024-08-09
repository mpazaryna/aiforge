from pathlib import Path

import pytest

from aiforge import config
from aiforge.utils.file_utils import get_file, write_to_file


@pytest.mark.parametrize("persistent", [True, False])
def test_write_to_file(persistent):
    content = "Test content"
    filename = "test_file.txt"

    file_path = write_to_file(content, filename, persistent)

    expected_dir = config.DATA_DIR if persistent else config.TMP_DIR
    assert file_path == expected_dir / filename
    assert file_path.exists()

    with open(file_path, "r") as f:
        assert f.read() == content

    # Print file location for manual cleanup
    print(f"\nTest file created at: {file_path}")
    print("Please remove this file manually after inspection.")


# @pytest.mark.skip(reason="Skipping for now")
def test_write_to_file_with_tuples():
    content = [("Title 1", "Content 1"), ("Title 2", "Content 2")]
    filename = "test_file_tuples.txt"

    file_path = write_to_file(content, filename, False)

    assert file_path == config.TMP_DIR / filename
    assert file_path.exists()

    with open(file_path, "r") as f:
        file_content = f.read()
        assert "Content from Title 1:" in file_content
        assert "Content 1" in file_content
        assert "Content from Title 2:" in file_content
        assert "Content 2" in file_content

    # Note: We're not cleaning up this file anymore


@pytest.mark.skip(reason="Skipping for now")
def test_validate_tmp_folder():
    """
    Test that the TMP_DIR in the config is set to the correct path.
    """
    expected_tmp_path = Path("/Users/mpaz/github/advanced-python-project/tmp")

    assert (
        config.TMP_DIR == expected_tmp_path
    ), f"TMP_DIR is incorrect. Expected {expected_tmp_path}, got {config.TMP_DIR}"

    # Print out the actual TMP_DIR for debugging
    print(f"Actual TMP_DIR: {config.TMP_DIR}")

    # Check if the directory actually exists
    assert config.TMP_DIR.exists(), f"The directory {config.TMP_DIR} does not exist"

    # Print out the contents of the TMP_DIR for debugging
    print("Contents of TMP_DIR:")
    for item in config.TMP_DIR.iterdir():
        print(f" - {item.name}")

    # Check specifically for test_file_tuples.txt
    test_file_tuples_path = config.TMP_DIR / "test_file_tuples.txt"
    if test_file_tuples_path.exists():
        print("test_file_tuples.txt found in TMP_DIR")
        with open(test_file_tuples_path, "r") as f:
            print("Contents of test_file_tuples.txt:")
            print(f.read())
    else:
        print("test_file_tuples.txt not found in TMP_DIR")


# @pytest.mark.skip(reason="Skipping for now")
def test_get_file_binary():
    """
    Test that get_file can retrieve a binary file (test.png) from the project's tmp folder.
    """
    # Use the correct tmp directory from config
    tmp_dir = config.TMP_DIR

    # Print debugging information
    print(f"TMP_DIR from config: {tmp_dir}")

    # Path to test.png
    test_png_path = tmp_dir / "test.png"

    # Check if test.png exists
    assert test_png_path.exists(), f"test.png not found at {test_png_path}"

    # Try to get the file
    file_content = get_file("test.png", persistent=False, binary=True)

    # Check that we got some content
    assert file_content, "File content is empty"

    # Check that the content is bytes
    assert isinstance(file_content, bytes), "File content is not in binary format"

    # Check for PNG signature
    assert file_content.startswith(b"\x89PNG"), "File does not start with PNG signature"
