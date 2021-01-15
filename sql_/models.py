# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DirInfo(Base):
    __tablename__ = 'dir_info'

    id = Column(Integer, primary_key=True)
    dir_name = Column(String(255), nullable=False)
    parent_id = Column(Integer)
    creat_time = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False, server_default=text("'1'"))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)


class FileInfo(Base):
    __tablename__ = 'file_info'

    file_id = Column(Integer, primary_key=True)
    dir_id = Column(ForeignKey('dir_info.id'), nullable=False, index=True)
    file_name = Column(VARCHAR(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    file_upload_time = Column(DateTime, nullable=False)
    file_status = Column(Integer, nullable=False, server_default=text("'1'"))
    uid = Column(VARCHAR(255), nullable=False)

    dir = relationship('DirInfo')
