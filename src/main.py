from fastapi import FastAPI

# Import our custom modules with their routers
import tts_service
import history_manager
import static_routes

# FastAPI setup
app = FastAPI(title="TTS API Service")

# Include the routers from each module
app.include_router(static_routes.router)
app.include_router(history_manager.router)
app.include_router(tts_service.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
