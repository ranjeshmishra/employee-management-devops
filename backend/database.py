
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def check_database_connection():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database(), current_user")
        )
        return result.fetchone()

def get_db():
    with SessionLocal() as db:
        yield db

if __name__ == "__main__":
    result = check_database_connection()
    print("Database:", result[0])
    print("Connected user:", result[1])
    print("PostgreSQL connection successful")
