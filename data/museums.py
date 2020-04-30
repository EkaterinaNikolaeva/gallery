import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

# Создание таблицы Museums для хранения информации о музеях

class Museum(SqlAlchemyBase):
    __tablename__ = 'Museums'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Addres = sqlalchemy.Column(sqlalchemy.String, nullable=True)
