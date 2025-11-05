from fastapi import FastAPI, HTTPException, Header, Depends
import os, secrets
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx

from db import SessionLocal, engine
from models import Base, User
from schemas import UserCreateResponse

app = FastAPI(title="TTS Gateway")
INITIAL_CREDITS = int(os.getenv("INITIAL_CREDITS", "100"))
ADMIN_SECRET = os.getenv("ADMIN_SECRET")

ENGINE_PRICES = {"espeak": 1, "piper": 2, "kokoro": 3}
ENGINE_ENDPOINTS = {
    "espeak": "http://tts_espeak:8000/synthesize",
    "piper": "http://tts_piper:8000/synthesize",
    "kokoro": "http://tts_kokoro:8000/synthesize"
}

async def get_db():
    async with SessionLocal() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/admin/create_user", response_model=UserCreateResponse)
async def create_user(admin_secret: str, db: AsyncSession = Depends(get_db)):
    if admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    api_key = secrets.token_hex(16)
    user = User(api_key=api_key, credits=INITIAL_CREDITS)
    db.add(user)
    await db.commit()
    return UserCreateResponse(api_key=api_key, credits=user.credits)

@app.get("/credits")
async def credits(authorization: str = Header(None), db: AsyncSession = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid bearer token")
    key = authorization.split(" ")[1]

    result = await db.execute(select(User).where(User.api_key == key))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return {"credits": user.credits}

@app.post("/synthesize")
async def synthesize(text: str, engine: str, authorization: str = Header(None), db: AsyncSession = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid bearer token")
    key = authorization.split(" ")[1]

    result = await db.execute(select(User).where(User.api_key == key))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if engine not in ENGINE_PRICES:
        raise HTTPException(status_code=400, detail="Unsupported engine")

    cost = ENGINE_PRICES[engine]
    if user.credits < cost:
        raise HTTPException(status_code=402, detail="Insufficient credits")

    async with httpx.AsyncClient(timeout=60) as client:
        backend = ENGINE_ENDPOINTS[engine]
        r = await client.post(backend, json={"text": text})
        r.raise_for_status()

    user.credits -= cost
    await db.commit()

    return r



