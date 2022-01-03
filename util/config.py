from dataclasses import dataclass


@dataclass
class configuration():
    UPLOAD_PATH = './upload/'
    CONFIG_PATH = './config/'
    CONFIG_AUTH = 'auth.json'
    ALLOWED_CONTENT = ['image/jpeg', 'image/png', 'image/gif']
    ERROR_UNALLOWED_CONTENT = "CONTENT TYPE IS NOT ALLOWED"
    BASE_URL = 'http://localhost:8000'
    IMAGE_DIR= '/media/'