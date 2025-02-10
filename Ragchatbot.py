from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="llama3.1",
)

vector_store = Chroma(
    persist_directory="./chroma_langchain_db",
    embedding_function=embeddings
)

retriever = vector_store.similarity_search_with_relevance_scores(
    query="adopter des programmes d’études et une nomenclature des grades, diplômes ou certificats universitaires",
    k=3
)

for doc in retriever:
    print(doc[0].metadata["source"], doc[1])

print("====" + retriever[2][0].page_content, retriever[2][1])