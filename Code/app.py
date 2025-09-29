from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid

# Import your real implementations here
from integrate import FixedAtelierGenerator, process_image, generate_multilingual_poem

UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

client = FixedAtelierGenerator(wm_text="Ghiblify! by VeerAvi")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    style_key = request.form["style"]
    language = request.form["language"]
    length = request.form["length"]
    style = request.form["style_name"]

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    input_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file.save(input_path)

    output_path = process_image(input_path, OUTPUT_FOLDER, style_key, client)

    if output_path:
        poems = generate_multilingual_poem(output_path, [language], length, style)
        return jsonify({
            "image_url": "/" + output_path.replace("\\", "/"),
            "poem": poems.get(language, "No poem generated.")
        })
    else:
        return jsonify({"error": "Image processing failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
