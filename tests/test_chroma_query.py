import pytest
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from aiforge.config import config


@pytest.fixture(scope="module")
def existing_vectordb():
    # Path to the existing ChromaDB
    persist_directory = str(config.tmp_dir / "chromadb")

    # Create an embedding function
    embedding_function = OpenAIEmbeddings()

    # Load the existing Chroma database
    return Chroma(
        persist_directory=persist_directory, embedding_function=embedding_function
    )


def test_query_existing_db(existing_vectordb):
    # The specific query we want to test
    # query = "How much money did Microsoft raise?"
    query = "Tell me about Microsoft and money raised."

    # Perform a similarity search
    results = existing_vectordb.similarity_search(query, k=1)

    # Check if we got a result
    assert len(results) > 0, "No results returned from the database"

    # Check if the result contains the expected information
    assert (
        "$10 billion" in results[0].page_content
    ), "Expected answer not found in the result"

    # Print the result for verification
    print(f"Query: {query}")
    print(f"Result: {results[0].page_content}")

    # Optionally, you can check the similarity score
    results_with_scores = existing_vectordb.similarity_search_with_score(query, k=1)
    document, score = results_with_scores[0]
    print(f"Similarity score: {score}")
