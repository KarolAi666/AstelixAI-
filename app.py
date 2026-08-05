
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ASTELIX AI - Serwer Główny
© 2024 Karol Jaskólski - Wszelkie prawa zastrzeżone
📧 cocieto2580123@gmail.com
📞 +48 791 380 755
"""

import os
import json
import uuid
import asyncio
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Astelix AI"
APP_VERSION = "4.0.0"
AUTHOR = "Karol Jaskólski"
EMAIL = "cocieto2580123@gmail.com"
PHONE = "+48 791 380 755"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=APP_NAME, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str
    mode: str = "GENERAL"
    temperature: float = 0.7
    max_tokens: int = 1000

class ChatResponse(BaseModel):
    id: str
    response: str
    model: str
    confidence: float
    processing_time: float
    timestamp: datetime

class AIEngine:
    def __init__(self):
        self.models = {
            "GPT-4": {"available": True},
            "Claude 3": {"available": True},
            "Gemini Pro": {"available": True},
            "Llama 2": {"available": True},
            "Mistral": {"available": True}
        }
        
        self.responses = {
            "GENERAL": "🤖 Oto ogólna odpowiedź:\n\n",
            "CODING": "💻 Kod:\n\n```python\n",
            "ANALYSIS": "📊 Analiza:\n\n",
            "CREATION": "🎨 Kreatywna odpowiedź:\n\n",
            "REASONING": "🧠 Rozumowanie:\n\n",
            "MULTI_MODAL": "🌐 Multimodalna:\n\n"
        }
    
    async def process(self, query: str, mode: str, temperature: float, max_tokens: int) -> Dict:
        import random
        await asyncio.sleep(random.uniform(0.3, 0.8))
        model = random.choice(list(self.models.keys()))
        
        responses = {
            "GENERAL": f"{self.responses['GENERAL']}Odpowiedź na: '{query}'\nModel: {model}",
            "CODING": f"{self.responses['CODING']}# Kod dla: {query}\ndef solution():\n    return True\n```\nModel: {model}",
            "ANALYSIS": f"{self.responses['ANALYSIS']}Analiza: {query}\nWnioski: ...\nModel: {model}",
            "CREATION": f"{self.responses['CREATION']}Inspiracje: {query}\nPomysły: ...\nModel: {model}",
            "REASONING": f"{self.responses['REASONING']}Kroki: 1. ... 2. ...\nModel: {model}",
            "MULTI_MODAL": f"{self.responses['MULTI_MODAL']}Analiza multimodalna: {query}\nModel: {model}"
        }
        
        return {
            "response": responses.get(mode, responses["GENERAL"]),
            "model": model,
            "confidence": random.uniform(0.78, 0.97),
            "tokens_used": random.randint(100, max_tokens)
        }

ai_engine = AIEngine()

@app.get("/", response_class=HTMLResponse)
async def get_index():
    try:
        if os.path.exists("templates/index.html"):
            with open("templates/index.html", "r", encoding="utf-8") as f:
                return f.read()
        return HTMLResponse("""<h1>⭐ Astelix AI</h1><p>✅ Serwer działa!</p>""")
    except:
        return HTMLResponse("<h1>⭐ Astelix AI</h1><p>✅ Serwer działa!</p>")

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy", "system": APP_NAME, "version": APP_VERSION, "author": AUTHOR}

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    result = await ai_engine.process(request.query, request.mode, request.temperature, request.max_tokens)
    return ChatResponse(
        id=str(uuid.uuid4()),
        response=result["response"],
        model=result["model"],
        confidence=result["confidence"],
        processing_time=0.5,
        timestamp=datetime.utcnow()
    )

@app.get("/api/v1/models")
async def get_models():
    return {"system": APP_NAME, "models": list(ai_engine.models.keys())}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            request = json.loads(data)
            result = await ai_engine.process(
                request.get('query', ''),
                request.get('mode', 'GENERAL'),
                request.get('temperature', 0.7),
                request.get('max_tokens', 1000)
            )
            await websocket.send_text(json.dumps({"type": "start", "model": result["model"]}))
            for word in result["response"].split():
                await asyncio.sleep(0.02)
                await websocket.send_text(json.dumps({"type": "chunk", "data": word + " "}))
            await websocket.send_text(json.dumps({"type": "end"}))
    except:
        pass

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
