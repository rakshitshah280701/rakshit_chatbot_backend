import os
import re
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.docstore.document import Document

# --- Config ---
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_file = "data/rakshit_profile.txt"
db_path = "vectorstore/faiss_db"
index_file = os.path.join(db_path, "index.faiss")

# --- Load full file ---
text = Path(text_file).read_text(encoding="utf-8")

# --- Extract the Project Portfolio section only ---
match = re.search(r"Project Portfolio \(In-Depth\)(.*?)(?:Publications|Future Goals|$)", text, re.DOTALL)
if not match:
    raise ValueError("🚨 Couldn't find the 'Project Portfolio (In-Depth)' section.")

project_section = match.group(1)

# --- Now extract numbered projects from that section ---
project_pattern = re.findall(r"\n\d+\.\s+(.*?)\n(.*?)(?=\n\d+\.|\Z)", project_section, re.DOTALL)

documents = []
splitter = RecursiveCharacterTextSplitter(chunk_size=450, chunk_overlap=50)

for title, body in project_pattern:
    clean_title = title.strip()
    chunks = splitter.split_text(body.strip())
    for chunk in chunks:
        documents.append(Document(page_content=chunk, metadata={"project": clean_title}))

if not documents:
    raise ValueError("🚨 No documents were created. Please check your splitting logic.")

# --- Build or Load FAISS ---
if not os.path.exists(index_file):
    print("⚠️ FAISS index not found. Creating it...")
    Path(db_path).mkdir(parents=True, exist_ok=True)
    db = FAISS.from_documents(documents, embedding_model)
    db.save_local(db_path)
    print("✅ FAISS index created and saved.")
else:
    print("✅ FAISS index found. Loading...")
    db = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)

# --- Hybrid Retrieval ---
bm25_retriever = BM25Retriever.from_texts([doc.page_content for doc in documents])
bm25_retriever.k = 5
faiss_retriever = db.as_retriever(search_kwargs={"k": 5})

hybrid = EnsembleRetriever(
    retrievers=[faiss_retriever, bm25_retriever],
    weights=[0.7, 0.3]
)

# --- CLI Test ---
query = input("🔍 Enter your test query: ")
docs = hybrid.invoke(query)

print("\n✅ Retrieved Chunks from Hybrid Retriever (FAISS + BM25):\n")
for i, doc in enumerate(docs):
    print(f"--- Chunk {i + 1} ---\n{doc.page_content}")
    if doc.metadata:
        print("📌 Metadata:", doc.metadata)
    print("----------------------\n")
