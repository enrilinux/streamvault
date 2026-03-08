from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os
import uuid

from app.downloader import download_video

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
async def download(url: str = Form(...), mode: str = Form(...)):
    path = download_video(url, mode)
    return {"path": path}


@app.get("/file")
async def file(path: str):
    return FileResponse(path)
