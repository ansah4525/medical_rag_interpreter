import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import pytesseract
from PIL import Image
import platform
from backend.chat import run_rag


CHAT_HISTORY = {}
MAX_HISTORY = 5  # Limit the number of turns stored per session

pytesseract.pytesseract.tesseract_cmd = r"D:\medicalbot\tesseract.exe"  # Update this path as needed
app = Flask( __name__,
    static_folder="../frontend",
    static_url_path="")
CORS(app)
DOCUMENT_STORE = {}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Windows only (if needed)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r"D:\medicalbot\tesseract.exe"

def extract_text(file_path):
    ext = os.path.splitext(file_path.lower())[1]
    print("Processing file:", file_path)

    if ext == ".pdf":
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    elif ext in [".png", ".jpg", ".jpeg"]:
        try:
            image = Image.open(file_path)

            # ✅ Convert to grayscale
            image = image.convert("L")

            # ✅ Increase contrast / binarize
            image = image.point(lambda x: 0 if x < 140 else 255, "1")

            config = r"--oem 3 --psm 6"
            text = pytesseract.image_to_string(image, config=config)

            return text.strip()

        except Exception as e:
            print("OCR ERROR FULL:", repr(e))
            return ""


    else:
        return "Unsupported file type"

import uuid
@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/extract-text", methods=["POST"])
def extract_text_api():
    print("Request received")

    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    text = extract_text(file_path)
    os.remove(file_path)

    session_id = str(uuid.uuid4())
    DOCUMENT_STORE[session_id] = text

    return jsonify({
        "session_id": session_id,
        "text": text
    })

@app.route("/chat", methods=["POST"])
def chat_api():

    data = request.get_json()

    session_id = data.get("session_id")
    user_question = data.get("message", "").strip()

    # -------------------------------
    # Uploaded report (optional)
    # -------------------------------

    report_text = ""

    if session_id and session_id in DOCUMENT_STORE:
        report_text = DOCUMENT_STORE[session_id]

    # -------------------------------
    # Chat history
    # -------------------------------

    history_key = session_id if session_id else "general"

    if history_key not in CHAT_HISTORY:
        CHAT_HISTORY[history_key] = []

    history = CHAT_HISTORY[history_key][-MAX_HISTORY:]

    # -------------------------------
    # Run RAG
    # -------------------------------

    result = run_rag(
        question=user_question,
        report=report_text,
        history=history
    )

    # -------------------------------
    # Save conversation
    # -------------------------------

    history.append({
        "user": user_question,
        "assistant": result["answer"]
    })

    return jsonify({
        "reply": result["answer"]
    })
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
