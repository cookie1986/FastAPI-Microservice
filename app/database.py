from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db" # if using sqlite
SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:dc8294dc8294!!@localhost/postgres'

# create database
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# create engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define base class - all python classes (i.e., tables) will extend from this base class
Base = declarative_base()

# dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()