FROM docker.io/python:3.11-slim

WORKDIR /app

COPY ../src/main.py .

COPY ../src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]