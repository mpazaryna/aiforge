"""
Asynchronous Wikipedia Scraper

This module implements an asynchronous scraper for fetching content from multiple Wikipedia pages
simultaneously. It demonstrates the use of asynchronous programming in Python to efficiently
retrieve data from web pages concurrently.

Key Features:
- Asynchronous HTTP requests using aiohttp
- Concurrent execution of multiple requests
- File I/O operations for saving scraped content

The script uses Python's asyncio library for managing asynchronous operations. It leverages
the aiohttp library for making non-blocking HTTP requests, which allows for efficient
handling of multiple requests concurrently.

Asynchronous Programming Concepts Used:
1. Coroutines (async/await): Used to define asynchronous functions.
2. AsyncIO Event Loop: Manages the execution of coroutines.
3. Asynchronous Context Managers: Used with aiohttp.ClientSession for efficient connection management.
4. Task Gathering: asyncio.gather() is used to run multiple coroutines concurrently and wait for all of them to complete.

Usage:
    Run this script directly to fetch and save content from predefined Wikipedia pages.
    python -m src.paz.lab.async_scraper

    Or import and use the functions in other scripts for custom scraping tasks.
"""

# Standard library imports for asynchronous operations and file path handling
import asyncio
from pathlib import Path
from typing import List, Tuple

# Third-party library for asynchronous HTTP requests
import aiohttp

from aiforge.config import config

# Custom utility functions for file operations and configuration
from aiforge.utils.file_utils import write_to_file


async def fetch_wikipedia_pages(urls: List[str]) -> List[Tuple[str, str]]:
    """
    Asynchronously fetch content from multiple Wikipedia pages.

    This function creates a single aiohttp session and uses it to fetch multiple URLs concurrently.
    It demonstrates the efficient use of asyncio for I/O-bound operations.

    Args:
        urls (List[str]): A list of Wikipedia URLs to fetch.

    Returns:
        List[Tuple[str, str]]: A list of tuples containing (url, html_content) for each fetched page.
    """

    async def fetch_url(session: aiohttp.ClientSession, url: str) -> Tuple[str, str]:
        """
        Asynchronously fetch content from a single URL.

        This nested function encapsulates the logic for a single HTTP GET request.
        It's defined here to share the session object efficiently.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            url (str): The URL to fetch.

        Returns:
            Tuple[str, str]: A tuple containing the URL and its HTML content.
        """
        async with session.get(url) as response:
            html_content = await response.text()
            return url, html_content

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    return results


def save_wikipedia_pages(
    content: List[Tuple[str, str]],
    output_filename: str,
    persistent: bool = False,
) -> Path:
    """
    Save fetched Wikipedia pages to a file.

    Args:
        content (List[Tuple[str, str]]): A list of tuples containing (url, html_content) for each page.
        output_filename (str): The name of the file to save the content.
        persistent (bool): If True, save to data folder; if False, save to tmp folder.

    Returns:
        Path: The path to the saved file.
    """
    output_dir = config.data_dir if persistent else config.tmp_dir
    output_file_path = output_dir / output_filename
    write_to_file(content, output_file_path)
    print(f"Content saved to {output_file_path}")
    return output_file_path


async def main():
    """
    Main asynchronous function to orchestrate the scraping process.

    This function demonstrates the high-level flow of the scraping process:
    1. Define URLs to scrape
    2. Fetch content asynchronously
    3. Save the fetched content to files
    """
    urls = [
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://en.wikipedia.org/wiki/Asynchronous_I/O",
    ]

    fetched_content = await fetch_wikipedia_pages(urls)

    save_wikipedia_pages(fetched_content, "wikipedia_content_tmp.txt", persistent=False)
    save_wikipedia_pages(
        fetched_content, "wikipedia_content_persistent.txt", persistent=True
    )


if __name__ == "__main__":
    asyncio.run(main())
