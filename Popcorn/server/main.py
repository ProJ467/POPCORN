from pathlib import Path
import mimetypes

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI(
    title="POPCORN API",
    version="0.1.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# DIRECTORIES
# =========================

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(exist_ok=True)


# =========================
# HOME
# =========================

@app.get("/")
async def root():

    return {
        "name": "POPCORN",
        "version": "0.1.0",
        "status": "online"
    }


# =========================
# FILE LIST
# =========================

@app.get("/files")
async def get_files():

    files = []

    for file in UPLOAD_DIR.iterdir():

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        if extension == ".mp4":
            file_type = "video"

        elif extension == ".mp3":
            file_type = "audio"

        elif extension in [
            ".png",
            ".jpg",
            ".jpeg",
            ".gif",
            ".webp"
        ]:
            file_type = "image"

        elif extension == ".html":
            file_type = "html"

        elif extension == ".py":
            file_type = "python"

        else:
            file_type = "file"

        files.append({
            "filename": file.name,
            "type": file_type
        })

    return {
        "files": files
    }


# =========================
# UPLOAD
# =========================

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is missing."
        )

    filename = Path(
        file.filename
    ).name

    file_path = UPLOAD_DIR / filename

    if file_path.exists():

        raise HTTPException(
            status_code=409,
            detail="A file with this name already exists."
        )

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            while True:

                chunk = await file.read(
                    1024 * 1024
                )

                if not chunk:
                    break

                buffer.write(chunk)

    except Exception as error:

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {error}"
        )

    return {
        "success": True,
        "filename": filename
    }


# =========================
# DELETE
# =========================

@app.delete("/files/{filename}")
async def delete_file(
    filename: str
):

    filename = Path(filename).name

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    try:

        file_path.unlink()

    except PermissionError:

        raise HTTPException(
            status_code=423,
            detail="File is currently in use."
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    return {
        "success": True,
        "filename": filename
    }


# =========================
# MEDIA
# =========================

@app.get("/media/{filename}")
async def media(
    filename: str
):

    filename = Path(filename).name

    file_path = UPLOAD_DIR / filename

    if not file_path.exists():

        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    if not file_path.is_file():

        raise HTTPException(
            status_code=400,
            detail="Not a file."
        )

    media_type, _ = mimetypes.guess_type(
        filename
    )

    if media_type is None:

        media_type = "application/octet-stream"

    return FileResponse(
        path=file_path,
        media_type=media_type
    )


# =========================
# STATIC FILES
# =========================

app.mount(
    "/uploads",
    StaticFiles(
        directory=UPLOAD_DIR
    ),
    name="uploads"
)