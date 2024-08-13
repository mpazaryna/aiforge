import json

import pytest

from aiforge.utils.file_utils import open_project_file, write_to_file


@pytest.fixture(scope="module")
def setup_test_data():
    # Create a sample user_data.json file in the test_data directory
    sample_data = {
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ]
    }
    write_to_file(json.dumps(sample_data), "user_data.json", directory="test_data")


def test_user_data_file_content(setup_test_data):
    with open_project_file("user_data.json", directory="test_data", mode="r") as f:
        content = json.load(f)
    assert "users" in content
    assert isinstance(content["users"], list)


def test_user_data_structure(setup_test_data):
    with open_project_file("user_data.json", directory="test_data", mode="r") as f:
        data = json.load(f)

    assert "users" in data
    for user in data["users"]:
        assert "id" in user
        assert "name" in user
        assert "email" in user


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        open_project_file("non_existent_file.json", directory="test_data", mode="r")


def test_invalid_json(setup_test_data):
    # Create a temporary file with invalid JSON
    write_to_file("invalid json", "invalid_user_data.json", directory="test_data")

    with pytest.raises(json.JSONDecodeError):
        with open_project_file(
            "invalid_user_data.json", directory="test_data", mode="r"
        ) as f:
            json.load(f)


def test_missing_users_key(setup_test_data):
    # Create a temporary file with missing 'users' key
    write_to_file(
        json.dumps({"data": []}), "missing_key_user_data.json", directory="test_data"
    )

    with open_project_file(
        "missing_key_user_data.json", directory="test_data", mode="r"
    ) as f:
        data = json.load(f)

    assert "users" not in data
