from fastapi import FastAPI, File, UploadFile
from util.CustomException import ConfigurationValidationError, InvalidJSON
from util.defaultConfig import DEFAULT_AUTH
from config.vars import *
import os
import json

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "Hello"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_CONTENT:
        return {"message": ERROR_UNALLOWED_CONTENT}
    await uploadFile(file)
    return {"filename": file.filename}

@app.on_event("startup")
def startup():
    # Validate configuration
    validateConfiguration()
        
    # Create upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
        print(f"Created {UPLOAD_PATH}")

async def uploadFile(file: UploadFile = File(...)):
    content = await file.read()
    with open(UPLOAD_PATH+file.filename, 'wb') as f:
        f.write(content)

def validateConfiguration() -> Exception:
    if not os.path.exists(CONFIG_PATH+CONFIG_AUTH):
        os.makedirs(CONFIG_PATH, exist_ok=True)
        with open(CONFIG_PATH+CONFIG_AUTH, 'w') as f:
            f.write(DEFAULT_AUTH)
        raise ConfigurationValidationError("Configuration created. Please configure them!")

    try:
        with open(CONFIG_PATH+CONFIG_AUTH, 'r') as f:
            json.loads(f.read())
        print("Configuration validation successful")
    except Exception as err:
        raise InvalidJSON(f"The configuration file {f} is invalid!" + err)
    