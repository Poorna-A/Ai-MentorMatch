import json
import uuid
import os
from dotenv import load_dotenv

# import chromadb
# from langchain.embeddings import OpenAIEmbeddings
# load_dotenv()


# # Initialize ChromaDB (Persistent storage)
# chroma_client = chromadb.PersistentClient(path="./chroma_db")
# collection = chroma_client.get_or_create_collection(name="resumes")

# # Initialize OpenAI embedding model
# embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# def generate_embedding(text):
#     """Generate embeddings for a given text"""
#     return embedding_model.embed_query(text)

# def store_resume(user_id, resume_json):
#     """Store resume in ChromaDB"""
#     resume_text = resume_json.get("resume_text", "")

#     if not resume_text:
#         print("No resume text found!")
#         return

#     # Generate embedding
#     embedding = generate_embedding(resume_text)

#     # Store in ChromaDB
#     collection.add(
#         ids=[str(uuid.uuid4())],  
#         embeddings=[embedding],
#         metadatas=[{"user_id": user_id, "resume": resume_json}]
#     )
#     print(f"Resume stored successfully for {user_id}")

# def retrieve_similar_resumes(query_text, top_k=3):
#     """Retrieve similar resumes"""
#     query_embedding = generate_embedding(query_text)
#     results = collection.query(
#         query_embeddings=[query_embedding],
#         n_results=top_k
#     )

#     return results["metadatas"][0] if results["metadatas"] else []


def store_data(user_data, filename="user_data.json"):
    """Saves extracted user details to a JSON file."""
    with open(filename, "w") as file:
        json.dump(user_data, file, indent=4)
    print("\n✅ Details saved successfully!")