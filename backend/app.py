from flask import Flask, request, send_file, jsonify
import os
import uuid
from .main import parse_json_to_csv

app = Flask(__name__)
UPLOAD_FOLDER = "backend/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if not file.filename.endswith(".json"):
        return jsonify({"error": "Only JSON files allowed"}), 400

    filename = f"{uuid.uuid4()}.json"
    json_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(json_path)

    csv_path, analysis_data = parse_json_to_csv(json_path)

    return jsonify({
        "download_url": f"/download/{os.path.basename(csv_path)}",
        "analysis": analysis_data
    })

@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
