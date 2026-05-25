from fastapi import FastAPI
from routers import books, auth

app = FastAPI()

app.include_router(books.router)
app.include_router(auth.router)
