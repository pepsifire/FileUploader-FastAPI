from fastapi import File, UploadFile, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic
import secrets
from util.CustomException import ConfigurationValidationError, InvalidJSON
from util.defaultConfig import DEFAULT_AUTH
from util import credentialStore, envVars, config
import json
import os

security = HTTPBasic()
creds = credentialStore.credentailStore()
configuration = config.configuration()

async def checkCredentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, creds.username)
    correct_password = secrets.compare_digest(credentials.password, creds.password)
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
    with open(configuration.UPLOAD_PATH+file.filename, 'wb') as f:
        f.write(content)

def validateConfiguration():
    if envVars.getAllowedContentTypes() is not None:
        configuration.ALLOWED_CONTENT = envVars.getAllowedContentTypes()
    if envVars.getBaseUrl() is not None:
        configuration.BASE_URL = envVars.getBaseUrl()
    if envVars.getAuthFromEnv():
        print("Loading configuration from environment variables")
        creds.username = envVars.getUsername()
        creds.password = envVars.getPassword()
    else:
        if not os.path.exists(configuration.CONFIG_PATH+configuration.CONFIG_AUTH):
            os.makedirs(configuration.CONFIG_PATH, exist_ok=True)
            with open(configuration.CONFIG_PATH+configuration.CONFIG_AUTH, 'w') as f:
                f.write(DEFAULT_AUTH)
            raise ConfigurationValidationError("Configuration created. Please configure them!")

        try:
            with open(configuration.CONFIG_PATH+configuration.CONFIG_AUTH, 'r') as f:
                content = json.loads(f.read())
                creds.username = content['USERNAME']
                creds.password = content['PASSWORD']
            print("Configuration validation successful")
            print(configuration.ALLOWED_CONTENT)
        except Exception as err:
            raise InvalidJSON(f"The configuration file {f} is invalid!" + err)

