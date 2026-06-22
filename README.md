# YouTube Video Downloader

A simple and elegant Flask web application that downloads YouTube videos with a beautiful glassmorphism UI. Works on desktop and mobile devices.

## Features

- 🎬 **Download YouTube videos** — Paste any YouTube URL and download instantly
- 🎨 **Beautiful UI** — Glassmorphism design with background image support
- 📱 **Fully responsive** — Works perfectly on desktop, tablet, and mobile
- ❌ **URL validation** — Checks if it's a valid YouTube URL before downloading
- ⚡ **Fast & reliable** — Uses `yt-dlp` for stable downloads
- 🌙 **Dark theme** — Easy on the eyes with a modern dark gradient background

## Tech Stack

- **Backend:** Python, Flask
- **Video Processing:** `yt-dlp` (maintained YouTube downloader)
- **Frontend:** HTML, CSS (responsive, no frameworks)
- **Deployment:** Vercel-ready

## Project Structure

```
youtube-downloader/
├── api/
│   ├── app.py
│   ├── static/
│   │   └── background.jpg (optional)
│   └── templates/
│       └── index.html
├── requirements.txt
├── vercel.json
└── README.md
```

## Installation

### Local Setup

1. **Clone or create the project:**

```bash
git clone https://github.com/yourusername/youtube-downloader.git
cd youtube-downloader
```

2. **Create virtual environment (optional but recommended):**

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Mac/Linux
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **(Optional) Add a background image:**

Place your image as `api/static/background.jpg`

## Usage

**Run the Flask app:**

```bash
python api/app.py
```

**Open in browser:**

```
http://127.0.0.1:5000
```

1. Paste a YouTube URL (e.g., `https://www.youtube.com/watch?v=...`)
2. Click **Download Video**
3. The video will download to your computer automatically

Downloaded videos are saved in your system's temp folder.

## How It Works

1. User enters a YouTube URL in the form
2. Flask validates that it's a real YouTube URL
3. `yt-dlp` fetches the video metadata and downloads it
4. The video file is sent to the user's browser as a download
5. Error messages appear directly on the website if something fails

## Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Displays the homepage |
| `/download` | POST | Processes the YouTube URL and downloads the video |

## Customization

### Change Background Image

1. Place your image in `api/static/`
2. The app automatically uses `background.jpg`
3. For a different filename, edit the HTML:
   ```html
   background-image: url("{{ url_for('static', filename='your-image.jpg') }}");
   ```

### Adjust Glassmorphism Effect

Edit the CSS in `templates/index.html`:
- `backdrop-filter: blur(16px)` — Change the blur amount
- `rgba(30, 41, 59, 0.25)` — Change card transparency
- Border colors and shadows for more customization

## Deployment to Vercel

1. Push to GitHub:
```bash
git add .
git commit -m "YouTube downloader app"
git push origin main
```

2. Go to [vercel.com](https://vercel.com)
3. Click **Add New Project**
4. Select your GitHub repo
5. Click **Deploy**

Vercel will automatically detect the Python project and deploy it.

## Requirements

- Python 3.7+
- Flask
- yt-dlp
- Pillow (for image support)

See `requirements.txt` for exact versions.

## Troubleshooting

### "Invalid URL! Please enter a valid YouTube URL"
- Make sure the URL contains `youtube.com` or `youtu.be`
- Try copying the URL directly from the address bar

### "YouTube blocked the request"
- YouTube rate-limits rapid downloads
- Wait a few moments and try again
- Try a different video

### Download seems to work but no file appears
- Check your browser's Downloads folder
- The file might be named `video.mp4`
- On some systems, downloaded files go to your temp folder

### Port 5000 already in use
```bash
python api/app.py --port 5001
```

## Why yt-dlp?

We use `yt-dlp` instead of older libraries because:
- ✅ Actively maintained and updated
- ✅ Handles YouTube's frequent changes
- ✅ More reliable than alternatives like `pytube`
- ✅ Better error handling
- ✅ Works with various video qualities and formats

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

Open source and available for personal or educational use.

## Future Improvements

- [ ] Audio-only downloads (MP3 format)
- [ ] Custom video quality selection
- [ ] Playlist downloads
- [ ] Download history/favorites
- [ ] Dark/light theme toggle

## Support

If you encounter issues:
1. Check the error message on the website
2. Verify the YouTube URL is correct
3. Try a different video
4. Check that you have internet connection

---

**Made with ❤️ using Flask and yt-dlp**
