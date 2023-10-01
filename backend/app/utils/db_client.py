# Purpose: Database client for handling database operations
# Path: backend\app\utils\db_client.py
import sys

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models import Base


class DBClient:
    engine: create_engine = None
    Session: sessionmaker = None

    postgres_host: str = settings.postgres_host
    postgres_user: str = settings.postgres_user
    postgres_password: str = settings.postgres_password
    postgres_port: int = settings.postgres_port

    logger.configure(
        handlers=[
            dict(sink=sys.stdout, level="INFO", colorize=True),
            dict(sink=sys.stderr, level="CRITICAL", colorize=True),
        ],
    )

    @classmethod
    def __init__(cls) -> None | Exception:
        cls.connect()

    @classmethod
    def connect(cls) -> None | Exception:
        try:
            if not cls.engine or not cls.Session:
                cls.engine = create_engine(
                    f"postgresql://{cls.postgres_user}:{cls.postgres_password}@{cls.postgres_host}:{cls.postgres_port}/db"
                )
                cls.Session = sessionmaker(
                    autocommit=False, autoflush=False, bind=cls.engine
                )

                logger.info("Success: Database client connected")

                cls.create_tables()

        except Exception as _:
            logger.critical("Error: Database client could not be connected")
            raise Exception()

    @classmethod
    def disconnect(cls) -> None | Exception:
        try:
            if cls.engine and cls.Session:
                cls.engine.dispose()
                cls.Session = None
                logger.info("Success: Database client disconnected")

        except Exception as _:
            logger.critical("Error: Database client could not be disconnected")
            raise Exception()

    @classmethod
    def create_tables(cls) -> None | Exception:
        try:
            Base.metadata.create_all(bind=cls.engine)
            logger.info("Success: Database tables created successfully")

        except Exception as e:
            logger.critical("Error: Database tables could not be created")
            raise e

    @classmethod
    def get_db_session(cls) -> Session:
        session = cls.Session()
        try:
            yield session
        finally:
            session.close()


db_client = DBClient()
