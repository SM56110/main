
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

if not os.path.exists("media"):
    os.makedirs("media")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_memory(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...)
):
    file_location = f"media/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "Капсула памяти успешно сохранена!"
    })
