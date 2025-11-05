from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    api_key = Column(String, unique=True, index=True, nullable=False)
    credits = Column(Integer, default=0, nullable=False)