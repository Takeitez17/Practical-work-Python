import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
