import os

# import boto3
# import json, re

import chromadb
# import requests
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter

from langchain_community.document_loaders import JSONLoader
from langchain.schema import Document
from langchain_ollama import OllamaEmbeddings
# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["source"] = record.get("url")

    return metadata

# Charger le fichier JSON
file_path = "UQACmanage_data.json"

# Définir le schéma JQ pour extraire les données nécessaires
jq_schema = ".[]" 

loader = JSONLoader(
    file_path=file_path,
    jq_schema=jq_schema,
    content_key='text',
    metadata_func=metadata_func)

data = loader.load()

data = data[:5]
print(len(data))

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
chunked_documents = text_splitter.split_documents(data)

embeddings = OllamaEmbeddings(
    model="llama3.1",
)

client = chromadb.Client()

if client.list_collections():
    consent_collection = client.create_collection("consent_collection")
else:
    print("Collection already exists")
vectordb = Chroma.from_documents(
    documents=chunked_documents,
    embedding=embeddings,
    persist_directory="./chroma_langchain_db"
)