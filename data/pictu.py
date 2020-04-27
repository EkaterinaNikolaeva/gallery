import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Picture(SqlAlchemyBase):
    __tablename__ = 'pictures'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)

    #Museum = sqlalchemy.Column(sqlalchemy.Integer)
    #Painter = sqlalchemy.Column(sqlalchemy.Integer)
   