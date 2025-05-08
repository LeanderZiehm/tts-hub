import os
import json
import asyncio
from fastapi import APIRouter, HTTPException

# Path for history storage
HISTORY_FILE = "tts_history.json"
OUTPUT_DIR = "tts_outputs"

# Create router for history endpoints
router = APIRouter(prefix="/history", tags=["history"])


def load_history():
    """Load conversion history from file"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []


def save_history(history):
    """Save conversion history to file"""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f)


def add_to_history(job_id, text, engine):
    """Add a new item to history"""
    history = load_history()
    history_item = {
        "jobId": job_id,
        "text": text,
        "engine": engine,
        "timestamp": str(asyncio.get_event_loop().time()),
    }

    history.insert(0, history_item)  # Add to beginning
    save_history(history)
    return history_item


def delete_history_item(job_id):
    """Delete a history item by job ID"""
    history = load_history()

    # Find and remove the item
    for i, item in enumerate(history):
        if item["jobId"] == job_id:
            del history[i]
            save_history(history)

            # Also delete the audio file if it exists
            output_path = os.path.join(OUTPUT_DIR, f"{job_id}.wav")
            if os.path.exists(output_path):
                os.remove(output_path)

            return {"success": True, "message": "History item deleted"}

    return None


def clear_history():
    """Clear all history"""
    history = load_history()

    # Delete all audio files
    for item in history:
        output_path = os.path.join(OUTPUT_DIR, f"{item['jobId']}.wav")
        if os.path.exists(output_path):
            os.remove(output_path)

    # Clear the history
    save_history([])
    return {"success": True, "message": "History cleared"}


# History API endpoints
@router.get("")
async def get_history():
    """Get all history items"""
    return load_history()


@router.delete("/{job_id}")
async def delete_history_endpoint(job_id: str):
    """Delete a history item by job ID"""
    result = delete_history_item(job_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="History item not found")


@router.delete("")
async def clear_history_endpoint():
    """Clear all history"""
    return clear_history()
