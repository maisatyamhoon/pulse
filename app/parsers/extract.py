import pdfplumber
import pytesseract
from io import BytesIO
from pdf2image import convert_from_bytes

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_pdf_text(file, password=None) -> str:
    file.file.seek(0)
    pdf_bytes = file.file.read()
    file.file.seek(0)

    text = ""
    clean_password = password.strip() if password else None

    # ---------- Normal extraction ----------
    try:
        with pdfplumber.open(BytesIO(pdf_bytes), password=clean_password) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        print("PDFPLUMBER ERROR:", e)

    # ---------- OCR fallback ----------
    if not text.strip():
        print("Falling back to OCR...")

        try:
            images = convert_from_bytes(
                pdf_bytes,
                userpw=clean_password
            )

            print(f"OCR IMAGES GENERATED: {len(images)}")

            for i, image in enumerate(images):
                ocr_text = pytesseract.image_to_string(image)
                print(f"OCR PAGE {i+1} TEXT:")
                print(ocr_text[:1000])
                text += ocr_text + "\n"

        except Exception as e:
            print("OCR ERROR:", e)

    return text.strip()