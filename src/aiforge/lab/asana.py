from typing import Dict, List

from aiforge.config import config
from aiforge.utils.json_utils import read_json_file


def load_asanas() -> List[Dict[str, str]]:
    asanas = read_json_file("asana.json", directory="tmp")
    if asanas is None:
        raise ValueError(
            "Failed to load asanas data. Check the logs for more information."
        )
    return asanas


def print_asanas(asanas: List[Dict[str, str]]):
    print(f"Loaded {len(asanas)} asanas:")
    for asana in asanas[:5]:  # Print first 5 asanas as an example
        print(
            f"ID: {asana['id']}, Name: {asana['name']}, Sanskrit: {asana['sanskrit']}"
        )
    print("...")


def main():
    try:
        asanas = load_asanas()
        print_asanas(asanas)
    except ValueError as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
