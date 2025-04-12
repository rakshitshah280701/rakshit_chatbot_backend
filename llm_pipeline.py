from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
import os

# Embedding model from Hugging Face
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def load_and_split_document(filepath):
    text = Path(filepath).read_text(encoding='utf-8')
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)
    return chunks

def embed_and_store(chunks, db_path="vectorstore/faiss_db"):
    if not os.path.exists(db_path):
        db = FAISS.from_texts(chunks, embedding_model)
        db.save_local(db_path)
        print("✅ Created and saved FAISS DB.")
    else:
        print("⚠️ FAISS DB already exists!")

def load_faiss_db(db_path="vectorstore/faiss_db"):
    return FAISS.load_local(db_path, embedding_model)

# Use this to create embeddings once
if __name__ == "__main__":
    chunks = load_and_split_document("data/rakshit_profile.txt")
    Path("vectorstore").mkdir(exist_ok=True)
    embed_and_store(chunks)
