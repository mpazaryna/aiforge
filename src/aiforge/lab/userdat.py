import json
from pathlib import Path

from aiforge.utils.file_utils import get_file


def parse_user_data(file_path=None):
    try:
        # If no file_path is provided, use the default
        if file_path is None:
            json_data = get_file("user_data.json", directory="tmp")
        else:
            with open(file_path, "r") as f:
                json_data = f.read()

        # Parse the JSON data
        data = json.loads(json_data)

        # Extract and print user information
        for user in data.get("users", []):
            print(
                f"ID: {user.get('id')}, Name: {user.get('name')}, Email: {user.get('email')}"
            )

        return data.get("users", [])
    except FileNotFoundError:
        print(f"Error: user_data.json file not found in specified location")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in user_data.json")
        return []


if __name__ == "__main__":
    parse_user_data()
