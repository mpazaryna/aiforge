import json
import os
from pathlib import Path

import pytest

from aiforge.lab.userdat import parse_user_data
from aiforge.utils.file_utils import write_to_file


@pytest.fixture(scope="module")
def output_files(tmp_path_factory):
    base_path = tmp_path_factory.mktemp("user_data")
    return {
        "user_data": base_path / "user_data.json",
        "user_data_bak": base_path / "user_data.json.bak",
    }


@pytest.fixture(autouse=True)
def cleanup(output_files):
    yield
    if os.environ.get("KEEP_TEST_FILES", "").lower() != "true":
        for file_path in output_files.values():
            if file_path.exists():
                file_path.unlink()
    else:
        print("\nTest files were not deleted. You can find them at:")
        for key, file_path in output_files.items():
            if file_path.exists():
                print(f"- {key}: {file_path}")


@pytest.fixture
def setup_test_data(output_files):
    # Create a temporary JSON file with test data
    test_data = {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ]
    }
    write_to_file(json.dumps(test_data), str(output_files["user_data"]))
    yield output_files["user_data"]
    # Cleanup is handled by the cleanup fixture


def test_parse_user_data(setup_test_data, capsys):
    # Call the function with the test file path
    users = parse_user_data(setup_test_data)

    # Check the output
    captured = capsys.readouterr()
    assert "ID: 1, Name: John Doe, Email: john@example.com" in captured.out
    assert "ID: 2, Name: Jane Smith, Email: jane@example.com" in captured.out

    # Check the returned data
    assert len(users) == 2
    assert users[0]["id"] == 1
    assert users[0]["name"] == "John Doe"
    assert users[0]["email"] == "john@example.com"
    assert users[1]["id"] == 2
    assert users[1]["name"] == "Jane Smith"
    assert users[1]["email"] == "jane@example.com"


def test_parse_user_data_file_not_found(output_files, capsys):
    # Use a non-existent file path
    non_existent_file = output_files["user_data"].parent / "non_existent.json"

    # Call the function with the non-existent file path
    users = parse_user_data(non_existent_file)

    # Check the output
    captured = capsys.readouterr()
    assert "Error: user_data.json file not found in specified location" in captured.out

    # Check the returned data
    assert len(users) == 0


def test_parse_user_data_invalid_json(output_files, capsys):
    # Write invalid JSON to the file
    invalid_json_file = output_files["user_data"].parent / "invalid.json"
    write_to_file("invalid json", str(invalid_json_file))

    # Call the function with the invalid JSON file
    users = parse_user_data(invalid_json_file)

    # Check the output
    captured = capsys.readouterr()
    assert "Error: Invalid JSON format in user_data.json" in captured.out

    # Check the returned data
    assert len(users) == 0
