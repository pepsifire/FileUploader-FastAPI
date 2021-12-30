import os

def checkEnvirontmentVariables() -> bool:
    """Check stuff from the environment variables"""
    username = os.getenv('auth_user', None)
    password = os.getenv('auth_password', None)
    if username is None or password is None:
        return False
    return True


def getUsername() -> str:
    return os.getenv('auth_user')

def getPassword() -> str:
    return os.getenv('auth_password')