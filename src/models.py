from database import Base
from sqlalchemy import Integer, Column, String, Float, ForeignKey
from pydantic import BaseModel, Field

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    age = Column(Integer)
    role = Column(String)
class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, default=0)
    owner_id = Column(ForeignKey("users.id"))

class BookRequest(BaseModel):
    title:str = Field(min_length=1, max_length=10)
    description:str
    price: float = Field(ge=0)
    