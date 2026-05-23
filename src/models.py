from database import Base
from sqlalchemy import Integer, Column, String, Float

class Books(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Float, default=0)

    