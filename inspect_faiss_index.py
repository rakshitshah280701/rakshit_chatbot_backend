from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path
import os

# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# FAISS DB setup
db_path = "vectorstore/faiss_db"
index_file = os.path.join(db_path, "index.faiss")
text_file = "data/rakshit_profile1.txt"

# Build FAISS index if not found
if not os.path.exists(index_file):
    print("⚠️ FAISS index not found. Creating it...")
    text = Path(text_file).read_text(encoding='utf-8')
    splitter = RecursiveCharacterTextSplitter(chunk_size=575, chunk_overlap=100)
    chunks = splitter.split_text(text)
    Path("vectorstore").mkdir(exist_ok=True)
    db = FAISS.from_texts(chunks, embedding_model)
    db.save_local(db_path)
    print("✅ FAISS index created and saved.")
else:
    print("✅ FAISS index found. Loading...")
    db = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)

retriever = db.as_retriever()

# Prompt user for query
query = input("🔍 Enter your question: ")

# New approach: invoke method
docs = retriever.invoke(query)

# Print results
print("\n✅ Retrieved Chunks from FAISS:\n")
for i, doc in enumerate(docs):
    print(f"--- Chunk {i + 1} ---\n{doc.page_content}\n----------------------\n")
