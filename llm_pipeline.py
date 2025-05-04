# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.llms import Ollama
# from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.chains import RetrievalQA
# from pathlib import Path
# import os

# # Load embedding model
# embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# # Load vector database
# db_path = "vectorstore/faiss_db"
# retriever = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True).as_retriever()

# # Load the Ollama LLM (e.g., phi)
# llm = Ollama(model="gemma3:1b")

# # LangChain RetrievalQA chaingit 
# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     chain_type="stuff"
# )

# # Main function that FastAPI calls
# def generate_response(user_question: str) -> str:
#     try:
#         # Step 1: Manually retrieve top 3 most relevant chunks
#         docs = retriever.get_relevant_documents(user_question)

#         print("\n🔍 Retrieved Chunks from FAISS:")
#         for i, doc in enumerate(docs):
#             print(f"\n--- Chunk {i+1} ---")
#             print(doc.page_content)

#         # Step 2: Concatenate retrieved chunks into context
#         context = "\n\n".join([doc.page_content for doc in docs])

#         # Step 3: Create full prompt manually
#         prompt = f"""
#         You are Rakshit's intelligent assistant. Use the context below to answer the user's question.

#         Context:
#         {context}

#         Question: {user_question}

#         Answer:
#         """

#         # Step 4: Run inference using Gemma 3
#         response = llm.invoke(prompt)

#         print("\n🧠 Final LLM Response:\n", response)
#         return response

#     except Exception as e:
#         return f"❌ Error during response generation: {str(e)}"



# # This is optional and for testing chunking + DB creation manually
# def load_and_split_document(filepath):
#     text = Path(filepath).read_text(encoding='utf-8')
#     splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
#     chunks = splitter.split_text(text)
#     return chunks

# def embed_and_store(chunks, db_path="vectorstore/faiss_db"):
#     if not os.path.exists(db_path):
#         db = FAISS.from_texts(chunks, embedding_model)
#         db.save_local(db_path)
#         print("✅ Created and saved FAISS DB.")
#     else:
#         print("⚠️ FAISS DB already exists!")

# if __name__ == "__main__":
#     chunks = load_and_split_document("data/rakshit_profile.txt")
#     Path("vectorstore").mkdir(exist_ok=True)
#     embed_and_store(chunks)


from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.chains import RetrievalQA
from pathlib import Path
import os

# Load embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Define vector database path
db_path = "vectorstore/faiss_db"
index_file = os.path.join(db_path, "index.faiss")

# Check if FAISS index exists, otherwise create it
if not os.path.exists(index_file):
    print("⚠️ FAISS index not found. Building from 'data/rakshit_profile.txt'...")
    text = Path("data/rakshit_profile.txt").read_text(encoding='utf-8')
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)

    Path("vectorstore").mkdir(exist_ok=True)
    db = FAISS.from_texts(chunks, embedding_model)
    db.save_local(db_path)
    print("✅ Created and saved FAISS DB.")
else:
    print("✅ FAISS index found. Loading...")
    db = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)

# Create retriever
retriever = db.as_retriever()

# Load Ollama LLM
llm = Ollama(model="gemma3:1b")

# LangChain QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

# Main function that FastAPI or CLI can use
def generate_response(user_question: str) -> str:
    try:
        # Step 1: Retrieve top relevant chunks
        docs = retriever.get_relevant_documents(user_question)

        print("\n🔍 Retrieved Chunks from FAISS:")
        for i, doc in enumerate(docs):
            print(f"\n--- Chunk {i+1} ---")
            print(doc.page_content)

        # Step 2: Concatenate chunks into prompt context
        context = "\n\n".join([doc.page_content for doc in docs])

        # Step 3: Format prompt
        prompt = f"""
        You are Rakshit's intelligent assistant. Use the context below to answer the user's question.

        Context:
        {context}

        Question: {user_question}

        Answer:
        """

        # Step 4: Get response from LLM
        response = llm.invoke(prompt)
        print("\n🧠 Final LLM Response:\n", response)
        return response

    except Exception as e:
        return f"❌ Error during response generation: {str(e)}"

# Optional CLI runner to regenerate index manually
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

if __name__ == "__main__":
    print("✅ Script loaded successfully. Ready to answer questions.")
