from fastapi import FastAPI
from pydantic import BaseModel
import openai
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("YOUR_OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(req: TextRequest):
    prompt = f"""
    You are a research assistant.
    Explain the following text in Korean.
    If it is a technical term, include:
    - definition
    - simple explanation
    - example usage

    Text:
    {req.text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"result": response.choices[0].message.content}
