from fastapi import FastAPI, HTTPException, Depends, Path, status
from typing import Annotated
from sqlalchemy.orm import Session

from models import Books, Base, BookRequest
from database import engine, SessionLocal

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/v1/books")
async def all_books(db: db_dependency):
    return db.query(Books).all()

@app.get("/v1/books/{book_id}")
async def book_by_id(db: Annotated[Session, Depends(get_db)], book_id:int = Path(gt=0)):
    res =  db.query(Books).filter(Books.id == book_id).first()
    if res is None: raise HTTPException(status_code=404, detail="Book not found")
    return res

@app.post("/v1/books", status_code=status.HTTP_201_CREATED)
async def create_new_book(db: db_dependency, book_request: BookRequest):
    book_model = Books(**book_request.model_dump())
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model

@app.put("/v1/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def modify_book(book_request: BookRequest, db: db_dependency, book_id:int = Path(gt=0)):
    book_model = db.query(Books).filter(Books.id == book_id).first() 
    if book_model is None: raise HTTPException(status_code=404, detail="Book not found")
    book_model.description = book_request.description
    book_model.price = book_request.price
    book_model.title = book_request.title
    db.add(book_model)
    db.commit()
    db.refresh(book_model)

@app.delete("/v1/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_book(db: db_dependency, book_id: int = Path(gt=0)):
    book_model = db.query(Books).filter(Books.id == book_id).first() 
    if book_model is None: raise HTTPException(status_code=404, detail="Book not found")

    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()
