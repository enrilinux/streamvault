from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
import os
import json
from datetime import datetime

from app.downloader import download_video

app = FastAPI()

DOWNLOAD_DIR = "downloads"
HISTORY_FILE = "history.json"
LOG_FILE = "data/app.log"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write("")

def write_log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Legge il file HTML direttamente
    try:
        with open("/app/app/templates/index.html", "r") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Errore</h1><p>{str(e)}</p>", status_code=500)


@app.get("/test")
async def test():
    return {"status": "ok", "message": "Server funzionante"}


@app.post("/download")
async def download(url: str = Form(...), mode: str = Form(...)):
    try:
        path = download_video(url, mode)
        write_log(f"Downloaded: {url} -> {path}")

        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

        history.append({
            "url": url,
            "mode": mode,
            "path": path,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M")
        })

        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)

        return {"path": path}
    except Exception as e:
        write_log(f"Error: {str(e)}")
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/history")
async def history():
    try:
        with open(HISTORY_FILE) as f:
            return JSONResponse(json.load(f))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/file")
async def file(path: str):
    try:
        safe_path = os.path.join(DOWNLOAD_DIR, os.path.basename(path))
        if not os.path.exists(safe_path):
            return JSONResponse(status_code=404, content={"error": "File not found"})
        return FileResponse(safe_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
