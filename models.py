from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DATETIME
from database import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    password = Column(String(500))
    fullname = Column(String(200), unique=True)


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    content = Column(Text)


class WeddingInfo(Base):
    __tablename__ = "wedding_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    bride_firstname = Column(String(100))
    bride_lastname = Column(String(100))
    groom_firstname = Column(String(100))
    groom_lastname = Column(String(100))
    datetime = Column(DATETIME)
    location = Column(Text)
    bestman_firstname = Column(String(100))
    bestman_lastname = Column(String(100))
    maidofhonor_firstname = Column(String(100))
    maidofhonor_lastname = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))





