from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from llm_pipeline import generate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rakshit-portfolio-alpha.vercel.app"],  # Or specify: ["http://localhost:3000"]
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
    response = generate_response(req.question)
    return {"answer": response}
