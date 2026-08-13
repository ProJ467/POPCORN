# POPCORN 0.02v
# server/main.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .accounts import create_account, get_account


app = FastAPI(
    title="POPCORN API",
    version="0.02v"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "name": "POPCORN",
        "version": "0.02v",
        "status": "online"
    }


# ------------------------------------------------------------
# Static uploads
# ------------------------------------------------------------

UPLOADS_DIR = Path(__file__).resolve().parent / "uploads"

# ensure the uploads directory exists so StaticFiles can mount it
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="uploads"
)

# also expose files under /media for frontend compatibility
app.mount(
    "/media",
    StaticFiles(directory=str(UPLOADS_DIR)),
    name="media"
)


# ============================================================
# FILE LISTING
# ============================================================

@app.get("/files")
def list_files():
    """Return a simple JSON list of filenames under `server/uploads`.

    The frontend expects `{ files: [{ filename: 'name' }, ...] }`.
    """

    files = []

    image_exts = {"png", "jpg", "jpeg", "gif", "webp", "bmp", "svg"}
    video_exts = {"mp4", "mov", "webm", "mkv"}
    audio_exts = {"mp3", "wav", "ogg", "m4a"}

    try:
        for p in sorted(UPLOADS_DIR.iterdir()):
            if p.is_file() and not p.name.startswith('.'):
                ext = p.suffix.lower().lstrip('.')
                if ext in video_exts:
                    ftype = "video"
                elif ext in audio_exts:
                    ftype = "audio"
                elif ext in image_exts:
                    ftype = "image"
                else:
                    ftype = "other"

                files.append({"filename": p.name, "type": ftype})
    except Exception:
        raise HTTPException(status_code=500, detail="Could not list uploads")

    return {"files": files}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Accept a multipart upload and save into the uploads directory."""

    filename = Path(file.filename).name

    # avoid path traversal and collisions
    target = UPLOADS_DIR / filename
    if target.exists():
        base = target.stem
        suf = target.suffix
        i = 1
        while True:
            candidate = UPLOADS_DIR / f"{base}-{i}{suf}"
            if not candidate.exists():
                target = candidate
                break
            i += 1

    try:
        content = await file.read()
        with target.open("wb") as out:
            out.write(content)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to save uploaded file")

    return JSONResponse({"success": True, "filename": target.name})


@app.delete("/files/{filename}")
def delete_file(filename: str):
    safe = Path(filename).name
    target = UPLOADS_DIR / safe
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        target.unlink()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to delete file")

    return JSONResponse({"success": True})


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }


# ============================================================
# ACCOUNTS
# ============================================================

@app.post("/accounts")
def create_new_account():
    account = create_account()

    return {
        "success": True,
        "account": account
    }


@app.get("/accounts/{account_id}")
def get_account_by_id(account_id: str):
    account = get_account(account_id)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "success": True,
        "account": account
    }