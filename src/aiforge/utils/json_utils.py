import json
from typing import Any, Dict, List, Union

from aiforge.utils.file_utils import get_file, write_to_file


def process_json_data(json_data: Union[str, Dict, List], key_path: str = None) -> Any:
    """
    Process JSON data and return the specified data based on the key path.

    :param json_data: JSON data as a string, dictionary, or list
    :param key_path: Dot-separated string indicating the path to the desired data
    :return: The data at the specified key path, or the entire data if no key path is provided
    """
    try:
        # Parse the JSON data if it's a string
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data

        # If no key path is provided, return the entire data
        if not key_path:
            return data

        # Navigate through the data structure based on the key path
        keys = key_path.split(".")
        for key in keys:
            if isinstance(data, dict):
                if key not in data:
                    return None
                data = data[key]
            elif isinstance(data, list) and key.isdigit():
                index = int(key)
                if index >= len(data):
                    return None
                data = data[index]
            else:
                return None

        return data

    except json.JSONDecodeError:
        print("Error: Invalid JSON format")
        return None
    except Exception as e:
        print(f"Error processing JSON data: {str(e)}")
        return None


def read_json_file(filename: str, directory: str = "tmp", key_path: str = None) -> Any:
    """
    Read JSON data from a file in the specified directory and process it.

    :param filename: Name of the file to read
    :param directory: Directory to read from ('tmp' or 'data'). Defaults to 'tmp'
    :param key_path: Dot-separated string indicating the path to the desired data
    :return: Processed JSON data
    """
    try:
        json_data = get_file(filename, directory)
        return process_json_data(json_data, key_path)
    except FileNotFoundError:
        print(f"Error: File {filename} not found in {directory} directory")
        return None


def write_json_file(
    data: Union[Dict, List], filename: str, directory: str = "tmp"
) -> bool:
    """
    Write JSON data to a file in the specified directory.

    :param data: Data to write (must be JSON serializable)
    :param filename: Name of the file to write
    :param directory: Directory to write to ('tmp' or 'data'). Defaults to 'tmp'
    :return: True if write was successful, False otherwise
    """
    try:
        json_data = json.dumps(data, indent=2)
        write_to_file(json_data, filename, directory)
        return True
    except Exception as e:
        print(f"Error writing JSON data to file: {str(e)}")
        return False
