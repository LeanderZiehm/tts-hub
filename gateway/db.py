import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)