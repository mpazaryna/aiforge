import json

import pytest

from aiforge.config import config
from aiforge.utils.file_utils import get_directory, get_file, write_to_file
from aiforge.utils.json_utils import process_json_data, read_json_file, write_json_file


@pytest.fixture
def setup_test_data():
    test_data = {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ],
        "settings": {"theme": "dark", "notifications": {"email": True, "push": False}},
    }
    filename = "test_data.json"
    write_to_file(json.dumps(test_data), filename, "tmp")
    return filename


@pytest.fixture(autouse=True)
def cleanup():
    yield
    # Clean up the test file after each test
    tmp_dir = get_directory("tmp")
    test_file = tmp_dir / "test_data.json"
    if test_file.exists():
        test_file.unlink()


def test_process_json_data(setup_test_data):
    json_data = get_file(setup_test_data, "tmp")

    # Test without key path
    result = process_json_data(json_data)
    assert isinstance(result, dict)
    assert "users" in result
    assert "settings" in result

    # Test with key path
    result = process_json_data(json_data, "users.0.name")
    assert result == "John Doe"

    # Test with nested key path
    result = process_json_data(json_data, "settings.notifications.email")
    assert result == True

    # Test with invalid key path
    result = process_json_data(json_data, "invalid.key.path")
    assert result is None


def test_read_json_file(setup_test_data):
    result = read_json_file(setup_test_data, "tmp", key_path="users.1.name")
    assert result == "Jane Smith"

    result = read_json_file(setup_test_data, "tmp", key_path="users.0.name")
    assert result == "John Doe"


def test_read_json_file_not_found():
    result = read_json_file("non_existent.json", "tmp")
    assert result is None


def test_write_json_file():
    data = {"key": "value"}
    filename = "output.json"

    result = write_json_file(data, filename, "tmp")
    assert result == True

    # Verify the written data
    written_data = json.loads(get_file(filename, "tmp"))
    assert written_data == data

    # Clean up
    tmp_dir = get_directory("tmp")
    (tmp_dir / filename).unlink()


def test_write_json_file_error():
    data = {"key": "value"}
    # Attempt to write to a directory that doesn't exist
    result = write_json_file(data, "test.json", "non_existent_dir")
    assert result == False
