from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import yt_dlp
import os
import re  # For more robust URL validation

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join("static", "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy-policy.html')


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"].strip()

        # Validate Instagram URL (basic check for a valid Instagram URL)
        if not re.match(r"^(https?://)?(www\.)?instagram\.com/.+$", url):
            return render_template("index.html", error="Bro, that ain't a valid Instagram URL!")

        opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'mp4',
            'quiet': True,
            'noplaylist': True,
            'http_headers': {'User-Agent': 'Mozilla/5.0'},
        }

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                filename = os.path.basename(filename)  # Keep only the file name (not full path)
                return render_template("index.html", filename=filename)
        except Exception as e:
            return render_template("index.html", error=f"An error occurred: {str(e)}")

    return render_template("index.html")

@app.route("/downloads/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
