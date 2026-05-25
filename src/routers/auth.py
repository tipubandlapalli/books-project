from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from pydantic import BaseModel, BaseModelf, BeforeValidator
from models import Users
from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
db_session = Annotated[Session, Depends(get_db)]

router = APIRouter()

bcyrpt_context =  CryptContext(schemes=['bcrypt'], deprecated='auto')
StrippedStr = Annotated[str, BeforeValidator(lambda v: v.strip() if isinstance(v, str) else v) ]
class UserRequest(BaseModel):
    username: StrippedStr
    password: StrippedStr
    age: int
    role: StrippedStr
    
    
@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_req: UserRequest, db: db_session):
    if db.query(Users).filter(Users.username == create_user_req.username).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username not available")
    new_user = Users(
        username=create_user_req.username,
        hashed_password=bcyrpt_context.hash(create_user_req.password),
        role=create_user_req.role,
        age=create_user_req.age,
    )
    db.add(new_user)
    db.commit()
    return new_user

