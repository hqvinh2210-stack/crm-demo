FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY frontend ./frontend

EXPOSE 8000

CMD sh -c "python seed_demo_data.py && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"
