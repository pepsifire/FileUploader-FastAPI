from fastapi import FastAPI, File, UploadFile
import os
UPLOAD_PATH = './upload/'
ALLOWED_CONTENT = ['image/jpeg', 'image/png', 'image/gif']
ERROR_UNALLOWED_CONTENT = "CONTENT TYPE IS NOT ALLOWED"
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
    # Create upload directory if it doesn't exist
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)
        print(f"Created {UPLOAD_PATH}")

async def uploadFile(file: UploadFile = File(...)):
    content = await file.read()
    with open(UPLOAD_PATH+file.filename, 'wb') as f:
        f.write(content)