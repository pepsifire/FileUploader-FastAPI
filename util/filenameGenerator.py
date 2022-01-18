import secrets
import string

class filenameGenerator:
    """ Generate random filenames"""

    def generateName(length=5) -> string:
        filename = ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(length))
        return filename

    