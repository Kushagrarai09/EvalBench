import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
load_dotenv(Path(__file__).resolve().parents[1] / ".env")
URL=os.getenv("DATABASE_URL", "sqlite:///./evalbench.db")
engine=create_engine(URL, connect_args={"check_same_thread":False} if URL.startswith("sqlite") else {}, future=True)
SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base=declarative_base()
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
