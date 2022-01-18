from ssl import RAND_add
from fastapi import FastAPI, File, UploadFile, Depends
from fastapi.staticfiles import StaticFiles
from util.config import configuration
import os
from util.misc import *
from util.filenameGenerator import filenameGenerator
from util.config import configuration

configuration = config.configuration()

app = FastAPI()
app.mount(configuration.IMAGE_DIR, StaticFiles(directory=configuration.UPLOAD_PATH), name=configuration.IMAGE_DIR)

@app.get("/")
async def index():
    return {"message": "Hello"}


@app.post("/upload")
async def upload(file: UploadFile = File(...), authorized = Depends(checkCredentials)):
    if file.content_type not in configuration.ALLOWED_CONTENT:
        return {"message": configuration.ERROR_UNALLOWED_CONTENT}
    if authorized:
        if configuration.RANDOMIZED_FILENAMES:
            _extension = file.filename.split('.')[1].lower() # Save the extension of the file for upload
            file.filename = filenameGenerator.generateName(5) +f".{_extension}"
        await uploadFile(file)
        return {"url": configuration.BASE_URL+configuration.IMAGE_DIR+file.filename}


@app.on_event("startup")
def startup():
    # Validate configuration
    validateConfiguration()
        
    # Create upload directory if it doesn't exist
    if not os.path.exists(configuration.UPLOAD_PATH):
        os.makedirs(configuration.UPLOAD_PATH)
        print(f"Created {configuration.UPLOAD_PATH}")

