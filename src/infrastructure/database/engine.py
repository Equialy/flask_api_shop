from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from src.settings import settings



DB_URL = settings.db.url_db


engine = create_engine(
    DB_URL
)

SessionFactory = sessionmaker (
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    future=True,
    autoflush=False,
)


class Base(DeclarativeBase):
    pass


def get_session() -> Generator[Session, None, None]:
    with SessionFactory() as session:
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


