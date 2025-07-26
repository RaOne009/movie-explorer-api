from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import time

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/movie_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

while True:
    try:
        with engine.connect() as connection:
            print("Connected to the database successfully.")
            break
    except Exception as e:
        print(f"Failed to connect to the database: {e}. Retrying in 5 seconds...")
        time.sleep(5)
        
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()