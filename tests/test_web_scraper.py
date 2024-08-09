from pathlib import Path

import pytest

from aiforge.config import AiForgeConfig
from aiforge.utils.web_scraper import fetch_wikipedia_pages, save_wikipedia_pages


@pytest.fixture
def wikipedia_urls():
    return [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://en.wikipedia.org/wiki/Asynchronous_I/O",
    ]


@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    # Set up test environment variables
    test_root = Path.cwd() / "test_root"
    monkeypatch.setenv("AIFORGE_PROJECT_ROOT", str(test_root))
    monkeypatch.setenv("AIFORGE_DATA_DIR", str(test_root / "test_data"))
    monkeypatch.setenv("AIFORGE_TMP_DIR", str(test_root / "test_tmp"))

    # Create a new config instance for each test
    test_config = AiForgeConfig()

    # Create test directories
    test_config.data_dir.mkdir(parents=True, exist_ok=True)
    test_config.tmp_dir.mkdir(parents=True, exist_ok=True)

    # Set the config for web_scraper
    import aiforge.utils.web_scraper

    monkeypatch.setattr(aiforge.utils.web_scraper, "config", test_config)

    yield test_config

    # Clean up
    import shutil

    shutil.rmtree(test_root)


@pytest.fixture
def output_files(setup_test_environment):
    return {
        "tmp": setup_test_environment.tmp_dir / "test_tmp.txt",
        "persistent": setup_test_environment.data_dir / "test_persistent.txt",
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


# Cleanup is handled by the setup_test_environment fixture
