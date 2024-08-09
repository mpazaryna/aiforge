import json
import os
from pathlib import Path

import pytest

from aiforge.config import config
from aiforge.vectorstore.chunking import chunk_text, save_chunks_to_json


@pytest.fixture
def sample_text_file():
    file_name = "sample.txt"
    file_path = config.data_dir / file_name
    with open(file_path, "w") as f:
        f.write(
            "This is a sample text. It will be used for testing the chunking function."
        )
    yield file_name
    os.remove(file_path)


def test_chunk_text(sample_text_file):
    chunk_size = 20
    chunks = chunk_text(sample_text_file, chunk_size=chunk_size)

    # Read the original text
    with open(config.data_dir / sample_text_file, "r") as f:
        original_text = f.read()

    # Test 1: Check if the number of chunks is correct
    expected_chunks = len(original_text) // chunk_size + (
        1 if len(original_text) % chunk_size != 0 else 0
    )
    assert (
        len(chunks) == expected_chunks
    ), f"Expected {expected_chunks} chunks, but got {len(chunks)}"

    # Test 2: Check if each chunk has the correct size (except possibly the last one)
    for i, chunk in enumerate(chunks[:-1]):
        assert (
            len(chunk) == chunk_size
        ), f"Chunk {i} has length {len(chunk)}, expected {chunk_size}"

    # Test 3: Check if the last chunk has the correct size
    assert (
        len(chunks[-1]) <= chunk_size
    ), f"Last chunk has length {len(chunks[-1])}, expected <= {chunk_size}"

    # Test 4: Check if concatenating all chunks produces the original text
    assert (
        "".join(chunks) == original_text
    ), "Concatenated chunks do not match the original text"


def test_save_chunks_to_json():
    chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
    output_file = "output.json"
    save_chunks_to_json(chunks, output_file)

    file_path = config.tmp_dir / output_file
    assert file_path.exists()
    with open(file_path, "r") as f:
        data = json.load(f)
    assert data == {"chunks": chunks}
    os.remove(file_path)


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        chunk_text("non_existent_file.txt")


def test_chunk_and_save_real_data():
    input_file = "my_test_data.txt"
    output_file = "my_test_data.json"
    chunk_size = 100

    # Ensure the input file exists
    input_path = config.data_dir / input_file
    assert input_path.exists(), f"Test file {input_file} not found in {config.data_dir}"

    # Read the original content
    with open(input_path, "r") as f:
        original_content = f.read()

    # Chunk the text
    chunks = chunk_text(input_file, chunk_size=chunk_size)

    # Save chunks to JSON
    save_chunks_to_json(chunks, output_file)

    # Verify the output file exists
    output_path = config.tmp_dir / output_file
    assert (
        output_path.exists()
    ), f"Output file {output_file} not created in {config.tmp_dir}"

    # Read the saved JSON
    with open(output_path, "r") as f:
        saved_data = json.load(f)

    # Verify the structure of the saved data
    assert "chunks" in saved_data, "Saved JSON does not contain 'chunks' key"
    assert isinstance(saved_data["chunks"], list), "Saved chunks is not a list"

    # Verify the content of the chunks
    reconstructed_text = "".join(saved_data["chunks"])
    assert (
        reconstructed_text == original_content
    ), "Reconstructed text does not match original"

    # Verify chunk sizes
    for i, chunk in enumerate(saved_data["chunks"][:-1]):
        assert len(chunk) == chunk_size, f"Chunk {i} has incorrect length: {len(chunk)}"
    assert (
        len(saved_data["chunks"][-1]) <= chunk_size
    ), f"Last chunk has incorrect length: {len(saved_data['chunks'][-1])}"

    # Clean up
    os.remove(output_path)


@pytest.fixture
def sample_text_files():
    file_contents = {
        "sherlock.txt": "To Sherlock Holmes she is always THE woman. I have seldom heard him mention her under any other name.",
        "gatsby.txt": "In my younger and more vulnerable years my father gave me some advice that I've been turning over in my mind ever since.",
        "moby_dick.txt": "Call me Ishmael. Some years ago—never mind how long precisely—having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world.",
    }

    created_files = []
    for filename, content in file_contents.items():
        file_path = config.data_dir / filename
        with open(file_path, "w") as f:
            f.write(content)
        created_files.append(filename)

    yield created_files

    # Clean up
    for filename in created_files:
        os.remove(config.data_dir / filename)


def test_process_multiple_files(sample_text_files):
    chunk_size = 50

    for input_file in sample_text_files:
        # Read original content
        with open(config.data_dir / input_file, "r") as f:
            original_content = f.read()

        # Chunk the text
        chunks = chunk_text(input_file, chunk_size=chunk_size)

        # Save chunks to JSON
        output_file = f"{Path(input_file).stem}_chunks.json"
        save_chunks_to_json(chunks, output_file)

        # Verify the output file exists
        output_path = config.tmp_dir / output_file
        assert (
            output_path.exists()
        ), f"Output file {output_file} not created in {config.tmp_dir}"

        # Read the saved JSON
        with open(output_path, "r") as f:
            saved_data = json.load(f)

        # Verify the structure of the saved data
        assert (
            "chunks" in saved_data
        ), f"Saved JSON for {input_file} does not contain 'chunks' key"
        assert isinstance(
            saved_data["chunks"], list
        ), f"Saved chunks for {input_file} is not a list"

        # Verify the content of the chunks
        reconstructed_text = "".join(saved_data["chunks"])
        assert (
            reconstructed_text == original_content
        ), f"Reconstructed text does not match original for {input_file}"

        # Verify chunk sizes
        for i, chunk in enumerate(saved_data["chunks"][:-1]):
            assert (
                len(chunk) == chunk_size
            ), f"Chunk {i} in {input_file} has incorrect length: {len(chunk)}"
        assert (
            len(saved_data["chunks"][-1]) <= chunk_size
        ), f"Last chunk in {input_file} has incorrect length: {len(saved_data['chunks'][-1])}"

        # Clean up
        # os.remove(output_path)

    # Verify all files were processed
    # assert (
    #    len(os.listdir(config.tmp_dir)) == 0
    # ), "Not all temporary files were cleaned up"


def test_process_multiple_files():
    chunk_size = 100
    input_files = ["moby_dick.txt", "sherlock_holmes.txt", "great_gatsby.txt"]

    for input_file in input_files:
        input_path = config.data_dir / input_file

        # Check if the file exists
        assert (
            input_path.exists()
        ), f"Test file {input_file} not found in {config.data_dir}"

        # Read original content
        with open(input_path, "r") as f:
            original_content = f.read()

        # Chunk the text
        chunks = chunk_text(input_file, chunk_size=chunk_size)

        # Save chunks to JSON
        output_file = f"{Path(input_file).stem}_chunks.json"
        save_chunks_to_json(chunks, output_file)

        # Verify the output file exists
        output_path = config.tmp_dir / output_file
        assert (
            output_path.exists()
        ), f"Output file {output_file} not created in {config.tmp_dir}"

        # Read the saved JSON
        with open(output_path, "r") as f:
            saved_data = json.load(f)

        # Verify the structure of the saved data
        assert (
            "chunks" in saved_data
        ), f"Saved JSON for {input_file} does not contain 'chunks' key"
        assert isinstance(
            saved_data["chunks"], list
        ), f"Saved chunks for {input_file} is not a list"

        # Verify the content of the chunks
        reconstructed_text = "".join(saved_data["chunks"])
        assert (
            reconstructed_text == original_content
        ), f"Reconstructed text does not match original for {input_file}"

        # Verify chunk sizes
        for i, chunk in enumerate(saved_data["chunks"][:-1]):
            assert (
                len(chunk) == chunk_size
            ), f"Chunk {i} in {input_file} has incorrect length: {len(chunk)}"
        assert (
            len(saved_data["chunks"][-1]) <= chunk_size
        ), f"Last chunk in {input_file} has incorrect length: {len(saved_data['chunks'][-1])}"

        # Clean up
        # os.remove(output_path)

    # Verify all files were processed
    # assert (
    #    len(os.listdir(config.tmp_dir)) == 0
    # ), "Not all temporary files were cleaned up"
