import os
from pathlib import Path

import pytest

from aiforge.chromadb.hello import (
    create_qa_chain,
    create_vectordb,
    load_documents,
    process_query,
    split_text,
)
from aiforge.config import config


@pytest.fixture(scope="module")
def test_data_dir():
    return config.test_data_dir


@pytest.fixture(scope="module")
def test_db_dir():
    return config.tmp_dir / "chromadb"


@pytest.fixture(scope="module")
def sample_documents(test_data_dir):
    # Create a sample document for testing
    sample_text = "This is a sample document for testing. Microsoft raised $10 billion."
    sample_file = test_data_dir / "sample.txt"
    sample_file.write_text(sample_text)
    yield
    sample_file.unlink()  # Clean up after test


@pytest.fixture(scope="module")
def vectordb(sample_documents, test_data_dir, test_db_dir):
    documents = load_documents(test_data_dir)
    texts = split_text(documents)
    return create_vectordb(texts, test_db_dir)


@pytest.fixture(scope="module")
def qa_chain(vectordb):
    return create_qa_chain(vectordb)


def test_load_documents(test_data_dir):
    documents = load_documents(test_data_dir)
    assert len(documents) > 0


def test_split_text(test_data_dir):
    documents = load_documents(test_data_dir)
    texts = split_text(documents)
    assert len(texts) > 0


def test_create_vectordb(vectordb):
    assert vectordb is not None


def test_create_qa_chain(qa_chain):
    assert qa_chain is not None


def test_process_query(qa_chain):
    query = "How much money did Microsoft raise?"
    result, sources = process_query(qa_chain, query)
    assert result is not None
    assert len(sources) > 0
    assert "$10 billion" in result
