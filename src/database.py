from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_CONNECT_URL = "sqlite:///./books.db"

engine = create_engine(url=DATABASE_CONNECT_URL, connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autoflush=False, expire_on_commit=False,bind=engine)

Base = declarative_base()
