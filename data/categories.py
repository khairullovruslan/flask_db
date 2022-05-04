
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, UserMixin):
    __tablename__ = 'categories'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    danger_activities = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    jobs = orm.relation("Jobs", back_populates='category')
