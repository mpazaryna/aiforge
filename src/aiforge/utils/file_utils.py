from pathlib import Path
from typing import List, Tuple, Union

from aiforge import config


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path: The path to the project root.
    """
    return config.PROJECT_ROOT


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
    output_dir = config.DATA_DIR if persistent else config.TMP_DIR
    output_file_path = output_dir / output_filename

    with open(output_file_path, "w", encoding="utf-8") as f:
        if isinstance(content, str):
            f.write(content)
        else:
            for title, text in content:
                f.write(f"Content from {title}: \n\n")
                f.write(text)
                f.write("\n\n" + "-" * 80 + "\n\n")

    return output_file_path


def get_file(
    filename: str, persistent: bool = False, binary: bool = False
) -> Union[str, bytes]:
    """
    Retrieve the contents of a file from either the tmp or data directory.

    Args:
        filename (str): The name of the file to retrieve.
        persistent (bool): If True, look in the data folder; if False, look in the tmp folder.
        binary (bool): If True, read the file in binary mode.

    Returns:
        Union[str, bytes]: The contents of the file, as a string or bytes object.

    Raises:
        FileNotFoundError: If the file doesn't exist in the specified location.
        IOError: If there's an error reading the file.
    """
    file_dir = config.DATA_DIR if persistent else config.TMP_DIR
    file_path = file_dir / filename

    print(f"get_file is looking for file at: {file_path}")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        mode = "rb" if binary else "r"
        encoding = None if binary else "utf-8"
        with open(file_path, mode, encoding=encoding) as f:
            return f.read()
    except IOError as e:
        raise IOError(f"Error reading file {file_path}: {str(e)}")
