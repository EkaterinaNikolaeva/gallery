import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

# Создание таблицы pictures для хранения информации о картинах

class Picture(SqlAlchemyBase):
    __tablename__ = 'pictures'
    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)

    #Museum = sqlalchemy.Column(sqlalchemy.Integer)
    #Painter = sqlalchemy.Column(sqlalchemy.Integer)
   
