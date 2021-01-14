# -*- coding: utf-8 -*- 
# @Time : 2020/12/17 11:25 
# @Author : hxq
# @File : user.py
from fastapi import APIRouter
from typing import List
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sql_ import crud, schemas, models
from sql_.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/passqord/")
def read_users(username:str,  db: Session = Depends(get_db)):
    users = crud.get_password(db, username=username)
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
