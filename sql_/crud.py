# -*- coding: utf-8 -*- 
# @Time : 2020/12/17 16:05 
# @Author : hxq
# @File : crud.py
import time
from math import ceil

from pydantic.schema import datetime
from sqlalchemy.orm import Session

from sql_ import schemas, models


# user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_password(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# dir
def get_dir_list(db: Session, parent_id: int):
    return db.query(models.Dir).filter(models.Dir.parent_id == parent_id)


def get_dir_by_id(db: Session, id: int):
    return db.query(models.Dir).filter(models.Dir.id == id).first()


def get_dir_by_name_parent_id(db: Session, dirname: str, parent_id: int):
    return db.query(models.Dir).filter(models.Dir.parent_id == parent_id, models.Dir.dirname == dirname).first()


def create_dir(db: Session, dir: schemas.DirCreate):
    db_dir = models.Dir(dirname=dir.dirname, parent_id=dir.parent_id, flag=1, update_time=datetime.now(),
                        create_time=datetime.now())
    db.add(db_dir)
    db.commit()
    db.refresh(db_dir)
    return db_dir


# file

def get_file_by_dirid_(db: Session, dirid: int, filename: str):
    return db.query(models.File).filter(models.File.dirid == dirid, models.File.filename == filename).first()

def get_file_by_MD5_(db: Session, MD5:str):
    return db.query(models.File).filter(models.File.md5 == MD5).first()