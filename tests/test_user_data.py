# File: tests/test_user_data.py

import json

import pytest

from aiforge.config import config
from aiforge.utils.file_utils import open_project_file


def test_user_data_file_content():
    with open_project_file("data", "user_data.json", "r") as f:
        data = json.load(f)
    assert "users" in data
    assert isinstance(data["users"], list)
    assert all(isinstance(user, dict) for user in data["users"])
    assert all(
        "id" in user and "name" in user and "email" in user for user in data["users"]
    )


def test_user_data_structure():
    with open_project_file("data", "user_data.json", "r") as f:
        data = json.load(f)
    users = data["users"]
    assert isinstance(users, list)
    assert all(isinstance(user, dict) for user in users)
    assert all("id" in user and "name" in user and "email" in user for user in users)


def test_file_not_found():
    result = open_project_file("data", "non_existent_file.json", "r")
    assert result is None


def test_invalid_json():
    # Create a temporary file with invalid JSON
    temp_file = config.data_dir / "invalid_user_data.json"
    temp_file.write_text("invalid json")

    with pytest.raises(json.JSONDecodeError):
        with open_project_file("data", "invalid_user_data.json", "r") as f:
            json.load(f)

    # Clean up the temporary file
    temp_file.unlink()


def test_missing_users_key():
    # Create a temporary file with missing 'users' key
    temp_file = config.data_dir / "missing_key_user_data.json"
    temp_file.write_text(json.dumps({"data": []}))

    with open_project_file("data", "missing_key_user_data.json", "r") as f:
        data = json.load(f)
        assert "users" not in data

    # Clean up the temporary file
    temp_file.unlink()


# Run the tests with: pytest tests/test_user_data.py
