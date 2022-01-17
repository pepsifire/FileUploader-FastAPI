import os
from typing import List

def getAuthFromEnv() -> bool:
    """Check stuff from the environment variables"""
    username = os.getenv('auth_user', None)
    password = os.getenv('auth_password', None)
    if username is None or password is None:
        return False
    return True

def getBaseUrl() -> str:
    return os.getenv('base_url', None)

def getUsername() -> str:
    return os.getenv('auth_user')

def getPassword() -> str:
    return os.getenv('auth_password')

def getAllowedContentTypes() -> List[str]:
    return os.getenv('allowed_content_types', None)