import uuid
import os
import asyncio
from concurrent.futures import ProcessPoolExecutor
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
from ttsEngines.ttsManager import get_tts_engines

# FastAPI setup
app = FastAPI()


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


@app.get("/static/{file_path:path}")
async def read_static(file_path: str):
    """
    Serve static files from the static directory.
    """
    file_path = os.path.join("static", file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


# Directory to store generated audio files
OUTPUT_DIR = "tts_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Map engine identifiers to classes
TTS_ENGINES = get_tts_engines()


# Job function executed in worker processes
def synthesize_job(tts_type: str, text: str, output_path: str) -> str:
    engine_cls = TTS_ENGINES.get(tts_type)
    if not engine_cls:
        raise ValueError(f"Unknown TTS engine: {tts_type}")
    engine = engine_cls()
    engine.synthesize(text, output_path)
    return output_path


executor = ProcessPoolExecutor(max_workers=os.cpu_count())

# Task tracking
tasks = {}  # id -> Future


@app.get("/tts/engines")
async def get_engines():
    """
    Returns a list of available TTS engines.
    """
    return list(TTS_ENGINES.keys())


class TTSRequest(BaseModel):
    text: str
    engine: str


@app.post("/tts/")
async def tts_request(request: TTSRequest):
    text = request.text
    engine = request.engine
    if engine not in TTS_ENGINES:
        raise HTTPException(status_code=400, detail="Unsupported TTS engine")
    job_id = str(uuid.uuid4())
    output_path = os.path.join(OUTPUT_DIR, f"{job_id}.wav")
    # Submit to process pool
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(executor, synthesize_job, engine, text, output_path)
    tasks[job_id] = future
    return {"job_id": job_id}


@app.get("/tts/{job_id}/status")
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


@app.get("/tts/{job_id}/download")
async def tts_download(job_id: str):
    future = tasks.get(job_id)
    if not future:
        raise HTTPException(status_code=404, detail="Job ID not found")
    if not future.done():
        raise HTTPException(status_code=400, detail="Job not finished yet")
    output_path = os.path.join(OUTPUT_DIR, f"{job_id}.wav")
    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="Output file missing")

    def iterfile():
        with open(output_path, "rb") as f:
            yield from f

    return StreamingResponse(iterfile(), media_type="audio/wav")
