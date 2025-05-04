from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- Config ---
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
db_path = "vectorstore/faiss_db"

# --- Load FAISS ---
print("✅ Loading FAISS index from local path...")
db = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)

# --- Use FAISS-only Retriever ---
retriever = db.as_retriever(search_kwargs={"k": 5})

# --- CLI Query ---
query = input("🔍 Enter your test query: ")
docs = retriever.invoke(query)

# --- Display Retrieved Chunks ---
print("\n✅ Retrieved Chunks from FAISS:\n")
for i, doc in enumerate(docs):
    print(f"--- Chunk {i + 1} ---\n{doc.page_content}")
    if doc.metadata:
        print("📌 Metadata:", doc.metadata)
    print("----------------------\n")
