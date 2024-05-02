from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base


db_url = "postgresql+psycopg2://postgres:admin@localhost/postgres"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
