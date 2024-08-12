# src/aiforge/utils/file_utils.py

from pathlib import Path
from typing import List, Literal, Tuple, Union

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


def open_project_file(
    directory: Literal["data", "tmp"], filename: str, mode: str = "r"
) -> Union[Path, None]:
    """
    Open a file from either the data or tmp directory of the project.

    Args:
        directory (Literal['data', 'tmp']): The directory to look in ('data' or 'tmp').
        filename (str): The name of the file to open.
        mode (str): The mode in which to open the file. Defaults to 'r' (read mode).

    Returns:
        Union[Path, None]: The opened file as a Path object if successful, None otherwise.

    Raises:
        ValueError: If an invalid directory is specified.
    """
    if directory == "data":
        file_path = config.data_dir / filename
    elif directory == "tmp":
        file_path = config.tmp_dir / filename
    else:
        raise ValueError("Invalid directory specified. Use 'data' or 'tmp'.")

    if "w" in mode or "a" in mode or file_path.exists():
        return file_path.open(mode)
    else:
        print(f"File {filename} not found in {directory} directory.")
        return None
