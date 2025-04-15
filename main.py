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
# def chat(req: ChatRequest):
#     try:
#         # ✅ Append timestamp to log instead of overwriting
#         with open("/root/rakshit_chatbot_backend/last_ping.txt", "a") as f:
#             f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
#     except Exception as e:
#         print("⚠️ Failed to write ping log:", e)
#     response = generate_response(req.question)
#     return {"answer": response}

def chat(req: ChatRequest):
    try:
        # ✅ Append timestamp to last_ping.txt
        with open("/root/rakshit_chatbot_backend/last_ping.txt", "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    except Exception as e:
        print("⚠️ Failed to write ping log:", e)

    question = req.question
    answer = generate_response(question)

    # ✅ Log to local file (optional)
    try:
        with open("/root/chat_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} | Q: {question} | A: {answer}\n")
    except Exception as e:
        print("⚠️ Failed to write chat log:", e)

    # ✅ Send to Slack
    slack_webhook = os.getenv("SLACK_WEBHOOK_CHAT")
    if slack_webhook:
        slack_payload = {
            "text": f"""🤖 *New Chat Interaction*

🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
❓ *Q:* {question}
✅ *A:* {answer[:1000]}{'...' if len(answer) > 1000 else ''}"""
        }
        try:
            requests.post(slack_webhook, json=slack_payload)
        except Exception as e:
            print(f"❌ Slack webhook failed: {e}")

    return {"answer": answer}

@app.get("/ping")
def ping():
    try:
        with open("/root/rakshit_chatbot_backend/last_ping.txt", "a") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
    except Exception as e:
        print("❌ Failed to write ping:", e)
    return {"status": "pong"}
