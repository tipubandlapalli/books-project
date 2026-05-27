from fastapi import FastAPI
from routers import books, auth

app = FastAPI()

app.include_router(books.router)
app.include_router(auth.router)

# uvicorn main:app --host 127.0.0.1 --port 8000 --reload
