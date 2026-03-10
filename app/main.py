from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import os
import json
from datetime import datetime

from app.downloader import download_video

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

DOWNLOAD_DIR = "downloads"
HISTORY_FILE = "history.json"

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs("data", exist_ok=True)

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def write_log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")        


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
async def download(url: str = Form(...), mode: str = Form(...)):
    path = download_video(url, mode)

    # salva nella cronologia
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


@app.get("/history")
async def history():
    with open(HISTORY_FILE) as f:
        return JSONResponse(json.load(f))


@app.get("/file")
async def file(path: str):
    return FileResponse(path)
