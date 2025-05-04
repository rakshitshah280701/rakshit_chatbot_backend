from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel
from llm_pipeline import generate_response
import os
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rakshitai.info", "https://www.rakshitai.info"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"message": "Rakshit ChatBot API is up!"}

@app.post("/chat")
def chat(req: ChatRequest):
    Path("/root/.activity").touch()  # ✅ Only here!
    question = req.question
    answer = generate_response(question)

    try:
        with open("/root/chat_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} | Q: {question} | A: {answer}\n")
    except Exception as e:
        print("⚠️ Failed to write chat log:", e)

    slack_webhook = os.getenv("SLACK_WEBHOOK_CHAT")
    if slack_webhook:
        slack_payload = {
            "text": f"""🤖 *New Chat Interaction*\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n❓ *Q:* {question}\n✅ *A:* {answer[:1000]}{'...' if len(answer) > 1000 else ''}"""
        }
        try:
            requests.post(slack_webhook, json=slack_payload)
        except Exception as e:
            print(f"❌ Slack webhook failed: {e}")

    return {"answer": answer}

@app.get("/ping")
def ping():
    return {"status": "pong"}

# Optional endpoint if needed, does not touch .activity anymore
@app.post("/keepalive")
def keepalive():
    return {"status": "ok"}
