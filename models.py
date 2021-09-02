import os
from functools import wraps
from os import environ as env
from sqlalchemy import (BLOB, DECIMAL, SMALLINT, TIMESTAMP, VARCHAR, DateTime,
                        BigInteger, Boolean, Column, Float, ForeignKey, Date, Time,
                        Integer, LargeBinary, String, Text, and_,
                        create_engine, func, not_, or_, text)
from sqlalchemy.exc import OperationalError, StatementError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import numpy as np
import sqlalchemy


DBDATA = os.getenv('SOLMATE_DB_URL')
DB_URL = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format(DBDATA.split(',')[0], DBDATA.split(
    ',')[1], DBDATA.split(',')[2], DBDATA.split(',')[3], DBDATA.split(',')[4])


Base = declarative_base()
engine = create_engine(DB_URL, pool_recycle=3600,
                       connect_args={'connect_timeout': 60})


def add_own_encoders(conn, cursor, query, *args):
    cursor.connection.encoders[np.int64] = lambda value, encoders: int(value)


event.listen(engine, "before_cursor_execute", add_own_encoders)


session = sessionmaker(bind=engine)

# class Users(Base):
#     __tablename__ = 'users'

#     idusers = Column(Integer, primary_key=True)
#     email = Column(Text)
#     username = Column(Text)
#     password = Column(Text)
#     status = Column(Text)
#     addTimestamp = Column(TIMESTAMP)


class Users(Base):
    __tablename__ = "users"
    
    idusers = Column(Integer, primary_key=True, index=True)
    public_key = Column(String, unique=True)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))


class WeddingInfo(Base):
    __tablename__ = "wedding_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.idusers',
                               ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    account_id = Column(Text)
    trasaction_id = Column(Text)
    bride_firstname = Column(String(100))
    bride_lastname = Column(String(100))
    groom_firstname = Column(String(100))
    groom_lastname = Column(String(100))
    datetime = Column(DateTime)
    location = Column(Text)
    bestman_firstname = Column(String(100))
    bestman_lastname = Column(String(100))
    maidofhonor_firstname = Column(String(100))
    maidofhonor_lastname = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

class Nft(Base):
    __tablename__ = "nft"

    idnft = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.idusers',
                               ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    datetime = Column(DateTime)
    image = Column(BLOB)
    metadata_account_address = Column(Text)
    minted_token_address = Column(Text)
    nft_address = Column(Text)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

class Social(Base):
    __tablename__ = "social"

    idsocial = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users.idusers',
                                ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    url = Column(Text)
    likes = Column(Integer, server_default=text("'0'"))
    shares = Column(Integer, server_default=text("'0'"))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
