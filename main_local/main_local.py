import os
import pickle
import time
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain.chains import LLMChain

logo = '''
███████╗ █████╗ ██████╗  █████╗ ██╗  ██╗ █████╗ ██╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██║
███████╗███████║██║  ██║███████║█████╔╝ ███████║██║
╚════██║██╔══██║██║  ██║██╔══██║██╔═██╗ ██╔══██║██║
███████║██║  ██║██████╔╝██║  ██║██║  ██╗██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
                                                   '''

file_path = "main_local/data/data.csv"
documents_cache_path = "main_local/.cache/documents_cache.pkl"

print(f"Current working directory: {os.getcwd()}")
print(f"Absolute path of the file: {os.path.abspath(file_path)}")

if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file {file_path} does not exist.")

try:
    print("Loading CSV file...")
    loader = CSVLoader(file_path=file_path)
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

print("Creating embeddings and FAISS index...")
embeddings = OllamaEmbeddings(model="llama3.2")
db = FAISS.from_documents(documents, embeddings)
print("Embeddings and FAISS index created successfully.")

def retrieve_info(query):
    similar_response = db.similarity_search(query, k=3)
    page_contents_array = [doc.page_content for doc in similar_response]
    return page_contents_array

print("Setting up LLMChain and prompts...")
llm = ChatOllama(temperature=0, model="llama3.2")

template = """
You are a world-class technical advisor. 
I will share a developer's question with you, and you will give me the best advice that 
I should provide to this developer based on past best practices, 
and you will follow ALL of the rules below:

1/ Advice should be very similar or even identical to the past best practices, 
in terms of length, tone of voice, logical arguments, and other details.

2/ If the best practices are irrelevant, then try to mimic the style of the best practice to the developer's question.

Below is a question I received from the developer:
{message}

Here is a list of best practices of how we normally respond to developers in similar scenarios:
{best_practice}

Please write the best advice that I should provide to this developer:
"""

prompt = PromptTemplate(
    input_variables=["message", "best_practice"],
    template=template
)

chain = prompt | llm
print("LLMChain and prompts set up successfully.")

def generate_response(message):
    best_practice = retrieve_info(message)
    response = chain.invoke({"message": message, "best_practice": best_practice})
    content = tuple(response)[0][1]
    return content

def type_out_text(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.01)
    print()


def main():
    # print(logo)
    while True:
        message = input("\nEnter your question (type /exit to quit): ")
        if message.lower() == "/exit":
            break
        result = generate_response(message)
        print("\n>>")
        type_out_text(result)

if __name__ == '__main__':
    main()