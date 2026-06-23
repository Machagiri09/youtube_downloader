from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os
import tempfile
import glob
import uuid

app = Flask(__name__, template_folder="templates")

DOWNLOAD_DIR = tempfile.gettempdir()
visit_count = 0


@app.route("/")
def home():
    global visit_count
    visit_count += 1
    return render_template("index.html", visitors=visit_count)


@app.route("/download", methods=["POST"])
def download():
    video_url = request.form.get("url", "").strip()

    if not video_url:
        return render_template("index.html", error="Please enter a URL", visitors=visit_count)

    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        return render_template(
            "index.html",
            error="Invalid URL! Please enter a valid YouTube URL.",
            visitors=visit_count
        )

    try:
        download_subdir = os.path.join(DOWNLOAD_DIR, "yt_downloads")
        os.makedirs(download_subdir, exist_ok=True)

        file_id = uuid.uuid4().hex
        output_template = os.path.join(download_subdir, f"{file_id}.%(ext)s")

        ydl_opts = {
            "format": (
                "best[filesize<=300M][ext=mp4]/"
                "best[filesize_approx<=300M][ext=mp4]/"
                "best[filesize<=300M]/"
                "best[filesize_approx<=300M]/"
                "best[ext=mp4]/best"
            ),
            "outtmpl": output_template,
            "max_filesize": 300000000,
            "noplaylist": True,
            "quiet": False,
            "no_warnings": False,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)

        video_files = glob.glob(os.path.join(download_subdir, f"{file_id}.*"))

        if video_files:
            latest_file = max(video_files, key=os.path.getmtime)

            return send_file(
                latest_file,
                as_attachment=True,
                download_name="video" + os.path.splitext(latest_file)[1]
            )

        return render_template(
            "index.html",
            error="Download finished, but file was not found.",
            visitors=visit_count
        )

    except Exception as e:
        error_msg = str(e).lower()
        print(f"Exception: {e}")

        if "file is larger than max-filesize" in error_msg or "max-filesize" in error_msg:
            return render_template(
                "index.html",
                error="Video is too large. Maximum allowed size is 300MB.",
                visitors=visit_count
            )

        elif "429" in error_msg or "403" in error_msg or "blocked" in error_msg:
            return render_template(
                "index.html",
                error="YouTube blocked the request. Please wait and try again.",
                visitors=visit_count
            )

        elif "404" in error_msg or "not found" in error_msg or "video unavailable" in error_msg:
            return render_template(
                "index.html",
                error="Video not found or unavailable. Please check the URL.",
                visitors=visit_count
            )

        else:
            return render_template(
                "index.html",
                error=f"Download failed: {str(e)}",
                visitors=visit_count
            )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))