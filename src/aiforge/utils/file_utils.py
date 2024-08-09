# src/aiforge/utils/file_utils.py

from pathlib import Path
from typing import List, Tuple, Union

from aiforge.config import config


def write_to_file(
    content: Union[str, List[Tuple[str, str]]],
    output_filename: str,
    persistent: bool = False,
) -> Path:
    """
    Write content to a file in either the tmp or data directory.

    Args:
        content (Union[str, List[Tuple[str, str]]]): The content to write. If a string, writes directly.
                                                     If a list of tuples, each tuple should be (title, content).
        output_filename (str): The name of the file to save the content.
        persistent (bool): If True, save to data folder; if False, save to tmp folder.

    Returns:
        Path: The path to the written file.
    """
    output_dir = config.data_dir if persistent else config.tmp_dir
    output_file_path = output_dir / output_filename

    if isinstance(content, str):
        with open(output_file_path, "w") as f:
            f.write(content)
    else:
        with open(output_file_path, "w") as f:
            for title, text in content:
                f.write(f"Content from {title}:\n{text}\n\n")

    return output_file_path


def get_file(
    filename: str, persistent: bool = False, binary: bool = False
) -> Union[str, bytes]:
    """
    Retrieve content from a file in either the tmp or data directory.

    Args:
        filename (str): The name of the file to retrieve.
        persistent (bool): If True, look in data folder; if False, look in tmp folder.
        binary (bool): If True, read file in binary mode.

    Returns:
        Union[str, bytes]: The content of the file.
    """
    file_dir = config.data_dir if persistent else config.tmp_dir
    file_path = file_dir / filename

    mode = "rb" if binary else "r"
    with open(file_path, mode) as f:
        return f.read()


# You can add more utility functions here as needed
