import fitz  # PyMuPDF
import os

pdf_path = "High Mechanical Performance of Lattice Structures Fabricated by Additive Manufacturing.pdf"
output_dir = "pdf_text_pages"  # 저장할 폴더

# 폴더 없으면 생성
os.makedirs(output_dir, exist_ok=True)

try:
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num, page in enumerate(doc):
        text = page.get_text()
        full_text += text

        # 페이지별 라인 단위로 나누기
        lines = text.splitlines()

        # 파일 이름: page_1.txt, page_2.txt ...
        file_path = os.path.join(output_dir, f"page_{page_num+1}.txt")

        # 페이지 텍스트 파일에 저장 (라인 단위)
        with open(file_path, "w", encoding="utf-8") as f:
            for i, line in enumerate(lines):
                f.write(f"{i+1}: {line}\n")  # 줄 번호 포함

        print(f"✅ Page {page_num+1} 저장 완료: {file_path}")

    # 전체 텍스트 저장 (선택)
    full_text_path = os.path.join(output_dir, "full_text.txt")
    with open(full_text_path, "w", encoding="utf-8") as f:
        f.write(full_text)
    print(f"\n✅ 전체 텍스트 저장 완료: {full_text_path}")

    if len(full_text.strip()) == 0:
        print("⚠ 텍스트가 없습니다. (스캔본일 가능성)")
    else:
        print("✅ PDF 전체 텍스트 추출 성공")

except Exception as e:
    print("❌ 오류 발생:", e)
