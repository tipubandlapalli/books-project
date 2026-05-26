top_secret = {
    'SECRET_KEY':"E42PmIo6toP5PlZ2KxUdz0RtScdwGhh+bBjT9kIr/2U=",
    'ALGORITHM':"HS256"
}

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from pydantic import BaseModel, BaseModel, BeforeValidator
from models import Users
from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import jwt

router = APIRouter(
    prefix='/user',
    tags=['auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='user/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()
db_session = Annotated[Session, Depends(get_db)]



bcyrpt_context =  CryptContext(schemes=['bcrypt'], deprecated='auto')

StrippedStr = Annotated[str, BeforeValidator(lambda v: v.strip() if isinstance(v, str) else v) ]
class UserRequest(BaseModel):
    username: StrippedStr
    password: StrippedStr
    age: int
    role: StrippedStr


@router.post("/register", status_code=status.HTTP_201_CREATED, description="User created successfully")
async def register_user(create_user_req: UserRequest, db: db_session):
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

async def auth_user(username, password, db):
        user = db.query(Users).filter(Users.username == username).first()
        if user and bcyrpt_context.verify(password, user.hashed_password):
            return user
        return None

def generate_token(username: str, user_id: int, expires_delta:timedelta):
        encode = {'sub': username, 'id': user_id, 'exp': datetime.now() + expires_delta}
        return {
            "access_token":jwt.encode(encode,top_secret['SECRET_KEY'], top_secret['ALGORITHM']),
            "token_type":"bearer"
        }

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db : db_session):
    try:
        payload = jwt.decode(token, top_secret["SECRET_KEY"], algorithms=[top_secret['ALGORITHM']])
        username = payload.get('sub')
        user_id = payload.get('id')
        if username and user_id:
            return {'username': username, 'user_id': user_id}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except :
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
         
@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_session):
    
    if user:= await auth_user(form_data.username, form_data.password, db):
            return generate_token(user.username, user.id, timedelta(minutes=5))
        
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="invalid credentials")