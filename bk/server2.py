from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

SHARED = "shared"
os.makedirs(SHARED, exist_ok=True)

@app.route("/")
def index():
    files = os.listdir(SHARED)

    html = """
    <h1>Prism SLINT Databases</h1>

    <h2>UPLOAD</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">Upload</button>
    </form>

    <h2>Index</h2>
    """

    for f in files:
        html += f'<a href="/download/{f}">{f}</a><br>'

    return html

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return "No file selected"

    file = request.files["file"]

    if file.filename == "":
        return "No file selected"

    file.save(os.path.join(SHARED, file.filename))

    return f"Uploaded: {file.filename}<br>/Back</a>"

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(
        SHARED,
        filename,
        as_attachment=True
    )

app.run(host="0.0.0.0", port=5000)