from fastapi import FastAPI, HTTPException
from src.Book import Book

app = FastAPI()

BOOKS = {
    1: Book(id=1, title="A", description="description", price=120),
    2: Book(id=2, title="B", description="description", price=104),
    3: Book(id=3, title="C", description="description", price=104),
    4: Book(id=4, title="D", description="description", price=1025),
}

@app.get("/v1/books")
async def all_books():
    return BOOKS


@app.get("/v1/books/{id}")
async def get_book_by_id(id: int):
    if id in BOOKS:
        return BOOKS[id]
    raise HTTPException(status_code=404, detail="book not found")

@app.post("/v1/books")
async def create_new_book(book: Book):
    if book.id in BOOKS:
        raise HTTPException(status_code=409, detail="id already exists")
    BOOKS[book.id] = book