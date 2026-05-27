from fastapi import APIRouter, HTTPException, Depends, Path, status
from typing import Annotated
from sqlalchemy.orm import Session

from src.models import Books, Base, BookRequest
from src.database import engine, SessionLocal
from src.routers.auth import get_current_user

router = APIRouter(
    prefix='/v1/books',
    tags=['books']
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/")
async def all_books(db: db_dependency):
    return db.query(Books).all()

@router.get("/{book_id}")
async def book_by_id(user: user_dependency, db: Annotated[Session, Depends(get_db)], book_id:int = Path(gt=0)):
    res =  db.query(Books).filter(Books.id == book_id).first()
    if res is None: raise HTTPException(status_code=404, detail="Book not found")
    if user.get('user_id') != res.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return res

@router.put("/", status_code=status.HTTP_201_CREATED)
async def create_new_book(user: user_dependency, db: db_dependency, book_request: BookRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="authentication failed")
    book_model = Books(**book_request.model_dump(), owner_id=user.get('user_id'))
    db.add(book_model)
    db.commit()
    db.refresh(book_model)
    return book_model

@router.put("/{book_id}", status_code=status.HTTP_204_NO_CONTENT) 
async def modify_book(user: user_dependency, book_request: BookRequest, db: db_dependency, book_id:int = Path(gt=0)): 
    book_model = db.query(Books).filter(Books.id == book_id).first() 
    if book_model is None: raise HTTPException(status_code=404, detail="Book not found")
    if user.get('user_id') != book_model.owner_id:  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    book_model.description = book_request.description
    book_model.price = book_request.price
    book_model.title = book_request.title
    db.add(book_model) 
    db.commit() 
    db.refresh(book_model) 

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def del_book(user: user_dependency, db: db_dependency, book_id: int = Path(gt=0)):
    book_model = db.query(Books).filter(Books.id == book_id).first() 
    if book_model is None: raise HTTPException(status_code=404, detail="Book not found")
    if user.get('user_id') != book_model.owner_id:  raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    db.query(Books).filter(Books.id == book_id).delete()
    db.commit()
