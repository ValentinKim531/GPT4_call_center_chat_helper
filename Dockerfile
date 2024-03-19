FROM python:3.8

WORKDIR /app

COPY . /app

RUN python -m venv /app/venv
RUN . /app/venv/bin/activate && pip install -r requirements.txt


CMD . /app/venv/bin/activate && uvicorn app:app --host=0.0.0.0 --port=8000
