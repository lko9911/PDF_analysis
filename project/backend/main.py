import os
import shutil
import fitz  # PyMuPDF
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- 헬퍼 함수: PDF 텍스트 추출 ----------
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text
    except Exception as e:
        raise Exception(f"PDF 텍스트 추출 중 오류 발생: {str(e)}")

# ---------- API 엔드포인트 ----------

@app.post("/upload-and-summarize")
async def upload_and_summarize(file: UploadFile = File(...)):
    # 1. 파일 확장자 체크
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="PDF 파일만 업로드 가능합니다.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    try:
        # 2. 파일 저장
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. PDF에서 텍스트 추출
        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="PDF에서 읽을 수 있는 텍스트가 없습니다.")

        # 4. OpenAI를 이용한 요약 (내용이 너무 길 경우 앞부분 4000자만 사용 예시)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "너는 논문이나 보고서를 요약해주는 전문 연구원이야."},
                {"role": "user", "content": f"다음 PDF 내용을 핵심 위주로 요약해줘:\n\n{extracted_text[:4000]}"}
            ]
        )

        return {
            "filename": file.filename,
            "summary": response.choices[0].message.content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 기존 텍스트 분석 API도 유지
class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
async def analyze_text(req: TextRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": f"Explain in Korean:\n{req.text}"}
            ]
        )
        return {"result": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))