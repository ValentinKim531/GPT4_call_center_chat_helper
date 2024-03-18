from fastapi import FastAPI, HTTPException, UploadFile, File
from environs import Env
from openai import AsyncOpenAI
from prompt import prompt

app = FastAPI()
env = Env()
env.read_env()

client = AsyncOpenAI(api_key=env.str("OPENAI_API_KEY"))

document_text = ""


@app.post("/upload-text-file/")
async def upload_text_file(text_file: UploadFile = File(...)):
    global document_text
    if text_file.content_type != "text/plain":
        raise HTTPException(
            status_code=400,
            detail="File must be a text file"
        )
    content = await text_file.read()
    document_text = content.decode("utf-8")
    return {"message": "Text file uploaded successfully"}


@app.post("/ask-question/")
async def ask_question(question: str):
    if not document_text:
        raise HTTPException(
            status_code=404,
            detail="Text file not found. Please upload a text file first."
        )

    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": question},
            {"role": "assistant", "content": document_text}
        ],
        max_tokens=1000
    )

    if response.choices:
        answer_content = response.choices[0].message.content
        return {"answer": answer_content}
    else:
        return {"answer": "No response from the model."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
