from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os
import tempfile
import glob

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
        return render_template("index.html", error="Please enter a URL")
    
    # Validate if it's a YouTube URL
    if "youtube.com" not in video_url and "youtu.be" not in video_url:
        return render_template("index.html", error="Invalid URL! Please enter a valid YouTube URL (youtube.com or youtu.be)")
    
    try:
        download_subdir = os.path.join(DOWNLOAD_DIR, "yt_downloads")
        os.makedirs(download_subdir, exist_ok=True)
        
        ydl_opts = {
            'format': 'best[filesize<300M][ext=mp4]/best[filesize<300M]',
            'outtmpl': os.path.join(download_subdir, 'video'),
            'max_filesize': 300000000,  # 300MB limit
            'quiet': False,
            'no_warnings': False,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(video_url, download=True)
        
        # List all files in the directory
        all_files = os.listdir(download_subdir)
        print(f"Files in {download_subdir}: {all_files}")
        
        # Look for ANY video file (mp4, webm, mkv, etc)
        video_extensions = ['*.mp4', '*.webm', '*.mkv', '*.flv', '*.avi']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(glob.glob(os.path.join(download_subdir, ext)))
        
        print(f"Found video files: {video_files}")
        
        if video_files:
            # Get the most recently modified file
            latest_file = max(video_files, key=os.path.getmtime)
            print(f"Sending file: {latest_file}")
            
            return send_file(
                latest_file,
                as_attachment=True,
                download_name="video.mp4",
                mimetype='video/mp4'
            )
        else:
            return render_template("index.html", error="Download complete! Video file saved to your temp folder.")
    
    except Exception as e:
        error_msg = str(e).lower()
        print(f"Exception: {error_msg}")
        
        # Check for file size errors
        if "file too large" in error_msg or "max_filesize" in error_msg or "files larger than" in error_msg:
            return render_template("index.html", error="❌ Video is too large (max 300MB). Please try a shorter video or different quality.")
        
        # Check for YouTube blocks
        elif "429" in error_msg or "403" in error_msg or "blocked" in error_msg:
            return render_template("index.html", error="❌ YouTube blocked the request. Please wait a moment and try again.")
        
        # Check for invalid URL
        elif "404" in error_msg or "not found" in error_msg or "video unavailable" in error_msg:
            return render_template("index.html", error="❌ Video not found or unavailable. Please check the URL.")
        
        # Generic error
        else:
            return render_template("index.html", error="❌ Download failed. Please try again with a different video.")

if __name__ == "__main__":
    # Use this for Railway/production
    app.run(host='0.0.0.0', port=5000)
    # Or use this for local testing
    # app.run(debug=True)