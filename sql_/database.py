# -*- coding: utf-8 -*- 
# @Time : 2020/12/17 15:29 
# @Author : hxq
# @File : database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import pymysql
pymysql.install_as_MySQLdb()
SQLALCHEMY_DATABASE_URL = "mysql://root:123456@127.0.0.1:3306/sck2?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
