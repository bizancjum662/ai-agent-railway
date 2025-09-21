# main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Simple AI Agent on Railway")

# OpenAI client - korzysta z OPENAI_API_KEY ustawionego w środowisku
client = OpenAI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    if not os.environ.get("OPENAI_API_KEY"):
        # Błąd 500 jeśli nie ustawiono klucza (lokalnie możesz użyć .env)
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY not set")

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": req.message},
            ],
            max_tokens=500,
            temperature=0.7,
        )
        # Bezpieczne wyciąganie treści odpowiedzi
        msg = completion.choices[0].message
        try:
            content = msg["content"]
        except Exception:
            content = getattr(msg, "content", str(msg))
        return {"reply": content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI error: {e}")
