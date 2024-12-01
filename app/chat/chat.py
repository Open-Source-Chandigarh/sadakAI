import os
import sys
import time
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_groq import ChatGroq
from app.chat.config import config
from langchain_core.prompts import ChatPromptTemplate

logo = '''
███████╗ █████╗ ██████╗  █████╗ ██╗  ██╗ █████╗ ██╗
██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██║
███████╗███████║██║  ██║███████║█████╔╝ ███████║██║
╚════██║██╔══██║██║  ██║██╔══██║██╔═██╗ ██╔══██║██║
███████║██║  ██║██████╔╝██║  ██║██║  ██╗██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
'''

qdrant_client = QdrantClient(url=config.QDRANT_URL, api_key=config.QDRANT_API_KEY)
embeddings = FastEmbedEmbeddings()
vector_store = QdrantVectorStore(client=qdrant_client, collection_name=config.COLLECTION_NAME, embedding=embeddings)

def retrieve_info(query):
    """Retrieve similar documents from Qdrant"""
    similar_docs = vector_store.similarity_search(query, k=3)
    return [doc.page_content for doc in similar_docs]

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