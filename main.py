from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel
from llm_pipeline import generate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rakshitai.info", "https://www.rakshitai.info"],  # Or specify: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define the request schema
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Rakshit ChatBot API is up!"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        # ✅ Append timestamp to log instead of overwriting
        with open("/root/rakshit_chatbot_backend/last_ping.txt", "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    except Exception as e:
        print("⚠️ Failed to write ping log:", e)
    response = generate_response(req.question)
    return {"answer": response}
