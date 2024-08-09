import pytest

from aiforge.utils.file_utils import get_project_root
from aiforge.utils.web_scraper import fetch_wikipedia_pages, save_wikipedia_pages

# from paz.utils.file_utils import get_project_root
# from paz.utils.web_scraper import fetch_wikipedia_pages, save_wikipedia_pages


@pytest.fixture
def wikipedia_urls():
    return [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://en.wikipedia.org/wiki/Asynchronous_I/O",
    ]


@pytest.fixture
def project_root():
    return get_project_root()


@pytest.fixture
def output_files(project_root):
    return {
        "tmp": project_root / "tmp" / "test_tmp.txt",
        "persistent": project_root / "data" / "test_persistent.txt",
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


# @pytest.fixture(autouse=True)
# def cleanup(output_files):
#    yield
# Clean up files after tests
#    for file_path in output_files.values():
#        if file_path.exists():
#            file_path.unlink()
