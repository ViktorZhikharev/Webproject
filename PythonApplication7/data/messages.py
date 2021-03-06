import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    author = sqlalchemy.Column(sqlalchemy.Integer, 
                                    sqlalchemy.ForeignKey("users.id"))
    reciever = sqlalchemy.Column(sqlalchemy.Integer)
    user = orm.relation('User')