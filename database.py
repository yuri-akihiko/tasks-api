from sqlalchemy import create_engine, text
from sqlmodel import Field, SQLModel, Session


DB_NAME = "tasks"
BASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432"
postgres_url = f"{BASE_URL}/{DB_NAME}"

engine = create_engine(postgres_url)


def _ensure_database_exists():
    default_engine = create_engine(f"{BASE_URL}/postgres", isolation_level="AUTOCOMMIT")
    with default_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": DB_NAME},
        ).fetchone()
        if not exists:
            conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
    default_engine.dispose()


def create_db_and_tables():
    _ensure_database_exists()
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session