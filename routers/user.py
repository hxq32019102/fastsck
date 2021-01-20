# -*- coding: utf-8 -*- 
# @Time : 2020/12/17 11:25 
# @Author : hxq
# @File : user.py
from fastapi import APIRouter
from sqlalchemy.orm import Session

from dependencies import *
from sql_ import crud, models
from sql_.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/password/change")
def read_users(username:str,old_password:str,new_password:str,db: Session = Depends(get_db)):
    '''修改 密码'''
    users = crud.password_change(db, username=username,password=old_password,new_password=new_password)
    return users

