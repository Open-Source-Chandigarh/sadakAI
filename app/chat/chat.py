import os
import sys
import pickle
import faiss
import time
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_groq import ChatGroq
from chat.config import config
from langchain_core.prompts import ChatPromptTemplate

logo = '''
███████╗ █████╗ ██████╗  █████╗ ██╗  ██╗ █████╗ ██╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██║
███████╗███████║██║  ██║███████║█████╔╝ ███████║██║
╚════██║██╔══██║██║  ██║██╔══██║██╔═██╗ ██╔══██║██║
███████║██║  ██║██████╔╝██║  ██║██║  ██╗██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
'''

file_path = "chat/data/data.csv"
documents_cache_path = "chat/.cache/documents_cache.pkl"
vector_store_path = "chat/.cache/vector_store.index"

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

try:
    print("Loading CSV file...")
    loader = CSVLoader(file_path=file_path, encoding="utf-8")
    documents = loader.load()
    print("CSV file loaded successfully.")
except Exception as e:
    raise RuntimeError(f"Error loading {file_path}: {e}")

if os.path.exists(documents_cache_path):
    print("Loading cached documents...")
    with open(documents_cache_path, 'rb') as f:
        documents = pickle.load(f)
    print("Cached documents loaded successfully.")
else:
    print("Saving documents to cache...")
    with open(documents_cache_path, 'wb') as f:
        pickle.dump(documents, f)
    print("Documents saved to cache successfully.")

model = SentenceTransformer('all-MiniLM-L6-v2')
if os.path.exists(vector_store_path):
    print("Loading FAISS index from cache...")
    index = faiss.read_index(vector_store_path)
    print("FAISS index loaded successfully.")
else:
    print("Creating embeddings and FAISS index...")
    embeddings = model.encode([doc.page_content for doc in documents])
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, vector_store_path)
    print("Embeddings and FAISS index created and saved to cache successfully.")

def retrieve_info(query):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k=3)
    page_contents_array = [documents[idx].page_content for idx in indices[0]]
    return page_contents_array

llm = ChatGroq(
    api_key=config.GROQ_API_KEY,  
    model=config.MODEL_NAME,
    temperature=0.5,
    max_tokens=500,
    max_retries=2,
)

# Define the custom prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a world-class technical advisor. I will share a developer's question with you, and you will give me the best advice that I should provide to this developer based on past best practices, and you will follow ALL of the rules below:

        1/ Advice should be very similar or even identical to the past best practices, 
        in terms of length, tone of voice, logical arguments, and other details.

        2/ If the best practices are irrelevant, then try to mimic the style of the best practice to the developer's question.

        3/ If the developer asks for a roadmap, provide a detailed roadmap according to what the developer asked.

        4/ If the developer asks how to learn a specific technology, give a detailed step-by-step process to learn the technology.

        5/ If the developer asks for sources to learn a specific technology, just provide the sources.

        Below is a question I received from the developer:
        {message}

        Here is a list of best practices of how we normally respond to developers in similar scenarios:
        {best_practice}

        Please write the best advice that I should provide to this developer:
        return the message in markdown format
        """
    ),
    ("human", "{message}"),
])

def generate_response(message):
    try:
        best_practice = retrieve_info(message)
        response = prompt | llm
        ai_response = response.invoke({
            "message": message,
            "best_practice": "\n".join(best_practice),
        })
        content = tuple(ai_response)[0][1]
        return content
    except Exception as e:
        return "Error processing the request."

def retrieve_info(query):
    query_embedding = model.encode([query])
    distances, indices = index.search(query_embedding, k=3)
    page_contents_array = [documents[idx].page_content for idx in indices[0]]
    return page_contents_array

def type_out_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.01)  
    print()

def main():
    sys.stdout.buffer.write(logo.encode('utf-8'))
    while True:
        message = input("\nEnter your question (type /exit to quit): ")
        if message.lower() == "/exit":
            break
        result = generate_response(message)
        print("\n>>")
        type_out_text(result)

if __name__ == '__main__':
    main()
