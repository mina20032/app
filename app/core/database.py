from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.core.config import get_settings


settings = get_settings()

engine = create_engine(
    str(settings.database_url),
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database tables (for first-time setup / dev).
    In production you can replace this with Alembic migrations.
    """
    # Import models so that they are registered with SQLAlchemy's metadata
    from app import models  # noqa

    Base.metadata.create_all(bind=engine)
