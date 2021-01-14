# -*- coding: utf-8 -*- 
# @Time : 2020/12/17 11:41 
# @Author : hxq
# @File : dependencies.py
'''依赖项'''
from fastapi import Header
from datetime import datetime, timedelta
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import BaseModel
import jwt, time
from fastapi import Depends, HTTPException
from sql_ import crud, models
from sql_.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    username: str
    password: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        exp: str = payload.get("exp")
        now_time = time.time()
        if int(exp) < now_time:
            raise credentials_exception
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = get_user(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user


def get_user(user_name: str, db=SessionLocal()):
    user = crud.get_password(db, username=user_name)
    return user


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if password != user.password:
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")
