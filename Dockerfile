FROM python:3.11-slim

WORKDIR /app

# Kopiuj pliki
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Port
EXPOSE 8000

# Uruchom
CMD ["python", "app.py", "--host", "0.0.0.0", "--port", "8000"]
