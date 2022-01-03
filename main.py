from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.staticfiles import StaticFiles
from config.vars import *
import os
from util.misc import *


app = FastAPI()
app.mount(IMAGE_DIR, StaticFiles(directory=UPLOAD_PATH), name=IMAGE_DIR)

@app.get("/")
async def index():
    return {"message": "Hello"}


@app.post("/upload")
async def upload(file: UploadFile = File(...), authorized = Depends(checkCredentials)):
    if file.content_type not in ALLOWED_CONTENT:
        return {"message": ERROR_UNALLOWED_CONTENT}
    if authorized:
        await uploadFile(file)
        return {"url": URL_PATH+IMAGE_DIR+file.filename}


@app.on_event("startup")
def startup():
    # Validate configuration
    validateConfiguration()
        
    # Create upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
        print(f"Created {UPLOAD_PATH}")

