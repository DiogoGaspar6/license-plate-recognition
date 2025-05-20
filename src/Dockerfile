FROM python:3.8-slim

WORKDIR /app

RUN pip install uv && apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY requirements.txt .

RUN uv pip install --no-cache-dir -r requirements.txt --system

COPY . .

COPY . .env

CMD ["python", "src/main.py"]