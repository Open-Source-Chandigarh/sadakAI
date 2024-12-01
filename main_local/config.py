import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_NAME = "llama3-70b-8192"
    DEBUG = os.getenv("DEBUG", "False").lower() in ['true', '1', 't']
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

config = Config()