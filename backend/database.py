
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Docker Compose configuration
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

if all([
    DATABASE_HOST,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD,
]):
    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=int(DATABASE_PORT),
        database=DATABASE_NAME,
    )
else:
    # Existing Windows local configuration
    database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise RuntimeError("Database configuration is missing")

engine = create_engine(
    database_url,
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
