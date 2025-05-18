import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

# Create router for static content
router = APIRouter(tags=["static"])


@router.get("/hacked")
async def hacked():
    return "hacked"



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
