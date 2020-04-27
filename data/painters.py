import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Painter(SqlAlchemyBase):
    __tablename__ = 'Painters'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    Name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    Title_of_photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)