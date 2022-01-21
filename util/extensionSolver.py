import magic
import mimetypes

def guessMime(file) -> str:
    return magic.from_buffer(file, mime=True)

def guessFileExtension(file) -> str:
    mime = guessMime(file)
    return mimetypes.guess_extension(mime)

