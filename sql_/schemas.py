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


class File(BaseModel):
    id: int
    dirid: int
    filename: str
    size: int
    w_h_px_: str
    md5: str
    create_time: datetime
    url: str
    dpi: str
    bslt_id: int
    slt_id: int
    del_flag: bool

    class Config:
        orm_mode = True


class Slt(BaseModel):
    id: int
    filename: str
    size: int
    w_h_px_: str
    md5: str
    create_time: datetime
    url: str
    dpi: str

    class Config:
        orm_mode = True


class DirBase(BaseModel):
    dirname: str
    parent_id: int


class DirCreate(DirBase):
    flag: int


class Dir(BaseModel):
    id: int
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True


class Bslt(BaseModel):
    id: int
    filename: str
    size: int
    w_h_px_: str
    md5: str
    create_time: datetime
    url: str
    dpi: str

    class Config:
        orm_mode = True

from fastapi import File
class FileUpload(BaseModel):
    chunkNumber: int
    chunkSize: str
    currentChunkSize: int
    filename: str
    identifier: str
    relativePath: int
    totalChunks: int
    totalSize: int
