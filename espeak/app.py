from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import subprocess
import uuid
from pathlib import Path

app = FastAPI(title="ESpeak TTS Service")

OUTPUT_DIR = Path("/tmp/tts_out")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.post("/synthesize")
def synthesize(text: str):
    try:
        out_file = OUTPUT_DIR / f"{uuid.uuid4()}.wav"
        subprocess.run(
            ["espeak", text, "--stdout"],
            check=True,
            stdout=open(out_file, "wb")
        )
        return FileResponse(out_file, media_type="audio/wav", filename=out_file.name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))