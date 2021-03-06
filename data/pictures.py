import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

# Создание таблицы Pictures для хранения информации о картинах

class Picture(SqlAlchemyBase):
    __tablename__ = 'Pictures'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    Title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Museum = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Painter = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    Picture = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Info = sqlalchemy.Column(sqlalchemy.String, nullable=True)
