from fastapi import FastAPI
from src.routers import books, auth

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"Welcome to the book store API"}

app.include_router(books.router)
app.include_router(auth.router)

# uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
