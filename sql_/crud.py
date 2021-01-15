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
    return db.query(models.DirInfo).filter(models.DirInfo.parent_id == parent_id)


def get_dir_by_id(db: Session, id: int):
    return db.query(models.DirInfo).filter(models.DirInfo.id == id).first()


def get_dir_by_name_parent_id(db: Session, dirname: str, parent_id: int):
    return db.query(models.DirInfo).filter(models.DirInfo.parent_id == parent_id, models.DirInfo.dir_name == dirname).first()


def create_dir(db: Session, dir: schemas.DirCreate):
    db_dir = models.DirInfo(dir_name=dir.dir_name, parent_id=dir.parent_id, status=1,creat_time=datetime.now())
    db.add(db_dir)
    db.commit()
    db.refresh(db_dir)
    return db_dir



# file
def get_file_list(db: Session, dir_id: int):
    return db.query(models.FileInfo).filter(models.FileInfo.dir_id == dir_id)



def get_file_by_dirid_filename(db: Session, dirid: int, filename: str):
    return db.query(models.FileInfo).filter(models.FileInfo.dir_id == dirid, models.FileInfo.file_name == filename).first()

def get_file_by_uid(db: Session, uid: str):
    return db.query(models.FileInfo).filter(models.FileInfo.uid == uid).first()
def get_file_name_by_url(db: Session, uid: str):
    return db.query(models.FileInfo).filter(models.FileInfo.uid == uid).first()
def create_file(db: Session,dir_id:int,file_name:str,file_size:int,uid:str):
    db_file = models.FileInfo(dir_id=dir_id,file_name=file_name,file_size=file_size,file_upload_time=datetime.now(),uid=uid)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file
    # file_id = Column(Integer, primary_key=True)
    # dir_id = Column(ForeignKey('dir_info.id'), nullable=False, index=True)
    # file_name = Column(VARCHAR(255), nullable=False)
    # file_size = Column(Integer, nullable=False)
    # file_upload_time = Column(DateTime, nullable=False)
    # file_status = Column(Integer, nullable=False, server_default=text("'1'"))
    # url = Column(String(255), nullable=False)


