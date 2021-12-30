from fastapi import File, UploadFile, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets
from util.CustomException import ConfigurationValidationError, InvalidJSON
from util.defaultConfig import DEFAULT_AUTH
from config.vars import *
import json
import os

security = HTTPBasic()

async def checkCredentails(credentials: HTTPBasicCredentials = Depends(security)):
    with open(CONFIG_PATH+CONFIG_AUTH, 'r') as f:
            content = json.loads(f.read())
            correct_username = secrets.compare_digest(credentials.username, content['USERNAME'])
            correct_password = secrets.compare_digest(credentials.password, content['PASSWORD'])
    if correct_username and correct_password:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )

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

