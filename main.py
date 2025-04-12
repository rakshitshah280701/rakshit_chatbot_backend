from fastapi import FastAPI
from pydantic import BaseModel
from llm_pipeline import generate_response

app = FastAPI()

# Define the request schema
class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Rakshit ChatBot API is up!"}

@app.post("/chat")
def chat(req: ChatRequest):
    response = generate_response(req.question)
    return {"answer": response}
