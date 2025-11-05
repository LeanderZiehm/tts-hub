from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from kokoro import KPipeline
import soundfile as sf
import numpy as np
import uuid
from pathlib import Path

app = FastAPI(title="Kokoro TTS Service")

# Initialize the pipeline with American English
pipeline = KPipeline(lang_code='a') 
OUTPUT_DIR = Path("/tmp/tts_out")
OUTPUT_DIR.mkdir(exist_ok=True)

@app.post("/synthesize")
def synthesize(text: str, voice: str = 'af_heart'):
    try:
        out_file = OUTPUT_DIR / f"{uuid.uuid4()}.wav"
        
        # The pipeline returns a generator
        generator = pipeline(text, voice=voice)
        
        audio_chunks = []
        for i, (gs, ps, audio) in enumerate(generator):
            audio_chunks.append(audio)
        
        if not audio_chunks:
            raise HTTPException(status_code=500, detail="Audio generation failed.")

        full_audio = np.concatenate(audio_chunks)

        sf.write(out_file, full_audio, 24000)
        
        return FileResponse(out_file, media_type="audio/wav", filename=out_file.name)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
