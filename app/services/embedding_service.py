import openai
import pdfplumber
import requests
from bs4 import BeautifulSoup
import chromadb
from chromadb.config import Settings

# Initialize Chroma
client = chromadb.Client(Settings(persist_directory="./chroma_store"))
collection = client.get_or_create_collection("turf_docs")

openai.api_key = "YOUR_OPENAI_API_KEY"

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text(separator='\n')

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def embed_and_store(text, source_id):
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        embedding = openai.Embedding.create(input=chunk, model="text-embedding-ada-002")["data"][0]["embedding"]
        collection.add(ids=[f"{source_id}_chunk_{i}"], embeddings=[embedding], documents=[chunk])
    client.persist()
