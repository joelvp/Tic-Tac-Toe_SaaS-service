from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

def get_engine():
    DATABASE_URL = (
        f"postgresql://{os.getenv('DB_USER','user')}:"
        f"{os.getenv('DB_PASSWORD','pass')}@"
        f"{os.getenv('DB_HOST','localhost')}:"
        f"{os.getenv('DB_PORT','5432')}/"
        f"{os.getenv('DB_NAME','test_db')}"
    )
    return create_engine(DATABASE_URL, echo=True)

def get_session():
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()

def get_db():
    """
    Provides a SQLAlchemy database session.
    Ensures the session is closed after use.
    """
    db = get_session()
    try:
        yield db
    finally:
        db.close()
