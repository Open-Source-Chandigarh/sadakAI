import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from config import config

def create_collection_if_not_exists(client):
    collections = client.get_collections().collections
    if config.COLLECTION_NAME not in [col.name for col in collections]:
        client.create_collection(
            collection_name=config.COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.DOT)
        )
        print(f"Collection `{config.COLLECTION_NAME}` created successfully.")
    else:
        print(f"Collection `{config.COLLECTION_NAME}` already exists.")

def process_csv(file_path, client, embeddings):
    try:
        print("Loading CSV file...")
        loader = CSVLoader(file_path=file_path, encoding="utf-8")
        documents = loader.load()
        print("CSV file loaded successfully.")
        
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        vector_store = QdrantVectorStore.from_texts(
            texts=texts,
            embedding=embeddings,
            metadatas=metadatas,
            collection_name=config.COLLECTION_NAME,
            url=config.QDRANT_URL,
            api_key=config.QDRANT_API_KEY,
            force_recreate=True
        )
        print(f"CSV file {file_path} ingested successfully.")
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

def ingest():
    client = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)
    create_collection_if_not_exists(client)

    embeddings = FastEmbedEmbeddings()

    file_path = "app/chat/data/data.csv"
    process_csv(file_path, client, embeddings)

if __name__ == "__main__":
    ingest()
