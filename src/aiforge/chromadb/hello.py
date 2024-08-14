import os
from pathlib import Path

from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAI, OpenAIEmbeddings

from aiforge.config import config


def load_documents(path):
    loader = DirectoryLoader(path, glob="*.txt", loader_cls=TextLoader)
    return loader.load()


def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_documents(documents)


def create_vectordb(texts, persist_directory):
    embedding = OpenAIEmbeddings()
    persist_directory_str = str(persist_directory)  # Convert PosixPath to string
    vectordb = Chroma.from_documents(
        documents=texts, embedding=embedding, persist_directory=persist_directory_str
    )
    vectordb.persist()
    return vectordb


def create_qa_chain(vectordb):
    retriever = vectordb.as_retriever(search_kwargs={"k": 2})
    return RetrievalQA.from_chain_type(
        llm=OpenAI(),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )


def process_query(qa_chain, query):
    llm_response = qa_chain(query)
    result = llm_response["result"]
    sources = [source.metadata["source"] for source in llm_response["source_documents"]]
    return result, sources
