import fitz  # PyMuPDF

pdf_path = "High Mechanical Performance of Lattice Structures Fabricated by Additive Manufacturing.pdf"   # 테스트할 PDF 파일 경로

try:
    doc = fitz.open(pdf_path)

    full_text = ""

    for page_num, page in enumerate(doc):
        text = page.get_text()
        print(f"\n===== Page {page_num+1} =====")
        print(text[:10000])  # 페이지당 앞 ~자만 출력
        full_text += text

    print("\n===========================")
    print("총 추출 문자 수:", len(full_text))

    if len(full_text.strip()) == 0:
        print("⚠ 텍스트가 없습니다. (스캔본일 가능성)")
    else:
        print("✅ 텍스트 추출 성공")

except Exception as e:
    print("❌ 오류 발생:", e)
