#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template_string
import random
import json

app = Flask(__name__)

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
        return responses.get(mode, responses["GENERAL"])

ai_engine = AIEngine()

# ============ HTML ============

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Astelix AI</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0f0a1a; color: white; font-family: system-ui; text-align: center; padding: 40px; }
        h1 { font-size: 3rem; background: linear-gradient(135deg,#7c3aed,#a78bfa); -webkit-background-clip: text; color: transparent; }
        .glass { background: rgba(30,15,50,0.6); border: 1px solid rgba(139,92,246,0.15); border-radius: 20px; padding: 20px; max-width: 500px; margin: 20px auto; }
        input { width: 80%; padding: 10px; border-radius: 10px; border: none; }
        button { padding: 10px 30px; border-radius: 10px; border: none; background: #7c3aed; color: white; cursor: pointer; }
        #response { margin-top: 20px; padding: 15px; background: rgba(0,0,0,0.3); border-radius: 10px; text-align: left; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>⭐ Astelix AI</h1>
    <p style="color:#a78bfa;">Hybrid Intelligence System</p>
    <div class="glass">
        <h3>💬 Zapytaj Astelix AI</h3>
        <select id="mode">
            <option value="GENERAL">Ogólny</option>
            <option value="CODING">Kod</option>
            <option value="ANALYSIS">Analiza</option>
            <option value="CREATION">Kreacja</option>
            <option value="REASONING">Rozumowanie</option>
            <option value="MULTI_MODAL">Multimodalny</option>
        </select>
        <br><br>
        <input type="text" id="query" placeholder="Wpisz pytanie...">
        <br><br>
        <button onclick="ask()">Wyślij</button>
        <div id="response"></div>
    </div>
    <p style="color:#94a3b8; font-size:0.8rem;">© 2024 Karol Jaskólski | 📧 cocieto2580123@gmail.com</p>

    <script>
        async function ask() {
            const query = document.getElementById('query').value;
            const mode = document.getElementById('mode').value;
            const responseDiv = document.getElementById('response');
            responseDiv.innerHTML = "⏳ Myślę...";
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({query: query, mode: mode})
                });
                const data = await res.json();
                responseDiv.innerHTML = data.response;
            } catch(e) {
                responseDiv.innerHTML = "❌ Błąd: " + e.message;
            }
        }
    </script>
</body>
</html>
"""

# ============ ENDPOINTY ============

@app.route('/')
def index():
    return HTML

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        query = data.get('query', '')
        mode = data.get('mode', 'GENERAL')
        response = ai_engine.process(query, mode)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'❌ Błąd: {str(e)}'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'system': 'Astelix AI'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
