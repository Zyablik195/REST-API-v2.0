import sqlalchemy
from .db_session import SqlAlchemyBase


class Hazards(SqlAlchemyBase):
    __tablename__ = 'hazards'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    factor = sqlalchemy.Column(sqlalchemy.String, nullable=True)