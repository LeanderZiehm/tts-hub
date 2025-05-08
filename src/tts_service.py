import os
import uuid
import asyncio
from concurrent.futures import ProcessPoolExecutor
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from ttsEngines.ttsManager import get_tts_engines

# Import history manager to add items to history
import history_manager

# Directory to store generated audio files
OUTPUT_DIR = "tts_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Map engine identifiers to classes
TTS_ENGINES = get_tts_engines()

# Create a process pool executor
executor = ProcessPoolExecutor(max_workers=os.cpu_count())

# Task tracking
tasks = {}  # id -> Future

# Create router for TTS endpoints
router = APIRouter(prefix="/tts", tags=["tts"])


def synthesize_job(tts_type: str, text: str, output_path: str) -> str:
    """
    Job function executed in worker processes
    """
    engine_cls = TTS_ENGINES.get(tts_type)
    if not engine_cls:
        raise ValueError(f"Unknown TTS engine: {tts_type}")
    engine = engine_cls()
    engine.synthesize(text, output_path)
    return output_path


def get_available_engines():
    """
    Returns a list of available TTS engines.
    """
    return list(TTS_ENGINES.keys())


def get_output_path(job_id):
    """
    Returns the output path for a job
    """
    return os.path.join(OUTPUT_DIR, f"{job_id}.wav")


def generate_job_id():
    """
    Generate a unique job ID
    """
    return str(uuid.uuid4())


def delete_tts_file(job_id):
    """
    Delete a TTS file by job ID
    """
    output_path = get_output_path(job_id)
    if os.path.exists(output_path):
        os.remove(output_path)
        return True
    return False


# TTS API endpoint models
class TTSRequest(BaseModel):
    text: str
    engine: str


# TTS API endpoints
@router.get("/engines")
async def get_engines_endpoint():
    """
    Returns a list of available TTS engines.
    """
    return get_available_engines()


@router.post("/")
async def tts_request(request: TTSRequest):
    text = request.text
    engine = request.engine

    available_engines = get_available_engines()
    if engine not in available_engines:
        raise HTTPException(status_code=400, detail="Unsupported TTS engine")

    job_id = generate_job_id()
    output_path = get_output_path(job_id)

    # Submit to process pool
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(executor, synthesize_job, engine, text, output_path)
    tasks[job_id] = future

    # Add to history
    history_item = history_manager.add_to_history(job_id, text, engine)

    return {"job_id": job_id, "history_item": history_item}


@router.get("/{job_id}/status")
async def tts_status(job_id: str):
    future = tasks.get(job_id)
    if not future:
        raise HTTPException(status_code=404, detail="Job ID not found")
    if future.done():
        try:
            # This will re-raise exceptions if any
            future.result()
            return {"status": "finished"}
        except Exception as e:
            return {"status": "error", "detail": str(e)}
    return {"status": "pending"}


@router.get("/{job_id}/download")
async def tts_download(job_id: str):
    future = tasks.get(job_id)
    if not future:
        raise HTTPException(status_code=404, detail="Job ID not found")
    if not future.done():
        raise HTTPException(status_code=400, detail="Job not finished yet")

    output_path = get_output_path(job_id)
    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="Output file missing")

    def iterfile():
        with open(output_path, "rb") as f:
            yield from f

    return StreamingResponse(iterfile(), media_type="audio/wav")


@router.delete("/{job_id}/delete")
async def delete_tts_file_endpoint(job_id: str):
    """Delete a TTS file by job ID"""
    if delete_tts_file(job_id):
        # Also delete from history
        result = history_manager.delete_history_item(job_id)
        if result:
            return result

    raise HTTPException(status_code=404, detail="File not found")
