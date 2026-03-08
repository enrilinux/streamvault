import yt_dlp
import glob
import re
import os

DOWNLOAD_DIR = "downloads"

def sanitize_filename(name):
    """Rimuove caratteri non validi dai nomi dei file"""
    return re.sub(r'[\\/*?:"<>|]', '', name)

def download_video(url, mode):
    # Template che usa il titolo e l'ID
    template = f"{DOWNLOAD_DIR}/%(title)s - %(id)s.%(ext)s"

    if mode == "audio":
        opts = {
            "format": "bestaudio/best",
            "outtmpl": template,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }
    else:
        opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": template
        }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)

    # Prende il file scaricato e lo rinomina in modo sicuro
    downloaded_files = glob.glob(f"{DOWNLOAD_DIR}/*{info['id']}*")
    final_path = downloaded_files[0]
    safe_path = os.path.join(
        DOWNLOAD_DIR,
        sanitize_filename(os.path.basename(final_path))
    )
    if safe_path != final_path:
        os.rename(final_path, safe_path)

    return safe_path