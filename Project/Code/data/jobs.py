import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'user_request'
    user_request_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer(), nullable=False)
    description = Column(String(500), nullable=False)
    result = Column(String(100), nullable=False)
