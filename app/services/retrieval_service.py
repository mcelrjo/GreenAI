import openai
import os
import chromadb
from chromadb.config import Settings

# Initialize Chroma
client = chromadb.Client(Settings(persist_directory="./chroma_store"))
collection = client.get_or_create_collection("turf_docs")

openai.api_key = os.getenv("OPENAI_API_KEY")

def retrieve_relevant_context(query):
    query_embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")["data"][0]["embedding"]
    results = collection.query(query_embeddings=[query_embedding], n_results=3, include=["documents"])
    return "\n\n".join(results["documents"][0]) if results["documents"] else ""

def generate_response(user_question, context):
    prompt = f"Context:\n{context}\n\nUser Question:\n{user_question}\n\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
