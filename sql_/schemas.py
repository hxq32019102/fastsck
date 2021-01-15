# -*- coding: utf-8 -*- 
# @Time : 2020/12/17 16:02 
# @Author : hxq
# @File : schemas.py
from fastapi import UploadFile
from pydantic import BaseModel
from pydantic.schema import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class FileCreate(BaseModel):
    dir_id: int




class File(FileCreate):
    file_name: str
    file_id: int
    file_size: int
    file_upload_time: datetime
    file_status: int
    uid:str

    class Config:
        orm_mode = True


class DirBase(BaseModel):
    dir_name: str
    parent_id: int


class DirCreate(DirBase):
    status: int


class Dir(BaseModel):
    id: int
    creat_time: datetime

    class Config:
        orm_mode = True


class FileUpload(BaseModel):
    chunkNumber: int
    chunkSize: str
    currentChunkSize: int
    filename: str
    identifier: str
    relativePath: int
    totalChunks: int
    totalSize: int
