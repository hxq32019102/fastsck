# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, LargeBinary, String, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Bslt(Base):
    __tablename__ = 'bslt'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    w_h_px_ = Column('w*h(px)', String(255), nullable=False)
    md5 = Column(String(255), nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)
    url = Column(String(255), nullable=False)
    dpi = Column(String(255), nullable=False)


class Dir(Base):
    __tablename__ = 'dir'

    id = Column(Integer, primary_key=True)
    dirname = Column(String(255), nullable=False)
    parent_id = Column(Integer, nullable=False, index=True)
    flag = Column(Integer, nullable=False, server_default=text("'1'"))
    update_time = Column(TIMESTAMP, nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)


class Slt(Base):
    __tablename__ = 'slt'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    w_h_px_ = Column('w*h(px)', String(255), nullable=False)
    md5 = Column(String(255), nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)
    url = Column(String(255), nullable=False)
    dpi = Column(String(255), nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    dirid = Column(ForeignKey('dir.id'), index=True)
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    w_h_px_ = Column('w*h(px)', String(255), nullable=False)
    md5 = Column(String(255), nullable=False)
    create_time = Column(TIMESTAMP, nullable=False)
    url = Column(String(255), nullable=False)
    dpi = Column(String(255), nullable=False)
    bslt_id = Column(ForeignKey('bslt.id'), nullable=False, index=True)
    slt_id = Column(ForeignKey('slt.id'), nullable=False, index=True)
    del_flag = Column('del-flag', LargeBinary, nullable=False)

    bslt = relationship('Bslt')
    dir = relationship('Dir')
    slt = relationship('Slt')
