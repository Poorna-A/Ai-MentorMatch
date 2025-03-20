from dotenv import load_dotenv
from openai import AzureOpenAI
import os


load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_ENDPOINT_EUS"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY_EUS"),
    api_version="2024-02-15-preview"
)