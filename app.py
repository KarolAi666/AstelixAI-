    #!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn
import random
import uuid
from datetime import datetime

app = FastAPI(title="Astelix AI", version="4.0.0")

# ============ MODELE ============

class ChatRequest(BaseModel):
    query: str
    mode: str = "GENERAL"

class ChatResponse(BaseModel):
    id: str
    response: str
    model: str
    timestamp: datetime

# ============ SILNIK AI ============

class AIEngine:
    def __init__(self):
        self.models = ["GPT-4", "Claude 3", "Gemini Pro", "Llama 2", "Mistral"]
    
    def process(self, query: str, mode: str):
        model = random.choice(self.models)
        responses = {
            "GENERAL": f"🤖 Ogólna odpowiedź na: '{query}'\n\n📌 Użyty model: {model}",
            "CODING": f"💻 Kod dla: {query}\n```python\ndef solution():\n    return True\n```\n\n📌 Użyty model: {model}",
            "ANALYSIS": f"📊 Analiza: {query}\n\n📌 Użyty model: {model}",
            "CREATION": f"🎨 Inspiracje: {query}\n\n📌 Użyty model: {model}",
            "REASONING": f"🧠 Rozumowanie: {query}\n\n📌 Użyty model: {model}",
            "MULTI_MODAL": f"🌐 Analiza multimodalna: {query}\n\n📌 Użyty model: {model}"
        }
        return {
            "response": responses.get(mode, responses["GENERAL"]),
            "model": model
        }

ai_engine = AIEngine()

# ============ ENDPOINTY ============

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Astelix AI</title></head>
    <body style="background:#0f0a1a;color:white;font-family:system-ui;text-align:center;padding:40px;">
        <h1 style="font-size:3rem;background:linear-gradient(135deg,#7c3aed,#a78bfa);-webkit-background-clip:text;color:transparent;">⭐ Astelix AI</h1>
        <p style="color:#a78bfa;">✅ Serwer działa!</p>
        <p style="color:#94a3b8;">© 2024 Karol Jaskólski</p>
        <p style="color:#94a3b8;">📧 cocieto2580123@gmail.com</p>
    </body>
    </html>
    """

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "system": "Astelix AI", "version": "4.0.0"}

@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
    result = ai_engine.process(request.query, request.mode)
    return ChatResponse(
        id=str(uuid.uuid4()),
        response=result["response"],
        model=result["model"],
        timestamp=datetime.utcnow()
    )

@app.get("/api/v1/models")
async def get_models():
    return {"models": ai_engine.models}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
