from flask import Flask, request, send_from_directory
import os
from html import escape
#Change the value of PORT to modify the port being used to run this program on the host machine.
PORT = 5000
app = Flask(__name__)
SHARED = "shared"
ASSETS = "assets"
os.makedirs(SHARED, exist_ok=True)
os.makedirs(ASSETS, exist_ok=True)
def human_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    return f"{size:.1f} {units[i]}"
@app.route("/")
def index():
    files = sorted(os.listdir(SHARED))
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Prism SLINT Databases</title>

<style>

body {{
    background: #05080c;
    color: #8bffb5;
    font-family: Consolas, monospace;
    margin: 0;
    padding: 20px;
}}

.panel {{
    border: 1px solid #1c6b39;
    background: #09110c;
    max-width: 1000px;
    margin: auto;
    box-shadow: 0 0 30px rgba(0,255,128,.15);
}}

.header {{
    background: #081d11;
    border-bottom: 1px solid #1c6b39;
    padding: 15px;
}}

.title {{
    font-size: 28px;
    color: #77ffcc;
    font-weight: bold;
    letter-spacing: 2px;
}}

.subtitle {{
    color: #5dd899;
    margin-top: 5px;
}}

.content {{
    padding: 20px;
}}

.section {{
    margin-bottom: 25px;
}}

.section-title {{
    color: #50ff9d;
    margin-bottom: 10px;
}}

input[type=file] {{
    background: #111;
    color: white;
    border: 1px solid #1c6b39;
    padding: 8px;
}}

button {{
    background: #114d2b;
    color: white;
    border: 1px solid #2ea45d;
    padding: 8px 16px;
    cursor: pointer;
    font-family: Consolas, monospace;
}}

button:hover {{
    background: #1b6f3f;
}}

.file {{
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px;
    border-bottom: 1px solid #10381f;
}}

.file:hover {{
    background: rgba(0,255,128,.08);
}}

.file img {{
    width: 16px;
    height: 16px;
    object-fit: contain;
}}

.file a {{
    color: #9bffd4;
    text-decoration: none;
    flex-grow: 1;
}}

.file a:hover {{
    color: white;
}}

.size {{
    color: #55bb88;
}}

.footer {{
    margin-top: 20px;
    padding-top: 10px;
    border-top: 1px solid #10381f;
    color: #4e9368;
    font-size: 12px;
}}

.scan {{
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 9999;
    background:
        repeating-linear-gradient(
            to bottom,
            rgba(255,255,255,.02),
            rgba(255,255,255,.02) 1px,
            transparent 1px,
            transparent 4px
        );
}}

</style>
</head>

<body>

<div class="scan"></div>

<div class="panel">

<div class="header">
    <div class="title">PRISM DATABASES</div>

    <div class="subtitle">
        OBJECT COUNT: {len(files)}
    </div>
</div>

<div class="content">

<div class="section">
    <div class="section-title">
        File Uploads (Uploads to host machine shared folder)
    </div>

    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" required>
        <button type="submit">Upload</button>
    </form>
</div>

<div class="section">

<div class="section-title">
    INDEX
</div>
"""

    for f in files:
        path = os.path.join(SHARED, f)
        size = human_size(os.path.getsize(path))

        safe_name = escape(f)
        download_url = "/download/" + escape(f, quote=True)

        html += f"""
<div class="file">
    <img src="/assets/folder.gif" alt="">
    <a href="{download_url}">
        {safe_name}
    </a>
    <span class="size">{size}</span>
</div>
"""

    html += """
</div>

<div class="footer">
PRISM STREAMER (2026)<br>
</div>

</div>
</div>

</body>
</html>
"""

    return html


@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return """
<!DOCTYPE html>
<html>
<head>
<title>Upload Error</title>
</head>
<body>
<img src="/assets/back.gif" alt="">
<a href="/">Back</a><br><br>
No file selected.
</body>
</html>
"""

    file = request.files["file"]

    if file.filename == "":
        return """
<!DOCTYPE html>
<html>
<head>
<title>Upload Error</title>
</head>
<body>
<img src="/assets/back.gif" alt="">
<a href="/">Back</a><br><br>
No file selected.
</body>
</html>
"""

    filename = os.path.basename(file.filename)
    file.save(os.path.join(SHARED, filename))

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Upload Successful</title>
</head>
<body>
<img src="/assets/back.gif" alt="">
<a href="/">Back</a><br><br>

Upload successful.<br>
Stored object:<br>
<b>{escape(filename)}</b>
</body>
</html>
"""


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(
        SHARED,
        filename,
        as_attachment=True
    )


@app.route("/assets/<path:filename>")
def assets(filename):
    return send_from_directory(
        ASSETS,
        filename
    )


app.run(
    host="0.0.0.0",
    port=PORT
)