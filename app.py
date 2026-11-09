from pathlib import Path

from flask import Flask, request

app = Flask(__name__)
PUBLIC_DIR = Path(__file__).resolve().parent / "public"


@app.get("/download")
def download():
    file_path = request.args.get("file_path")
    if not file_path:
        return "Missing 'file_path' parameter", 400

    # Ensure the file path is within the public directory
    full_path = (PUBLIC_DIR / file_path).resolve()
    if not full_path.is_relative_to(PUBLIC_DIR.resolve()):
        return "Forbidden", 403
    if not full_path.is_file():
        return "File not found", 404
    return full_path.read_text(), 200
