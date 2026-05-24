from database import Base
from sqlalchemy import Integer, Column, String, Float
from pydantic import BaseModel, Field

class Books(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, default=0)


class BookRequest(BaseModel):
    title:str = Field(min_length=1, max_length=10)
    description:str
    price: float = Field(ge=0)
    