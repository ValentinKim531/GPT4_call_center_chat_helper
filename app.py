import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
from environs import Env
from openai import AsyncOpenAI
import re

app = FastAPI()
env = Env()
env.read_env()

client = AsyncOpenAI(api_key=env.str("OPENAI_API_KEY"))
assistant_id = env.str("ASSISTANT_ID")


class Question(BaseModel):
    question: str


def remove_annotations(text: str) -> str:
    pattern = r'\【.*?\】'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


@app.post("/ask-question/")
async def ask_question(question: Question):
    thread = await client.beta.threads.create()

    await client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=question.question
    )

    run = await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id
    )

    while run.status in ['queued', 'in_progress', 'cancelling']:
        await asyncio.sleep(1)
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    if run.status == 'completed':
        messages = await client.beta.threads.messages.list(
            thread_id=thread.id
        )

        assistant_messages = [remove_annotations(msg.content[0].text.value) for msg in messages.data if
                              msg.role == 'assistant']
        full_response = " ".join(assistant_messages)
        return {"answer": full_response}
    else:
        return {"answer": "Не удалось получить ответ от ассистента."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
