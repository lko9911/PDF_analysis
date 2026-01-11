# 백엔드 서버 구축 - FastAPI 사용, OpenAI API 연동, PDF 업로드 기능 포함

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import os
import shutil

# 환경변수 로드
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS (Middleware) - 브라우저에서 다른 도메인이 서버 접근 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 접근
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- 텍스트 분석 ----------
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

    return {
        "result": response.choices[0].message.content
    }

# ---------- PDF 업로드 ----------
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "path": file_path
    }
