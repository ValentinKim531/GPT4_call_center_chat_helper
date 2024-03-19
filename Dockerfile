FROM python:3.8

WORKDIR /app

COPY . /app

RUN python -m venv /app/venv
RUN . /app/venv/bin/activate && pip install -r requirements.txt

ENV PORT=8000

EXPOSE $PORT

CMD . /app/venv/bin/activate && uvicorn app:app --host=0.0.0.0 --port=$PORT
