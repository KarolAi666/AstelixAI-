astelix-ai/
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
├── LICENSE
├── render.yaml
├── templates/
│   └── index.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── icons/
│       └── favicon.ico
└── data/
    └── .gitkeep#!/usr/bin/env python3
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
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# ============ KONFIGURACJA ============
load_dotenv()

APP_NAME = "Astelix AI"
APP_VERSION = "4.0.0"
AUTHOR = "Karol Jaskólski"
EMAIL = "cocieto2580123@gmail.com"
PHONE = "+48 791 380 755"

# Logowanie
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============ FASTAPI APP ============
app = FastAPI(
    title=APP_NAME,
    description="Zaawansowany system AI łączący wszystkie modele",
    version=APP_VERSION
)

# CORS - ważne dla dostępu z telefonu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ MODELE DANYCH ============
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

# ============ SILNIK AI ============
class AIEngine:
    """Silnik AI - symulacja odpowiedzi"""
    
    def __init__(self):
        self.models = {
            "GPT-4": {
                "available": True,
                "capabilities": ["text", "code", "analysis", "reasoning"],
                "description": "Zaawansowany model OpenAI"
            },
            "Claude 3": {
                "available": True,
                "capabilities": ["text", "reasoning", "safety", "analysis"],
                "description": "Model Anthropic - bezpieczny i etyczny"
            },
            "Gemini Pro": {
                "available": True,
                "capabilities": ["text", "multi_modal", "reasoning"],
                "description": "Model Google - wielomodalny"
            },
            "Llama 2": {
                "available": True,
                "capabilities": ["text", "reasoning", "translation"],
                "description": "Open-source model Meta"
            },
            "Mistral": {
                "available": True,
                "capabilities": ["text", "code", "reasoning"],
                "description": "Szybki i wydajny model francuski"
            }
        }
        
        self.responses = {
            "GENERAL": "🤖 Oto ogólna odpowiedź na Twoje pytanie:\n\n",
            "CODING": "💻 Oto kod, który Ci pomoże:\n\n```python\n",
            "ANALYSIS": "📊 Analiza danych:\n\n",
            "CREATION": "🎨 Kreatywna odpowiedź:\n\n",
            "REASONING": "🧠 Rozumowanie krok po kroku:\n\n",
            "MULTI_MODAL": "🌐 Odpowiedź multimodalna:\n\n"
        }
    
    async def process(self, query: str, mode: str, temperature: float, max_tokens: int) -> Dict:
        """Przetwarzanie zapytania"""
        
        import random
        
        # Symulacja czasu przetwarzania
        await asyncio.sleep(random.uniform(0.3, 0.8))
        
        # Wybierz model
        model = random.choice(list(self.models.keys()))
        
        # Generuj odpowiedź
        base_response = self.responses.get(mode, self.responses["GENERAL"])
        
        # Różne odpowiedzi w zależności od trybu
        responses = {
            "GENERAL": f"""{base_response}To jest ogólna odpowiedź na: '{query}'

📌 **Szczegóły:**
- Użyty model: {model}
- Temperatura: {temperature}
- Maksymalna liczba tokenów: {max_tokens}
- Status: ✅ Sukces

💡 **Wskazówka:** Możesz zmienić tryb na Kod, Analizę lub Kreatywność dla lepszych rezultatów.""",

            "CODING": f"""{base_response}# Rozwiązanie dla: {query}

def solve_problem():
    \"\"\"
    Rozwiązanie problemu wygenerowane przez Astelix AI
    \"\"\"
    print("Astelix AI - Kod wygenerowany pomyślnie!")
    
    # Logika rozwiązania
    result = True
    
    return result

# Przykład użycia:
if __name__ == "__main__":
    result = solve_problem()
    print(f"Wynik: {result}")

📌 **Użyty model:** {model}
⚡ **Język:** Python
✅ **Status:** Kod gotowy do użycia""",

            "ANALYSIS": f"""{base_response}📈 **Analiza dla:** '{query}'

🔍 **Kluczowe wnioski:**
1. Pierwszy wniosek dotyczący analizy
2. Drugi wniosek z danych
3. Trzeci wniosek - rekomendacja

📊 **Dane statystyczne:**
- Współczynnik A: 85%
- Współczynnik B: 72%
- Współczynnik C: 91%

💡 **Rekomendacje:**
• Rekomendacja 1 - działaj natychmiast
• Rekomendacja 2 - zaplanuj na przyszłość
• Rekomendacja 3 - monitoruj postępy

📌 **Użyty model:** {model}""",

            "CREATION": f"""{base_response}✨ **Inspiracje dla:** '{query}'

🎯 **Pomysł 1:** Innowacyjne podejście do tematu
🎯 **Pomysł 2:** Kreatywna interpretacja
🎯 **Pomysł 3:** Nieszablonowe rozwiązanie

🎨 **Wizja artystyczna:**
Wyobraź sobie połączenie nowoczesności z tradycją...
 
📝 **Propozycja treści:**
[Twoja kreatywna treść tutaj]

📌 **Użyty model:** {model}
✨ **Poziom kreatywności:** Wysoki""",

            "REASONING": f"""{base_response}🧩 **Rozumowanie dla:** '{query}'

**Krok 1:** Analiza problemu
- Identyfikacja kluczowych elementów
- Określenie celów

**Krok 2:** Zbieranie informacji
- Wyszukiwanie danych
- Weryfikacja źródeł

**Krok 3:** Synteza rozwiązań
- Łączenie informacji
- Tworzenie wniosków

**Krok 4:** Weryfikacja
- Sprawdzenie poprawności
- Testowanie hipotez

💡 **Wniosek końcowy:** [Tu pojawi się rozwiązanie]

📌 **Użyty model:** {model}
🧠 **Poziom złożoności:** Zaawansowany""",

            "MULTI_MODAL": f"""{base_response}🌐 **Odpowiedź multimodalna dla:** '{query}'

🖼️ **Analiza wizualna:**
- Wykryto wzorce wizualne
- Kolorystyka: [opis]
- Kompozycja: [opis]

🔊 **Analiza dźwięku:**
- Częstotliwość: [dane]
- Tonacja: [dane]

📝 **Synteza treści:**
Połączenie wszystkich modalności daje następujący obraz...

📌 **Użyty model:** {model}
🌐 **Tryb:** Multimodalny
✅ **Status:** Analiza zakończona"""
        }

        # Wybierz odpowiedź
        response_text = responses.get(mode, responses["GENERAL"])
        
        return {
            "response": response_text,
            "model": model,
            "confidence": random.uniform(0.78, 0.97),
            "tokens_used": random.randint(100, max_tokens)
        }

# Inicjalizacja silnika AI
ai_engine = AIEngine()

# ============ ENDPOINTY ============

@app.get("/", response_class=HTMLResponse)
async def get_index():
    """Strona główna"""
    try:
        if os.path.exists("templates/index.html"):
            with open("templates/index.html", "r", encoding="utf-8") as f:
                return f.read()
        else:
            return get_fallback_page()
    except Exception as e:
        logger.error(f"Error loading index: {e}")
        return get_fallback_page()

def get_fallback_page():
    """Strona zastępcza gdy brak plików"""
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Astelix AI</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                background: linear-gradient(135deg, #0f0a1a, #1a0f2e);
                color: #e2e8f0;
                font-family: system-ui, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
                text-align: center;
            }
            .container {
                background: rgba(30, 15, 50, 0.6);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(139, 92, 246, 0.15);
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                width: 100%;
            }
            h1 {
                background: linear-gradient(135deg, #7c3aed, #8b5cf6, #a78bfa);
                -webkit-background-clip: text;
                background-clip: text;
                color: transparent;
                font-size: 3rem;
            }
            .status { color: #10b981; margin: 20px 0; }
            .model-tag {
                background: rgba(139, 92, 246, 0.15);
                border: 1px solid rgba(139, 92, 246, 0.2);
                border-radius: 12px;
                padding: 4px 12px;
                font-size: 0.8rem;
                color: #c4b5fd;
                display: inline-block;
                margin: 4px;
            }
            .info {
                color: #94a3b8;
                font-size: 0.9rem;
                margin-top: 20px;
                padding-top: 20px;
                border-top: 1px solid rgba(139, 92, 246, 0.15);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>⭐ Astelix AI</h1>
            <p style="color: #a78bfa;">Hybrid Intelligence System</p>
            <div class="status">✅ Serwer działa poprawnie</div>
            <div>
                <span class="model-tag">GPT-4</span>
                <span class="model-tag">Claude 3</span>
                <span class="model-tag">Gemini Pro</span>
                <span class="model-tag">Llama 2</span>
                <span class="model-tag">Mistral</span>
            </div>
            <div class="info">
                © 2024 Karol Jaskólski<br>
                📧 cocieto2580123@gmail.com<br>
                📞 +48 791 380 755
            </div>
        </div>
    </body>
    </html>
    """)

@app.get("/api/v1/health")
async def health_check():
    """Sprawdzenie stanu systemu"""
    return {
        "status": "healthy",
        "system": APP_NAME,
        "version": APP_VERSION,
        "author": AUTHOR,
        "email": EMAIL,
        "phone": PHONE,
        "models": list(ai_engine.models.keys()),
        "models_count": len(ai_engine.models),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Główny endpoint czatu"""
    try:
        logger.info(f"Chat request: mode={request.mode}, query={request.query[:50]}...")
        
        result = await ai_engine.process(
            query=request.query,
            mode=request.mode,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        return ChatResponse(
            id=str(uuid.uuid4()),
            response=result["response"],
            model=result["model"],
            confidence=result["confidence"],
            processing_time=0.5,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(500, str(e))

@app.get("/api/v1/models")
async def get_models():
    """Pobierz dostępne modele"""
    return {
        "system": APP_NAME,
        "version": APP_VERSION,
        "models": [
            {
                "id": name,
                "name": name,
                "available": data["available"],
                "capabilities": data["capabilities"],
                "description": data["description"]
            }
            for name, data in ai_engine.models.items()
        ],
        "active": sum(1 for m in ai_engine.models.values() if m["available"]),
        "total": len(ai_engine.models)
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket dla strumieniowej komunikacji"""
    await websocket.accept()
    logger.info("WebSocket connected")
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                request = json.loads(data)
                
                result = await ai_engine.process(
                    query=request.get('query', ''),
                    mode=request.get('mode', 'GENERAL'),
                    temperature=request.get('temperature', 0.7),
                    max_tokens=request.get('max_tokens', 1000)
                )
                
                response_text = result["response"]
                words = response_text.split()
                
                await websocket.send_text(json.dumps({
                    "type": "start",
                    "model": result["model"]
                }))
                
                for word in words:
                    await asyncio.sleep(0.02)
                    await websocket.send_text(json.dumps({
                        "type": "chunk",
                        "data": word + " "
                    }))
                
                await websocket.send_text(json.dumps({
                    "type": "end",
                    "metadata": {
                        "model": result["model"],
                        "confidence": result["confidence"],
                        "tokens": result["tokens_used"]
                    }
                }))
                
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "data": "Invalid JSON"
                }))
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

# ============ SERWOWANIE STATYCZNYCH PLIKÓW ============
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/icons", exist_ok=True)
os.makedirs("templates", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ============ URUCHOMIENIE ============
if __name__ == "__main__":
    import sys
    
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    for arg in sys.argv:
        if arg.startswith("--port="):
            port = int(arg.split("=")[1])
        elif arg.startswith("--host="):
            host = arg.split("=")[1]
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   █████╗ ███████╗████████╗███████╗██╗     ██╗██╗  ██╗     ║
║  ██╔══██╗██╔════╝╚══██╔══╝██╔════╝██║     ██║╚██╗██╔╝     ║
║  ███████║███████╗   ██║   █████╗  ██║     ██║ ╚███╔╝      ║
║  ██╔══██║╚════██║   ██║   ██╔══╝  ██║     ██║ ██╔██╗      ║
║  ██║  ██║███████║   ██║   ███████╗███████╗██║██╔╝ ██╗     ║
║  ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝     ║
║                                                              ║
║              ASTELIX AI HYBRID v4.0                         ║
║        © 2024 Karol Jaskólski - Wszelkie prawa zastrzeżone ║
║        📧 cocieto2580123@gmail.com                         ║
║        📞 +48 791 380 755                                  ║
║                                                              ║
║        🌐 Serwer uruchomiony na: http://{}:{}      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """.format(host, port))
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-dotenv==1.0.0
aiofiles==23.2.1
jinja2==3.1.2
httpx==0.25.1
websockets==12.0
python-multipart==0.0.6# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Data
data/
*.db
*.sqlite
*.log

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db# ⭐ Astelix AI

## Hybrid Intelligence System

### 📋 Opis

Astelix AI to zaawansowany system sztucznej inteligencji, który łączy najlepsze cechy wszystkich dostępnych modeli AI w jednym zintegrowanym rozwiązaniu.

### ✨ Funkcje

- 🤖 **Wielomodelowość** - GPT-4, Claude 3, Gemini Pro, Llama 2, Mistral
- 🎯 **6 trybów pracy** - Ogólny, Kod, Analiza, Kreacja, Rozumowanie, Multimodalny
- 📱 **Responsywny interfejs** - Działa na każdym urządzeniu
- 🎤 **Głosowe wpisywanie** - Mów zamiast pisać
- 🔄 **WebSocket** - Strumieniowanie odpowiedzi w czasie rzeczywistym
- 🌐 **Dostęp z każdego miejsca** - Wdrożony na Render.com

### 🚀 Szybki start

```bash
# 1. Pobierz kod
git clone https://github.com/KarolAi666/astelix-ai.git
cd astelix-ai

# 2. Zainstaluj zależności
pip install -r requirements.txt

# 3. Uruchom serwer
python app.py --host 0.0.0.0 --port 8000
---

## 📄 5. `LICENSE`
python:3.11-slimWORKDIR /app# Kopiuj plikiCOPY requirements.txt .RUN pip install --no-cache-dir -r requirements.txtCOPY . .# PortEXPOSE 8000# UruchomCMD ["python", "app.py", "--host", "0.0.0.0", "--port", "8000"]
0 zatwierdzonych komentarzyUwagi0 ( 0 )Zablokuj rozmowęservices:
  - type: web
    name: astelix-ai
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py --host 0.0.0.0 --port 10000
    envVars:
      - key: PORT
        value: 10000
      - key: HOST
        value: 0.0.0.0
    plan: free
