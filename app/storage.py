import os
import uuid
from app.config import settings

def save_file(file):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(settings.UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    return path
