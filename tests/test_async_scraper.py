import os
from pathlib import Path

import pytest

from aiforge.config import config
from aiforge.lab.async_scraper import fetch_wikipedia_pages, save_wikipedia_pages


@pytest.fixture
def wikipedia_urls():
    return [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://en.wikipedia.org/wiki/Asynchronous_I/O",
    ]


@pytest.fixture
def output_files():
    return {
        "tmp": config.tmp_dir / "test_tmp.txt",
        "persistent": config.data_dir / "test_persistent.txt",
    }


@pytest.mark.asyncio
async def test_fetch_save_and_validate_wikipedia_pages(wikipedia_urls, output_files):
    # Fetch the content
    fetched_content = await fetch_wikipedia_pages(wikipedia_urls)

    # Save the content
    save_wikipedia_pages(
        fetched_content,
        output_files["tmp"].name,
        persistent=False,
    )
    save_wikipedia_pages(
        fetched_content,
        output_files["persistent"].name,
        persistent=True,
    )

    # Validate saved content
    for file_path in output_files.values():
        assert file_path.exists(), f"File not found at {file_path}"

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check for expected content
        assert "Python" in content, f"'Python' not in {file_path}"
        assert (
            "programming language" in content.lower()
        ), f"'programming language' not in {file_path}"
        assert "asynchronous" in content.lower(), f"'asynchronous' not in {file_path}"


@pytest.fixture(autouse=True)
def cleanup(output_files):
    yield
    # Clean up files after tests only if KEEP_TEST_FILES is not set
    if os.environ.get("KEEP_TEST_FILES", "").lower() != "true":
        for file_path in output_files.values():
            if file_path.exists():
                file_path.unlink()
    else:
        print("\nTest files were not deleted. You can find them at:")
        for key, file_path in output_files.items():
            if file_path.exists():
                print(f"- {key}: {file_path}")
